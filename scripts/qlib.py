"""Shared helpers for content scripts and the verifier.

Content scripts describe topics with `topic(...)` and questions with `num(...)`
and `mc(...)`. Maths in prompts and choices is plain Unicode
(x², √5, −3, ±, 3/4); `to_sympy()` converts it for machine checking.
"""
import re

BANDS = ["y9", "y10", "y10opt", "general", "methods", "specialist"]
SENIOR = {"general", "methods", "specialist"}
BAND_LABEL = {"y9": "Year 9", "y10": "Year 10", "y10opt": "Year 10 Optional",
              "general": "General", "methods": "Methods", "specialist": "Specialist"}


def level_of(band, unit=None):
    if band == "y9":
        return 9
    if band in ("y10", "y10opt"):
        return 10
    return 11 if unit in (1, 2) else 12


def rank_of(band, unit=None):
    """Ordering used for 'a prerequisite may not come later than its topic'."""
    if band == "y9":
        return 0
    if band == "y10":
        return 1
    if band == "y10opt":
        return 2
    return 2 + int(unit)  # U1 -> 3 ... U4 -> 6


# ---------------------------------------------------------------- authoring

def topic(id, name, band, group, type, desc, mastery, standards, pre=(), qs=(), unit=None,
          tech="free", root_reason=None):
    """group: strand for Years 9-10 ('Algebra'), or 'T1 Surds and quadratic functions' for senior."""
    if band in SENIOR:
        chapter = "%s U%d · %s" % (BAND_LABEL[band], unit, group)
        strand = None
    else:
        chapter = "%s · %s" % (BAND_LABEL[band], group)
        strand = group
    t = {
        "id": id, "name": name, "band": band, "level": level_of(band, unit),
        "chapter": chapter, "type": type, "description": desc, "mastery_criteria": list(mastery),
        "standards": [{"id": s, "confidence": c} for s, c in standards],
        "tech": tech, "status": "draft",
    }
    if unit is not None:
        t["unit"] = unit
    if strand:
        t["strand"] = strand
    if root_reason:
        t["root_reason"] = root_reason
    deps = [{"topicId": id, "prerequisiteId": p, "strength": s, "reason": r} for p, s, r in pre]
    questions = []
    for i, q in enumerate(qs, 1):
        q = dict(q)
        q["id"] = "%s_q%d" % (id, i)
        q["topicId"] = id
        questions.append(q)
    return t, deps, questions


def num(prompt, answer, verify=None, diff="basic", expl="", unordered=False, tech=None):
    q = {"difficulty": diff, "type": "numeric", "prompt": prompt, "answer": str(answer), "explanation": expl}
    if verify is not None:
        q["verify"] = verify
    if unordered:
        q["unordered"] = True
    if tech:
        q["tech"] = tech
    return q


def mc(prompt, choices, correct, verify=None, diff="basic", expl="", tech=None):
    """choices: list of strings; correct: 0-based index of the right one."""
    keys = "ABCD"
    q = {"difficulty": diff, "type": "choice", "prompt": prompt,
         "choices": [{"key": keys[i], "text": c} for i, c in enumerate(choices)],
         "answer": keys[correct], "explanation": expl}
    if verify is not None:
        q["verify"] = verify
    if tech:
        q["tech"] = tech
    return q


# ---------------------------------------------------------------- Unicode maths -> sympy text

SUP = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹⁻", "0123456789-")
SUP_RE = re.compile(r"[⁰¹²³⁴⁵⁶⁷⁸⁹⁻]+")


def to_sympy_text(s):
    s = s.strip()
    s = s.replace("−", "-").replace("–", "-").replace("×", "*").replace("÷", "/").replace("π", "pi")
    s = SUP_RE.sub(lambda m: "**(" + m.group(0).translate(SUP) + ")", s)
    s = re.sub(r"√\(", "sqrt(", s)
    s = re.sub(r"√(\d+|[a-z])", r"sqrt(\1)", s)
    return s


def split_solutions(s):
    """'x = 2 or x = −3' / 'x = −1 ± √3' / 'x = 1 and x = 5' -> list of expression texts, or None."""
    t = s.strip()
    if not re.match(r"^[a-z]\s*=", t):
        return None
    parts = re.split(r"\s+(?:or|and)\s+|,\s*", t)
    out = []
    for p in parts:
        p = re.sub(r"^[a-z]\s*=\s*", "", p.strip())
        if "±" in p:
            out.append(p.replace("±", "+", 1))
            out.append(p.replace("±", "-", 1))
        else:
            out.append(p)
    return out
