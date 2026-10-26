#!/usr/bin/env python3
"""Machine-check question answers with SymPy and write data/verification_report.json.

Each question may carry `verify`: a SymPy expression (string) for the correct answer.
Available names: everything in `sympy` (sqrt, Rational, Integer, expand, factor, solve, simplify, ...),
symbols a b c k m n p q t x y, and rnd(expr, dp) for rounding to dp decimal places.
The string is evaluated with no Python builtins except abs/len/max/min/sorted/round/range.

numeric  The verify result (number, tuple, or list of solutions) must equal `answer`.
         Lists are compared as multisets when the question is `unordered`, otherwise in order.
choice   Every choice text is converted to SymPy (Unicode maths: x², √5, ±, −). Exactly one choice
         must equal the verify result, and it must be the keyed answer. Comparison mode follows the
         result: a number (value), an expression in x etc. (algebraic identity), or a list of
         solutions (set, choices written as "x = 2 ± √3" or "x = 1 and x = 5").
Questions without `verify` count as `unverifiable` and need the blind second pass.
A verify that is only a literal (e.g. "5" or "(3, 7)") is reported as `restated`: it checks the
answer's format, not its mathematics.

Run:  python3 scripts/verify_questions.py   (needs sympy: pip install sympy)
"""
import ast
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from qlib import to_sympy_text, split_solutions  # noqa: E402

try:
    import sympy as sp
    from sympy.parsing.sympy_parser import (parse_expr, standard_transformations,
                                            implicit_multiplication_application, convert_xor)
except ImportError:
    print("verify_questions: sympy is not installed (pip install sympy); skipping.")
    sys.exit(2)

TRANSFORMS = standard_transformations + (implicit_multiplication_application, convert_xor)
SYMS = {n: sp.Symbol(n) for n in "a b c k m n p q t x y".split()}


def rnd(expr, dp):
    return sp.Rational(str(round(float(sp.N(expr, 30)), dp)))


NS = {k: getattr(sp, k) for k in dir(sp) if not k.startswith("_")}
NS.update(SYMS)
NS.update({"rnd": rnd, "abs": abs, "len": len, "max": max, "min": min, "sorted": sorted, "round": round,
           "range": range, "__builtins__": {}})


def evaluate(src):
    return eval(compile(src, "<verify>", "eval"), dict(NS))


def is_literal(src):
    try:
        ast.literal_eval(src)
        return True
    except (ValueError, SyntaxError):
        return False


def parse_math(text):
    return parse_expr(to_sympy_text(text), local_dict=dict(SYMS), transformations=TRANSFORMS)


def same(a, b):
    try:
        d = sp.simplify(sp.nsimplify(a) - sp.nsimplify(b)) if not (getattr(a, "free_symbols", None) or getattr(b, "free_symbols", None)) \
            else sp.simplify(sp.expand(a - b))
        return d == 0
    except Exception:
        return False


def as_list(v):
    if isinstance(v, dict):
        return None
    if isinstance(v, (list, tuple, set, sp.FiniteSet)):
        return [sp.sympify(x) for x in v]
    return None


def multiset_equal(xs, ys, ordered):
    if len(xs) != len(ys):
        return False
    if ordered:
        return all(same(a, b) for a, b in zip(xs, ys))
    left = list(ys)
    for a in xs:
        hit = next((i for i, b in enumerate(left) if same(a, b)), None)
        if hit is None:
            return False
        left.pop(hit)
    return True


def parse_numeric_answer(ans):
    a = ans.strip().replace("−", "-")
    if a.startswith("(") and a.endswith(")"):
        return "tuple", [sp.Rational(p.strip()) for p in a[1:-1].split(",")]
    parts = [re.sub(r"^[a-z]\s*=\s*", "", p.strip()) for p in a.split(",")]
    vals = [sp.Rational(p) for p in parts]
    return ("list" if len(vals) > 1 else "single"), vals


def check_numeric(q, result):
    kind, vals = parse_numeric_answer(q["answer"])
    lst = as_list(result)
    if kind == "single":
        if lst is not None:
            return len(lst) == 1 and same(lst[0], vals[0]), "verify gave %s" % (lst,)
        return same(sp.sympify(result), vals[0]), "verify gave %s" % (result,)
    if lst is None:
        return False, "answer has several values but verify gave %s" % (result,)
    ordered = kind == "tuple" or not q.get("unordered")
    return multiset_equal(lst, vals, ordered), "verify gave %s" % (lst,)


def choice_value(text, mode):
    if mode == "set":
        sols = split_solutions(text)
        return None if sols is None else [parse_math(s) for s in sols]
    if mode == "expr":
        text = re.sub(r"^(?:y|f\(x\))\s*=\s*", "", text.strip())  # "y = (x − 2)²" -> right-hand side
    return parse_math(text)


def check_choice(q, result):
    lst = as_list(result)
    if lst is not None:
        mode, target = "set", lst
    else:
        target = sp.sympify(result)
        mode = "expr" if target.free_symbols else "value"
    matches, unparsed = [], []
    for c in q["choices"]:
        try:
            v = choice_value(c["text"], mode)
        except Exception:
            v = None
        if v is None:
            unparsed.append(c["key"])
            continue
        ok = multiset_equal(v, target, False) if mode == "set" else same(v, target)
        if ok:
            matches.append(c["key"])
    if matches == [q["answer"]]:
        return True, "mode=%s" % mode
    return False, "mode=%s matches=%s keyed=%s unparsed=%s" % (mode, matches, q["answer"], unparsed)


def main():
    with open(os.path.join(ROOT, "data", "questions.json"), encoding="utf-8") as f:
        questions = json.load(f)
    report = {"auto_verified": [], "restated": [], "mismatch": [], "unverifiable": [], "error": []}
    for q in questions:
        src = q.get("verify")
        if not src:
            report["unverifiable"].append(q["id"])
            continue
        try:
            result = evaluate(src)
            ok, note = (check_numeric if q["type"] == "numeric" else check_choice)(q, result)
        except Exception as e:  # noqa: BLE001
            report["error"].append({"id": q["id"], "error": "%s: %s" % (type(e).__name__, e)})
            continue
        if not ok:
            report["mismatch"].append({"id": q["id"], "note": note})
        elif is_literal(src):
            report["restated"].append(q["id"])
        else:
            report["auto_verified"].append(q["id"])
    summary = {k: len(v) for k, v in report.items()}
    summary["total"] = len(questions)
    out = {"summary": summary, **report}
    with open(os.path.join(ROOT, "data", "verification_report.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print("verify:", summary)
    for m in report["mismatch"]:
        print("MISMATCH", m["id"], m["note"])
    for m in report["error"]:
        print("ERROR   ", m["id"], m["error"])
    return 1 if report["mismatch"] or report["error"] else 0


if __name__ == "__main__":
    sys.exit(main())
