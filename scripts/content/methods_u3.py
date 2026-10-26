"""Mathematical Methods Unit 3 (Year 12): Further calculus and introduction to statistics.

AI-drafted from the QCAA Mathematical Methods 2025 syllabus. Not reviewed by a teacher.
"""
from qlib import topic, num, mc

T1 = "T1 Differentiation of exponential and logarithmic functions"
T2 = "T2 Differentiation of trigonometric functions and differentiation rules"
T3 = "T3 Further applications of differentiation"
T4 = "T4 Introduction to integration"
T5 = "T5 Discrete random variables"


def S(t, s):
    return [("qcaa25:MM.U3.T%d.S%d" % (t, s), "exact")]


T = []

# ------------------------------------------------------------------ T1

T.append(topic(
    "qm_m3_001", "The number e and the derivative of eˣ", "methods", T1, "procedural",
    "Recognise e as the base for which d/dx(eˣ) = eˣ, and differentiate e^(f(x)) with the chain rule.",
    ["Knows d/dx(eˣ) = eˣ", "Differentiates e^(kx) and e^(f(x))", "Evaluates derivatives at a point"],
    S(1, 1), unit=3,
    pre=[("qm_m2_019", "hard", "Chain rule for e^(f(x))"), ("qm_m2_003", "hard", "Exponential graphs")], qs=[
        mc("d/dx e^(3x) =", ["e^(3x)", "3e^(3x)", "3xe^(3x − 1)", "e^(3x)/3"], 1, "diff(exp(3*x), x)", expl="Chain rule: e^(3x) × 3."),
        mc("d/dx (5eˣ − x²) =", ["5e^x − 2x", "5e^x − x", "e^x − 2x", "5xe^(x − 1) − 2x"], 0, "diff(5*exp(x) - x**2, x)",
           expl="d/dx eˣ = eˣ, so 5eˣ − 2x."),
        num("f(x) = e^(2x). Find f′(0).", "2", "diff(exp(2*x), x).subs(x, 0)", "standard", "f′(x) = 2e^(2x), and e⁰ = 1."),
        mc("d/dx e^(x²) =", ["e^(2x)", "x²e^(x² − 1)", "2xe^(x²)", "2e^(x²)"], 2, "diff(exp(x**2), x)", "standard", "Chain rule: e^(x²) × 2x."),
    ]))

T.append(topic(
    "qm_m3_002", "Natural logarithms and equations with base e", "methods", T1, "procedural",
    "Use ln x as the inverse of eˣ and solve equations with base e.",
    ["Uses ln(eˣ) = x and e^(ln x) = x", "Solves eˣ = k and ln(f(x)) = k", "Solves quadratic-type equations in eˣ"],
    S(1, 2), unit=3,
    pre=[("qm_m2_006", "hard", "Logarithm laws"), ("qm_m3_001", "soft", "The number e")], qs=[
        num("Simplify ln(e⁵).", "5", "log(exp(5))", "basic", "ln and e cancel."),
        mc("Solve eˣ = 7.", ["x = 7/e", "x = ln 7", "x = e^7", "x = log₇ e"], 1, "solve(exp(x) - 7, x)", expl="Take ln of both sides."),
        num("Solve ln(2x − 1) = 0.", "1", "solve(log(2*x - 1), x)", "standard", "2x − 1 = e⁰ = 1."),
        mc("Solve e^(2x) − 5eˣ + 6 = 0.", ["x = 2, 3", "x = ln 2, ln 3", "x = ln 5, ln 6", "x = e^2, e^3"], 1,
           "[r for r in solve(exp(2*x) - 5*exp(x) + 6, x) if r.is_real]", "standard", "Let u = eˣ: (u − 2)(u − 3) = 0."),
    ]))

T.append(topic(
    "qm_m3_003", "The derivative of ln x", "methods", T1, "procedural",
    "Use d/dx(ln x) = 1/x and d/dx ln(f(x)) = f′(x)/f(x).",
    ["Differentiates ln x", "Differentiates ln(f(x)) with the chain rule", "Uses log laws to simplify before differentiating"],
    S(1, 2), unit=3,
    pre=[("qm_m3_002", "hard", "Natural logarithms"), ("qm_m2_019", "hard", "Chain rule")], qs=[
        mc("d/dx ln(x) =", ["ln(x)/x", "1/x", "e^x", "x"], 1, "diff(log(x), x)", expl="A standard result."),
        mc("d/dx ln(3x + 2) =", ["1/(3x + 2)", "3/x", "3/(3x + 2)", "ln(3)/(3x + 2)"], 2, "diff(log(3*x + 2), x)", expl="f′/f = 3/(3x + 2)."),
        mc("d/dx ln(x² + 1) =", ["1/(x² + 1)", "2x/(x² + 1)", "2x ln(x² + 1)", "2/x"], 1, "diff(log(x**2 + 1), x)", "standard", "f′/f = 2x/(x² + 1)."),
        num("f(x) = ln(5x). Find f′(2).", "1/2", "diff(log(5*x), x).subs(x, 2)", "standard", "ln(5x) = ln 5 + ln x, so f′(x) = 1/x."),
    ]))

T.append(topic(
    "qm_m3_004", "Applications of exponential and logarithmic derivatives", "methods", T1, "application",
    "Use derivatives of exponential and logarithmic functions for rates of change and stationary points in models.",
    ["Finds rates of change in growth and decay models", "Finds stationary points of exponential and log functions"],
    S(1, 2), unit=3, tech="either",
    pre=[("qm_m3_001", "hard", "Derivatives of exponentials"), ("qm_m3_003", "soft", "Derivatives of logs"), ("qm_m2_005", "soft", "Exponential models")], qs=[
        num("P(t) = 100e^(0.2t). Find the rate of growth at t = 0.", "20", "diff(100*exp(t/5), t).subs(t, 0)", "basic", "P′(t) = 20e^(0.2t), so 20."),
        num("P(t) = 100e^(0.2t). Find the rate of growth at t = 5, to 1 decimal place.", "54.4", "rnd(diff(100*exp(t/5), t).subs(t, 5), 1)", "basic",
            "20e ≈ 54.4.", tech="active"),
        num("Find the x-coordinate of the stationary point of y = x − ln x, x > 0.", "1", "solve(diff(x - log(x), x), x)", "standard", "1 − 1/x = 0."),
        num("Find the x-coordinate of the stationary point of y = xe^(−x).", "1", "solve(diff(x*exp(-x), x), x)", "standard",
            "e^(−x)(1 − x) = 0."),
    ]))

# ------------------------------------------------------------------ T2

T.append(topic(
    "qm_m3_005", "Derivatives of sine, cosine and tangent", "methods", T2, "procedural",
    "Use d/dx sin x = cos x, d/dx cos x = −sin x and d/dx tan x = 1/cos²x (x in radians).",
    ["Recalls the three derivatives", "Differentiates sums with trig terms", "Uses radians"],
    S(2, 1), unit=3,
    pre=[("qm_m1_021", "hard", "Graphs of sin, cos and tan"), ("qm_m2_014", "soft", "Term-by-term differentiation")], qs=[
        mc("d/dx sin(x) =", ["−cos(x)", "cos(x)", "sin(x)", "−sin(x)"], 1, "diff(sin(x), x)", expl="A standard result."),
        mc("d/dx cos(x) =", ["sin(x)", "cos(x)", "−sin(x)", "−cos(x)"], 2, "diff(cos(x), x)", expl="A standard result; note the minus sign."),
        mc("d/dx tan(x) =", ["1/sin(x)^2", "1/cos(x)^2", "−1/cos(x)^2", "cos(x)^2"], 1, "diff(tan(x), x)", "standard", "d/dx tan x = sec²x = 1/cos²x."),
        num("f(x) = 3 sin x + 2 cos x. Find f′(0).", "3", "diff(3*sin(x) + 2*cos(x), x).subs(x, 0)", "standard", "f′(x) = 3 cos x − 2 sin x."),
    ]))

T.append(topic(
    "qm_m3_006", "Differentiation rules with exponential, log and trig functions", "methods", T2, "procedural",
    "Apply the chain, product and quotient rules to functions involving eˣ, ln x, sin x, cos x and tan x.",
    ["Uses the chain rule with trig and exponential functions", "Uses product and quotient rules", "Gives answers in factorised form"],
    S(2, 2), unit=3,
    pre=[("qm_m3_005", "hard", "Trig derivatives"), ("qm_m3_001", "hard", "Exponential derivatives"), ("qm_m3_003", "hard", "Log derivatives"),
         ("qm_m2_022", "hard", "Combining rules")], qs=[
        mc("d/dx sin(3x) =", ["cos(3x)", "−3cos(3x)", "3cos(3x)", "3sin(3x)"], 2, "diff(sin(3*x), x)", expl="cos(3x) × 3."),
        mc("d/dx (xeˣ) =", ["e^x", "(x + 1)e^x", "xe^x", "(x − 1)e^x"], 1, "diff(x*exp(x), x)", expl="Product rule: eˣ + xeˣ."),
        mc("d/dx (ln(x)/x) =", ["(ln(x) − 1)/x^2", "1/x^2", "(1 − ln(x))/x^2", "−ln(x)/x^2"], 2, "diff(log(x)/x, x)", "standard",
           "((1/x)x − ln x)/x² = (1 − ln x)/x²."),
        mc("d/dx (e^(2x) cos(x)) =", ["e^(2x)(2cos(x) + sin(x))", "e^(2x)(2cos(x) − sin(x))", "−2e^(2x)sin(x)", "2e^(2x)cos(x)"], 1,
           "diff(exp(2*x)*cos(x), x)", "standard", "2e^(2x) cos x − e^(2x) sin x."),
    ]))

T.append(topic(
    "qm_m3_007", "Applications of trigonometric derivatives", "methods", T2, "application",
    "Use derivatives of trigonometric functions for gradients, tangents, rates of change and stationary points.",
    ["Finds gradients and tangents to trig curves", "Interprets rates of change in periodic models", "Finds stationary points on an interval"],
    S(2, 1), unit=3,
    pre=[("qm_m3_005", "hard", "Trig derivatives"), ("qm_m1_024", "soft", "Trigonometric models")], qs=[
        num("Find the gradient of y = sin x at x = 0.", "1", "diff(sin(x), x).subs(x, 0)", "basic", "cos 0 = 1."),
        mc("The water depth is d(t) = 3 sin(πt/6) + 5 m. At what rate is it changing at t = 0, in metres per hour?", ["3", "π/2", "π/6", "3π"], 1,
           "diff(3*sin(pi*t/6) + 5, t).subs(t, 0)", expl="d′(t) = 3 × (π/6) cos(πt/6) = (π/2) cos(πt/6)."),
        mc("Find the equation of the tangent to y = cos x at x = π/2.", ["y = x − π/2", "y = −x + π/2", "y = −x", "y = −x + π"], 1,
           "-(x - pi/2)", "standard", "Gradient −sin(π/2) = −1 through (π/2, 0)."),
        mc("Find the x-values of the stationary points of y = x + 2 cos x for 0 < x < π.", ["x = π/3, 2π/3", "x = π/6", "x = π/6, 5π/6", "x = π/2"], 2,
           "solveset(1 - 2*sin(x), x, Interval.open(0, pi))", "standard", "1 − 2 sin x = 0, so sin x = 1/2."),
    ]))

# ------------------------------------------------------------------ T3

T.append(topic(
    "qm_m3_008", "The second derivative and acceleration", "methods", T3, "procedural",
    "Find second derivatives and interpret acceleration as the second derivative of displacement.",
    ["Differentiates twice", "Finds acceleration from displacement", "Interprets the sign of acceleration"],
    S(3, 1), unit=3,
    pre=[("qm_m2_016", "hard", "Velocity from displacement"), ("qm_m3_006", "soft", "Differentiating a range of functions")], qs=[
        mc("f(x) = x⁴ − 3x². Find f″(x).", ["4x³ − 6x", "12x² − 6", "12x²", "12x − 6"], 1, "diff(x**4 - 3*x**2, x, 2)", expl="f′ = 4x³ − 6x, then f″ = 12x² − 6."),
        num("x(t) = t³ − 6t² + 9t metres. Find the acceleration at t = 1, in m/s².", "-6", "diff(t**3 - 6*t**2 + 9*t, t, 2).subs(t, 1)", "basic",
            "x″(t) = 6t − 12."),
        mc("y = e^(2x). Find y″.", ["2e^(2x)", "4e^(2x)", "e^(2x)", "4xe^(2x)"], 1, "diff(exp(2*x), x, 2)", "standard", "Each derivative brings down a 2."),
        num("x(t) = t³ − 6t² + 9t metres. When is the acceleration zero?", "2", "solve(diff(t**3 - 6*t**2 + 9*t, t, 2), t)", "standard", "6t − 12 = 0."),
    ]))

T.append(topic(
    "qm_m3_009", "Concavity and points of inflection", "methods", T3, "conceptual",
    "Link the sign of f″ to concavity and find points of inflection where the concavity changes.",
    ["Uses f″ > 0 for concave up and f″ < 0 for concave down", "Finds points of inflection and checks for a sign change"],
    S(3, 1), unit=3,
    pre=[("qm_m3_008", "hard", "Needs the second derivative")], qs=[
        num("Find the x-coordinate of the point of inflection of y = x³ − 6x².", "2", "solve(diff(x**3 - 6*x**2, x, 2), x)", "basic", "6x − 12 = 0."),
        mc("If f″(x) > 0 on an interval, then f is:", ["concave down", "concave up", "increasing", "decreasing"], 1, expl="Gradient is increasing."),
        mc("On which interval is y = x³ − 6x² concave down?", ["x > 2", "x < 2", "x < 0", "0 < x < 4"], 1, diff="standard", expl="f″ = 6x − 12 < 0 when x < 2."),
        num("Find the x-coordinates of the points of inflection of y = x⁴ − 6x².", "1, -1", "solve(diff(x**4 - 6*x**2, x, 2), x)", "standard",
            "12x² − 12 = 0, and f″ changes sign at each.", unordered=True),
    ]))

T.append(topic(
    "qm_m3_010", "The second derivative test and curve sketching", "methods", T3, "procedural",
    "Classify stationary points with the second derivative and sketch curves showing stationary points and inflections.",
    ["Applies the second derivative test", "Knows when the test is inconclusive", "Combines features in a sketch"],
    S(3, 1), unit=3,
    pre=[("qm_m3_009", "hard", "Concavity"), ("qm_m2_018", "hard", "Curve sketching with stationary points")], qs=[
        mc("At a stationary point x = a, f″(a) = −4. The point is a:", ["local minimum", "local maximum", "point of inflection", "cannot tell"], 1,
           expl="Concave down at a stationary point gives a maximum."),
        num("Find the x-coordinate of the local minimum of y = x³ − 12x.", "2",
            "[r for r in solve(diff(x**3 - 12*x, x), x) if diff(x**3 - 12*x, x, 2).subs(x, r) > 0]", "basic", "x = ±2; f″(2) = 12 > 0."),
        num("Find the local maximum value of y = x³ − 12x.", "16", "(x**3 - 12*x).subs(x, -2)", "standard", "At x = −2: −8 + 24 = 16."),
        mc("For f(x) = x⁴, f′(0) = 0 and f″(0) = 0. At x = 0 there is:",
           ["a local minimum (the test is inconclusive, so check the sign of f′)", "a point of inflection", "a local maximum", "no stationary point"], 0,
           diff="standard", expl="f′ changes from negative to positive, so it is a minimum."),
    ]))

T.append(topic(
    "qm_m3_011", "Optimisation", "methods", T3, "application",
    "Develop a function from a description and use derivatives to find maximum or minimum values, checking endpoints.",
    ["Writes the quantity to optimise in one variable", "Finds and justifies the optimum", "Answers in context"],
    S(3, 1), unit=3,
    pre=[("qm_m2_017", "hard", "Stationary points"), ("qm_m3_010", "soft", "Justifying with the second derivative"), ("qm_m1_007", "soft", "Quadratic max/min models")], qs=[
        num("Profit is P(x) = −2x² + 80x − 300. What value of x gives maximum profit?", "20", "solve(diff(-2*x**2 + 80*x - 300, x), x)", "basic",
            "P′ = −4x + 80 = 0."),
        num("A rectangle has a perimeter of 40 cm. What is its largest possible area, in cm²?", "100", "maximum(x*(20 - x), x, Interval(0, 20))", "basic",
            "A = x(20 − x) is greatest at x = 10."),
        mc("What is the maximum value of y = xe^(−x) for x ≥ 0?", ["e", "1/e", "1", "0"], 1, "maximum(x*exp(-x), x, Interval(0, oo))", "standard",
           "At x = 1, y = e⁻¹."),
        num("An open box is made from a 12 cm × 12 cm sheet by cutting x cm squares from the corners: V = x(12 − 2x)². Find x for maximum volume.", "2",
            "[r for r in solve(diff(x*(12 - 2*x)**2, x), x) if 0 < r < 6]", "standard", "V′ = (12 − 2x)(12 − 6x) = 0 gives x = 2 in the domain."),
    ]))

# ------------------------------------------------------------------ T4

T.append(topic(
    "qm_m3_012", "Anti-derivatives and the power rule", "methods", T4, "procedural",
    "Find indefinite integrals of powers of x, including negative and fractional powers, with a constant of integration.",
    ["Uses ∫xⁿ dx = xⁿ⁺¹/(n + 1) + c", "Rewrites roots and fractions as powers", "Includes + c"],
    S(4, 1), unit=3,
    pre=[("qm_m2_014", "hard", "Anti-differentiation reverses the power rule")], qs=[
        mc("∫ x³ dx =", ["3x² + c", "x⁴/4 + c", "x⁴ + c", "4x⁴ + c"], 1, "integrate(x**3, x) + c", expl="Add 1 to the power and divide by it."),
        mc("∫ (6x² − 4x + 1) dx =", ["2x³ − 2x² + x + c", "12x − 4 + c", "6x³ − 4x² + x + c", "2x³ − 4x² + x + c"], 0,
           "integrate(6*x**2 - 4*x + 1, x) + c", expl="Integrate term by term."),
        mc("∫ √x dx =", ["(1/2)x^(−1/2) + c", "(2/3)x^(3/2) + c", "(3/2)x^(3/2) + c", "x^(3/2) + c"], 1, "integrate(sqrt(x), x) + c", "standard",
           "x^(1/2) integrates to x^(3/2) ÷ 3/2."),
        mc("∫ 1/x³ dx =", ["−3/x⁴ + c", "1/(2x²) + c", "−1/(2x²) + c", "ln(x³) + c"], 2, "integrate(x**-3, x) + c", "standard",
           "x⁻³ integrates to x⁻²/(−2)."),
    ]))

T.append(topic(
    "qm_m3_013", "Integrals of eˣ, 1/x, sin x and cos x", "methods", T4, "procedural",
    "Use the standard indefinite integrals of eˣ, 1/x, sin x and cos x.",
    ["Recalls the standard integrals", "Combines them with constant multiples and sums"],
    S(4, 1), unit=3,
    pre=[("qm_m3_012", "hard", "Indefinite integrals"), ("qm_m3_001", "hard", "Derivative of eˣ"), ("qm_m3_003", "hard", "Derivative of ln x"),
         ("qm_m3_005", "hard", "Derivatives of sin and cos")], qs=[
        mc("∫ eˣ dx =", ["xe^(x − 1) + c", "e^x + c", "e^(x + 1)/(x + 1) + c", "ln(x) + c"], 1, "integrate(exp(x), x) + c", expl="eˣ is its own derivative."),
        mc("∫ cos(x) dx =", ["−sin(x) + c", "cos(x) + c", "sin(x) + c", "−cos(x) + c"], 2, "integrate(cos(x), x) + c", expl="d/dx sin x = cos x."),
        mc("∫ (2/x + sin(x)) dx, for x > 0, =", ["2ln(x) + cos(x) + c", "2ln(x) − cos(x) + c", "−2/x² − cos(x) + c", "2ln(x) + sin(x) + c"], 1,
           "integrate(2/x + sin(x), x) + c", "standard", "∫ 1/x dx = ln x and ∫ sin x dx = −cos x."),
        mc("∫ (3eˣ − 4cos(x)) dx =", ["3e^x + 4sin(x) + c", "3e^x − 4cos(x) + c", "3xe^x − 4sin(x) + c", "3e^x − 4sin(x) + c"], 3,
           "integrate(3*exp(x) - 4*cos(x), x) + c", "standard", "Term by term."),
    ]))

T.append(topic(
    "qm_m3_014", "Integrals of linear composites", "methods", T4, "procedural",
    "Integrate f(ax + b) for powers, eˣ, 1/x, sin and cos by dividing by a.",
    ["Recognises the linear inner function", "Divides by the coefficient of x"],
    S(4, 1), unit=3,
    pre=[("qm_m3_013", "hard", "Standard integrals"), ("qm_m2_019", "soft", "Reverses the chain rule")], qs=[
        mc("∫ e^(2x) dx =", ["2e^(2x) + c", "e^(2x)/2 + c", "e^(2x) + c", "e^(2x + 1)/(2x + 1) + c"], 1, "integrate(exp(2*x), x) + c",
           expl="Divide by the coefficient 2."),
        mc("∫ (3x + 1)⁴ dx =", ["(3x + 1)⁵/5 + c", "12(3x + 1)³ + c", "(3x + 1)⁵/15 + c", "(3x + 1)⁵/3 + c"], 2, "integrate((3*x + 1)**4, x) + c",
           expl="(3x + 1)⁵/5, divided by 3."),
        mc("∫ cos(3x) dx =", ["3sin(3x) + c", "sin(3x)/3 + c", "−sin(3x)/3 + c", "sin(3x) + c"], 1, "integrate(cos(3*x), x) + c", "standard",
           "Divide by 3."),
        mc("∫ 1/(2x + 1) dx, for x > −1/2, =", ["ln(2x + 1) + c", "2ln(2x + 1) + c", "ln(2x + 1)/2 + c", "−1/(2x + 1)² + c"], 2,
           "integrate(1/(2*x + 1), x) + c", "standard", "ln(2x + 1), divided by 2."),
    ]))

T.append(topic(
    "qm_m3_015", "Finding a function from its derivative", "methods", T4, "procedural",
    "Determine f(x) from f′(x) and a known value, by integrating and solving for the constant.",
    ["Integrates f′(x)", "Uses the given point to find c", "Evaluates the resulting function"],
    S(4, 1), unit=3,
    pre=[("qm_m3_012", "hard", "Indefinite integrals")], qs=[
        num("f′(x) = 2x and f(0) = 3. Find f(2).", "7", "(lambda F: (F + 3 - F.subs(x, 0)).subs(x, 2))(integrate(2*x, x))", "basic",
            "f(x) = x² + 3, so f(2) = 7."),
        num("f′(x) = 3x² − 1 and f(1) = 4. Find f(2).", "10", "(lambda F: (F + 4 - F.subs(x, 1)).subs(x, 2))(integrate(3*x**2 - 1, x))", "basic",
            "f(x) = x³ − x + 4."),
        mc("f′(x) = eˣ and f(0) = 5. Then f(x) =", ["e^x + 5", "e^x + 4", "e^x", "5e^x"], 1, "(lambda F: F + 5 - F.subs(x, 0))(integrate(exp(x), x))",
           "standard", "f(x) = eˣ + c and 1 + c = 5."),
        num("f′(x) = 6x − 4 and f(2) = 1. Find f(0).", "-3", "(lambda F: (F + 1 - F.subs(x, 2)).subs(x, 0))(integrate(6*x - 4, x))", "standard",
            "f(x) = 3x² − 4x + c with 12 − 8 + c = 1, so c = −3."),
    ]))

T.append(topic(
    "qm_m3_016", "Motion: displacement from velocity and acceleration", "methods", T4, "application",
    "Find velocity from acceleration and displacement from velocity using anti-derivatives and initial conditions.",
    ["Integrates acceleration to velocity", "Integrates velocity to displacement", "Uses initial conditions for each constant"],
    S(4, 1), unit=3,
    pre=[("qm_m3_015", "hard", "Uses initial conditions"), ("qm_m3_008", "hard", "Links displacement, velocity and acceleration")], qs=[
        num("v(t) = 4t + 1 m/s and x(0) = 2 m. Find x(3), in metres.", "23", "(lambda X: (X + 2 - X.subs(t, 0)).subs(t, 3))(integrate(4*t + 1, t))", "basic",
            "x(t) = 2t² + t + 2."),
        num("a(t) = 6 m/s² and v(0) = 2 m/s. Find v(4), in m/s.", "26", "2 + integrate(6, (t, 0, 4))", "basic", "v(t) = 6t + 2."),
        num("a(t) = 6t, v(0) = 0 and x(0) = 1. Find x(2).", "9", "1 + integrate(integrate(6*t, (t, 0, t)), (t, 0, 2))", "standard",
            "v = 3t², x = t³ + 1."),
        num("v(t) = 3t² − 12 m/s and x(0) = 0. Find x(2).", "-16", "integrate(3*t**2 - 12, (t, 0, 2))", "standard", "x(t) = t³ − 12t, so 8 − 24."),
    ]))

# ------------------------------------------------------------------ T5 Discrete random variables

DRV = "X takes the values 0, 1, 2 and 3 with probabilities 0.1, 0.3, k and 0.2. "

T.append(topic(
    "qm_m3_017", "Discrete random variables and probability functions", "methods", T5, "conceptual",
    "Describe discrete random variables with probability functions and use them to find probabilities.",
    ["Checks a probability function sums to 1", "Finds unknown probabilities", "Finds P(X ≥ a) and similar"],
    S(5, 1), unit=3,
    pre=[("qm_m1_026", "hard", "Probability rules")], qs=[
        num(DRV + "Find k.", "0.4", "1 - Rational(1, 10) - Rational(3, 10) - Rational(2, 10)", "basic", "1 − 0.6 = 0.4."),
        num(DRV + "Using k = 0.4, find P(X ≥ 2).", "0.6", "Rational(4, 10) + Rational(2, 10)", "basic", "0.4 + 0.2."),
        mc("Which list could be the probabilities of a discrete random variable?", ["0.2, 0.5, 0.3", "0.4, 0.4, 0.4", "0.6, −0.1, 0.5", "0.5, 0.6"], 0,
           diff="standard", expl="Each must be between 0 and 1, and they must sum to 1."),
        num("Two fair coins are tossed and X is the number of heads. Find P(X = 1).", "1/2", "binom_pmf(2, 1, Rational(1, 2))", "standard", "HT or TH: 2/4."),
    ]))

T.append(topic(
    "qm_m3_018", "Expected value", "methods", T5, "procedural",
    "Calculate E(X) = Σ x p(x) and interpret it, including E(aX + b) = aE(X) + b.",
    ["Calculates the mean of a distribution", "Interprets expected value in games and decisions", "Uses linear changes"],
    S(5, 1), unit=3,
    pre=[("qm_m3_017", "hard", "Uses the probability function")], qs=[
        num("X takes 0, 1, 2, 3 with probabilities 0.1, 0.3, 0.4, 0.2. Find E(X).", "1.7",
            "sum([v*Rational(p, 10) for v, p in [(0, 1), (1, 3), (2, 4), (3, 2)]])", "basic", "0 + 0.3 + 0.8 + 0.6 = 1.7."),
        num("Find E(X) for the score on a fair six-sided die.", "3.5", "Rational(sum(range(1, 7)), 6)", "basic", "21/6 = 3.5."),
        num("A game costs $2 to play. You win $10 with probability 0.1, otherwise nothing. Find the expected profit in dollars.", "-1",
            "10*Rational(1, 10) - 2", "standard", "Expected winnings $1, minus the $2 cost."),
        num("E(X) = 3. Find E(2X + 1).", "7", "2*3 + 1", "standard", "2 × 3 + 1."),
    ]))

T.append(topic(
    "qm_m3_019", "Variance and standard deviation of a discrete random variable", "methods", T5, "procedural",
    "Calculate Var(X) = E(X²) − [E(X)]² and the standard deviation, and use Var(aX + b) = a²Var(X).",
    ["Calculates variance from a distribution", "Takes the square root for standard deviation", "Uses Var(aX + b) = a²Var(X)"],
    S(5, 1), unit=3,
    pre=[("qm_m3_018", "hard", "Variance is built from expected values"), ("qm_10o_014", "soft", "Standard deviation of data")], qs=[
        num("X takes 0, 1, 2 with probabilities 0.25, 0.5, 0.25. Find Var(X).", "0.5",
            "(lambda ps: sum(v**2*p for v, p in ps) - sum(v*p for v, p in ps)**2)([(0, Rational(1, 4)), (1, Rational(1, 2)), (2, Rational(1, 4))])",
            "basic", "E(X) = 1, E(X²) = 1.5, so Var = 0.5."),
        num("Var(X) = 4. Find the standard deviation of X.", "2", "sqrt(4)", "basic", "√4 = 2."),
        num("Var(X) = 2. Find Var(3X − 1).", "18", "3**2*2", "standard", "3² × 2; the −1 does not change the spread."),
        num("X takes the values 1 and 3 with probability 0.5 each. Find the standard deviation of X.", "1",
            "sqrt(Rational(1, 2)*(1 - 2)**2 + Rational(1, 2)*(3 - 2)**2)", "standard", "Mean 2, each value is 1 away."),
    ]))

T.append(topic(
    "qm_m3_020", "Bernoulli distributions", "methods", T5, "conceptual",
    "Model a single trial with two outcomes as a Bernoulli random variable with mean p and variance p(1 − p).",
    ["Identifies Bernoulli situations", "Uses E(X) = p and Var(X) = p(1 − p)"],
    S(5, 2), unit=3,
    pre=[("qm_m3_019", "hard", "Mean and variance of a discrete variable")], qs=[
        num("X ~ Bernoulli(0.3). Find E(X).", "0.3", "Rational(3, 10)", "basic", "E(X) = p."),
        num("X ~ Bernoulli(0.3). Find Var(X).", "0.21", "Rational(3, 10)*(1 - Rational(3, 10))", "basic", "0.3 × 0.7."),
        mc("Which can be modelled as a Bernoulli random variable?", ["Whether a single free throw goes in", "The number of heads in 10 tosses",
                                                                     "A student's height", "The time until a bus arrives"], 0,
           diff="standard", expl="One trial with two outcomes."),
        num("A Bernoulli variable has Var(X) = 0.25. Find p.", "0.5", "solve(p*(1 - p) - Rational(1, 4), p)", "standard", "p(1 − p) = 0.25 gives p = 0.5."),
    ]))

T.append(topic(
    "qm_m3_021", "Binomial probabilities", "methods", T5, "procedural",
    "Recognise binomial situations and calculate P(X = r) = ⁿCᵣ pʳ(1 − p)ⁿ⁻ʳ.",
    ["Checks the binomial conditions", "Calculates single binomial probabilities"],
    S(5, 3), unit=3,
    pre=[("qm_m3_020", "hard", "Each trial is Bernoulli"), ("qm_m1_008", "hard", "Combinations count the orderings"),
         ("qm_m1_028", "hard", "Trials are independent")], qs=[
        num("X ~ Bin(4, 0.5). Find P(X = 2).", "3/8", "binom_pmf(4, 2, Rational(1, 2))", "basic", "⁴C₂ × 0.5⁴ = 6/16."),
        num("X ~ Bin(3, 0.2). Find P(X = 0).", "0.512", "binom_pmf(3, 0, Rational(2, 10))", "basic", "0.8³."),
        num("X ~ Bin(5, 0.1). Find the exact value of P(X = 1).", "0.32805", "binom_pmf(5, 1, Rational(1, 10))", "standard", "5 × 0.1 × 0.9⁴."),
        num("A quiz has 4 questions, each with 4 options. A student guesses every answer. Find P(exactly 3 correct).", "3/64",
            "binom_pmf(4, 3, Rational(1, 4))", "standard", "⁴C₃ × (1/4)³ × 3/4 = 12/256."),
    ]))

T.append(topic(
    "qm_m3_022", "Binomial mean, variance and cumulative probabilities", "methods", T5, "procedural",
    "Use E(X) = np and Var(X) = np(1 − p), and find 'at least', 'at most' and 'between' probabilities.",
    ["Calculates mean and variance", "Uses complements for 'at least one'", "Sums probabilities for ranges"],
    S(5, 3), unit=3,
    pre=[("qm_m3_021", "hard", "Single binomial probabilities")], qs=[
        num("X ~ Bin(20, 0.3). Find E(X).", "6", "20*Rational(3, 10)", "basic", "np = 6."),
        num("X ~ Bin(20, 0.3). Find Var(X).", "4.2", "20*Rational(3, 10)*Rational(7, 10)", "basic", "np(1 − p) = 6 × 0.7."),
        num("X ~ Bin(3, 0.4). Find P(X ≥ 1).", "0.784", "1 - binom_pmf(3, 0, Rational(4, 10))", "standard", "1 − 0.6³."),
        num("X ~ Bin(10, 0.5). Find P(X ≤ 2) as a fraction.", "7/128", "sum(binom_pmf(10, r, Rational(1, 2)) for r in range(3))", "standard",
            "(1 + 10 + 45)/1024 = 56/1024."),
    ]))
