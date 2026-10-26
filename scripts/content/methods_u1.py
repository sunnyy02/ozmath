"""Mathematical Methods Unit 1 (Year 11), Topics 2-5. Topic 1 is in pilot_quadratics.py.

AI-drafted from the QCAA Mathematical Methods 2025 syllabus. Not reviewed by a teacher.
"""
from qlib import topic, num, mc

T2 = "T2 Binomial expansion and cubic functions"
T3 = "T3 Functions and relations"
T4 = "T4 Trigonometric functions"
T5 = "T5 Probability"


def S(t, s):
    return [("qcaa25:MM.U1.T%d.S%d" % (t, s), "exact")]


T = []

# ------------------------------------------------------------------ T2 Binomial expansion and cubic functions

T.append(topic(
    "qm_m1_008", "Combinations and Pascal's triangle", "methods", T2, "procedural",
    "Count unordered selections with ⁿCᵣ and link the entries of Pascal's triangle to combinations.",
    ["Evaluates ⁿCᵣ", "Counts selections in context", "Reads combinations from Pascal's triangle"],
    S(2, 1), unit=1,
    pre=[("qm_9_014", "soft", "Systematic listing of outcomes")], qs=[
        num("Evaluate ⁵C₂.", "10", "binomial(5, 2)", "basic", "5 × 4 ÷ 2 = 10."),
        num("How many ways can 3 students be chosen from 7?", "35", "binomial(7, 3)", "basic", "⁷C₃ = 35."),
        num("Evaluate ¹⁰C₇.", "120", "binomial(10, 7)", "standard", "¹⁰C₇ = ¹⁰C₃ = 120."),
        num("A committee of 2 boys and 2 girls is chosen from 5 boys and 4 girls. How many committees are possible?", "60",
            "binomial(5, 2)*binomial(4, 2)", "standard", "⁵C₂ × ⁴C₂ = 10 × 6 = 60."),
    ]))

T.append(topic(
    "qm_m1_009", "The binomial theorem", "methods", T2, "procedural",
    "Expand (a + b)ⁿ with binomial coefficients and find a particular term or coefficient.",
    ["Writes a full expansion for small n", "Finds a specific coefficient", "Handles negative and fractional terms"],
    S(2, 1), unit=1,
    pre=[("qm_m1_008", "hard", "Coefficients are combinations"), ("qm_9_004", "hard", "Expanding products")], qs=[
        mc("Expand (x + 1)³.", ["x³ + 1", "x³ + 3x² + 3x + 1", "x³ + 3x + 1", "x³ + 2x² + 2x + 1"], 1, "expand((x + 1)**3)",
           expl="Coefficients 1, 3, 3, 1 from row 3 of Pascal's triangle."),
        num("Find the coefficient of x² in (x + 2)⁴.", "24", "expand((x + 2)**4).coeff(x, 2)", "basic", "⁴C₂ × 2² = 6 × 4 = 24."),
        num("Find the coefficient of x³ in (2x − 1)⁵.", "80", "expand((2*x - 1)**5).coeff(x, 3)", "standard",
            "⁵C₃ × 2³ × (−1)² = 10 × 8 = 80."),
        num("Find the term independent of x in (x + 3/x)⁴.", "54", "expand((x + 3/x)**4).coeff(x, 0)", "standard",
            "Need x² × (3/x)²: ⁴C₂ × 9 = 54."),
    ]))

T.append(topic(
    "qm_m1_010", "Polynomials: degree, coefficients and expanding cubics", "methods", T2, "procedural",
    "Identify the degree and coefficients of a polynomial and expand cubic polynomials from their factors.",
    ["States degree and leading coefficient", "Expands a product of three linear factors"],
    S(2, 2), unit=1,
    pre=[("qm_9_004", "hard", "Expanding products of brackets")], qs=[
        num("What is the degree of 4x³ − x⁵ + 2?", "5", "degree(4*x**3 - x**5 + 2, x)", "basic", "The highest power is x⁵."),
        mc("Expand (x − 1)(x + 2)(x − 3).", ["x³ − 2x² − 5x + 6", "x³ − 2x² + 5x + 6", "x³ + 2x² − 5x − 6", "x³ − 2x² − 5x − 6"], 0,
           "expand((x - 1)*(x + 2)*(x - 3))", expl="(x − 1)(x + 2) = x² + x − 2, then multiply by (x − 3)."),
        num("What is the leading coefficient of (2x + 1)²(3 − x)?", "-4", "LC(expand((2*x + 1)**2*(3 - x)), x)", "standard",
            "The x³ term is 4x² × (−x) = −4x³."),
        num("Expand (x + 2)³. What is the coefficient of x?", "12", "expand((x + 2)**3).coeff(x, 1)", "standard",
            "(x + 2)³ = x³ + 6x² + 12x + 8."),
    ]))

T.append(topic(
    "qm_m1_011", "Graphs of cubic functions", "methods", T2, "conceptual",
    "Sketch cubic graphs showing intercepts, repeated roots and end behaviour.",
    ["Finds intercepts from factored form", "Describes end behaviour from the leading term", "Recognises a touching point at a repeated root"],
    S(2, 2), unit=1,
    pre=[("qm_m1_010", "hard", "Needs polynomial form and factors"), ("qm_m1_004", "soft", "Same intercept reasoning as quadratics")], qs=[
        mc("Describe the end behaviour of y = −x³ + 4x.",
           ["as x → ∞, y → −∞; as x → −∞, y → ∞", "as x → ∞, y → ∞; as x → −∞, y → −∞",
            "as x → ±∞, y → ∞", "as x → ±∞, y → −∞"], 0, expl="The leading term −x³ dominates."),
        num("Find the x-intercepts of y = (x + 2)(x − 1)(x − 4).", "-2, 1, 4", "solve((x + 2)*(x - 1)*(x - 4), x)", "basic",
            "Each factor gives an intercept.", unordered=True),
        mc("At which x-intercept does y = (x − 3)²(x + 1) touch the x-axis without crossing?", ["x = −1", "x = 3", "x = 1", "x = −3"], 1,
           diff="standard", expl="A squared factor gives a repeated root, where the graph touches the axis."),
        num("Find the y-intercept of y = (x − 2)(x + 3)(2x − 1).", "6", "((x - 2)*(x + 3)*(2*x - 1)).subs(x, 0)", "standard",
            "(−2)(3)(−1) = 6."),
    ]))

T.append(topic(
    "qm_m1_012", "Solving cubic equations", "methods", T2, "procedural",
    "Solve cubic equations that are factorised, have a common factor, or can be factorised with the factor theorem.",
    ["Uses the null factor law on three factors", "Takes out a common factor first", "Finds a first root then factorises"],
    S(2, 2), unit=1,
    pre=[("qm_10o_010", "hard", "Factor theorem to find a first factor"), ("qm_m1_002", "hard", "Solving the remaining quadratic")], qs=[
        num("Solve x(x − 2)(x + 5) = 0.", "0, 2, -5", "solve(x*(x - 2)*(x + 5), x)", "basic", "Each factor equals zero.", unordered=True),
        num("Solve x³ − 9x = 0.", "0, 3, -3", "solve(x**3 - 9*x, x)", "basic", "x(x − 3)(x + 3) = 0.", unordered=True),
        num("Solve x³ − 2x² − 5x + 6 = 0.", "1, -2, 3", "solve(x**3 - 2*x**2 - 5*x + 6, x)", "standard",
            "x = 1 is a root; dividing gives (x − 1)(x² − x − 6) = (x − 1)(x − 3)(x + 2).", unordered=True),
        num("Solve x³ = 8 for real x.", "2", "[r for r in solve(x**3 - 8, x) if r.is_real]", "standard", "The only real cube root of 8 is 2."),
    ]))

BOX = "An open box is made from a 10 cm × 10 cm sheet by cutting x cm squares from each corner, so V = x(10 − 2x)². "

T.append(topic(
    "qm_m1_013", "Cubic models", "methods", T2, "application",
    "Build and use cubic models, choosing a sensible domain and interpreting solutions in context.",
    ["Evaluates a cubic model", "States a practical domain", "Solves model equations and interprets them"],
    S(2, 2), unit=1, tech="either",
    pre=[("qm_m1_011", "hard", "Reading features of the cubic graph"), ("qm_m1_012", "soft", "Solving model equations")], qs=[
        num(BOX + "Find V when x = 2.", "72", "(x*(10 - 2*x)**2).subs(x, 2)", "basic", "2 × 6² = 72 cm³."),
        mc(BOX + "What is a sensible domain for x?", ["0 < x < 5", "0 < x < 10", "x > 0", "−5 < x < 5"], 0,
           expl="x must be positive and 10 − 2x must be positive."),
        num(BOX + "Using technology, find the exact x that gives the largest volume.", "5/3",
            "[r for r in solve(diff(x*(10 - 2*x)**2, x), x) if 0 < r < 5][0]", "standard",
            "V′ = (10 − 2x)(10 − 6x) = 0 gives x = 5/3 in the domain.", tech="active"),
        num("A model is P(t) = t³ − 6t² + 9t + 2. Find all t where P(t) = 2.", "0, 3", "solve(t**3 - 6*t**2 + 9*t, t)", "standard",
            "t(t − 3)² = 0, so t = 0 or t = 3.", unordered=True),
    ]))

# ------------------------------------------------------------------ T3 Functions and relations

T.append(topic(
    "qm_m1_014", "Functions, relations and function notation", "methods", T3, "conceptual",
    "Tell functions from relations with the vertical line test and use f(x) notation.",
    ["Applies the vertical line test", "Evaluates f(a) and solves f(x) = k", "Uses independent and dependent variables"],
    S(3, 1), unit=1,
    pre=[("qm_9_008", "soft", "Familiar graphs give examples of functions")], qs=[
        mc("Which of these is NOT a function?", ["y = x²", "x² + y² = 4", "y = 2x + 1", "y = 1/x"], 1,
           expl="A circle gives two y-values for most x-values."),
        num("f(x) = 3x² − 2. Find f(−2).", "10", "(3*x**2 - 2).subs(x, -2)", "basic", "3 × 4 − 2 = 10."),
        num("f(x) = 2x − 1. Solve f(a) = 9.", "5", "solve(2*a - 1 - 9, a)", "standard", "2a − 1 = 9, so a = 5."),
        mc("The vertical line test checks whether:", ["each x-value has at most one y-value", "each y-value has one x-value",
                                                      "the graph passes through the origin", "the graph is continuous"], 0,
           diff="standard", expl="A function gives exactly one output for each input."),
    ]))

T.append(topic(
    "qm_m1_015", "Domain and range", "methods", T3, "conceptual",
    "State natural and restricted domains and the corresponding ranges, using interval or set notation.",
    ["Finds natural domains (roots, fractions)", "Finds ranges from graphs", "Works with restricted domains"],
    S(3, 1), unit=1,
    pre=[("qm_m1_014", "hard", "Domain and range describe a function's inputs and outputs")], qs=[
        mc("What is the natural domain of f(x) = √(x − 3)?", ["x > 3", "x ≥ 3", "x ≥ 0", "all real x"], 1,
           expl="The expression under the root must be non-negative."),
        mc("What is the range of y = x² + 1?", ["y ≥ 0", "all real y", "y ≥ 1", "y > 1"], 2, expl="x² ≥ 0, so x² + 1 ≥ 1."),
        mc("What is the natural domain of f(x) = 1/(x + 2)?", ["x ≠ −2", "x ≠ 2", "x > −2", "x ≥ −2"], 0, diff="standard",
           expl="The denominator cannot be 0."),
        num("f(x) = 2x + 1 has domain 0 ≤ x ≤ 4. What is the largest value in its range?", "9", "(2*x + 1).subs(x, 4)", "standard",
            "f is increasing, so the maximum is f(4) = 9."),
    ]))

PW = "f(x) = x + 1 when x < 0, and f(x) = x² when x ≥ 0. "

T.append(topic(
    "qm_m1_016", "Piecewise functions", "methods", T3, "procedural",
    "Evaluate, graph and solve with functions defined by different rules on different parts of the domain.",
    ["Chooses the correct rule for an input", "Checks solutions lie in the right piece", "Models charges with piecewise rules"],
    S(3, 1), unit=1,
    pre=[("qm_m1_015", "hard", "Each piece has its own restricted domain")], qs=[
        num(PW + "Find f(−3).", "-2", "-3 + 1", "basic", "−3 < 0, so use x + 1."),
        num(PW + "Find f(3).", "9", "3**2", "basic", "3 ≥ 0, so use x²."),
        num(PW + "Solve f(x) = 4.", "2", "[r for r in solve(x**2 - 4, x) if r >= 0] + [r for r in solve(x + 1 - 4, x) if r < 0]", "standard",
            "x + 1 = 4 gives x = 3, which is not < 0. x² = 4 with x ≥ 0 gives x = 2."),
        num("A phone plan costs $20 for up to 2 GB, then $10 per extra GB. What does 3.5 GB cost, in dollars?", "35",
            "20 + 10*(Rational(7, 2) - 2)", "standard", "20 + 10 × 1.5 = 35."),
    ]))

T.append(topic(
    "qm_m1_017", "Circles", "methods", T3, "procedural",
    "Use (x − h)² + (y − k)² = r² to find centre and radius, including by completing the square.",
    ["Writes the equation from centre and radius", "Reads centre and radius", "Completes the square in x and y"],
    S(3, 2), unit=1,
    pre=[("qm_10o_011", "hard", "Extends circles from Year 10 optional content"), ("qm_m1_014", "soft", "A circle is a relation, not a function")], qs=[
        mc("Which is the equation of the circle with centre (0, 0) and radius 5?", ["x² + y² = 5", "x² + y² = 25", "(x − 5)² + y² = 25", "x² − y² = 25"], 1,
           expl="r² = 25."),
        mc("Find the centre of (x + 3)² + (y − 4)² = 16.", ["(−3, 4)", "(3, −4)", "(−3, −4)", "(3, 4)"], 0, expl="h = −3 and k = 4."),
        num("Find the radius of x² + y² + 8x − 2y + 8 = 0.", "3", "sqrt(16 + 1 - 8)", "standard", "(x + 4)² + (y − 1)² = 16 + 1 − 8 = 9."),
        mc("Does the point (1, 2) lie inside, on or outside the circle x² + y² = 4?", ["inside", "on", "outside"], 2, diff="standard",
           expl="1² + 2² = 5 > 4, so it is outside."),
    ]))

T.append(topic(
    "qm_m1_018", "Reciprocal functions", "methods", T3, "conceptual",
    "Sketch y = a/(x − h) + k showing asymptotes, intercepts and behaviour near the asymptotes.",
    ["Reads asymptotes from the rule", "Finds intercepts", "Describes reflections and dilations"],
    S(3, 3), unit=1,
    pre=[("qm_10o_011", "hard", "Builds on hyperbolas"), ("qm_m1_015", "soft", "Excluded values from the domain")], qs=[
        mc("What are the asymptotes of y = 2/(x − 3) + 1?", ["x = 3 and y = 1", "x = −3 and y = 1", "x = 3 and y = 2", "x = 1 and y = 3"], 0,
           expl="Vertical at x − 3 = 0; horizontal at y = 1."),
        num("Find the y-intercept of y = 2/(x − 3) + 1.", "1/3", "(2/(x - 3) + 1).subs(x, 0)", "basic", "2/(−3) + 1 = 1/3."),
        num("Find the x-intercept of y = 2/(x − 3) + 1.", "1", "solve(2/(x - 3) + 1, x)", "standard", "2/(x − 3) = −1, so x − 3 = −2."),
        mc("The graph of y = −1/x lies in which quadrants?", ["1 and 3", "2 and 4", "1 and 2", "3 and 4"], 1, diff="standard",
           expl="For x > 0, y < 0 (quadrant 4); for x < 0, y > 0 (quadrant 2)."),
    ]))

# ------------------------------------------------------------------ T4 Trigonometric functions

T.append(topic(
    "qm_m1_019", "Radian measure, arc length and sector area", "methods", T4, "procedural",
    "Convert between degrees and radians and use l = rθ and A = ½r²θ.",
    ["Converts degrees and radians", "Calculates arc length", "Calculates sector area"],
    S(4, 1), unit=1,
    pre=[("qm_10o_012", "soft", "Angles on the unit circle")], qs=[
        mc("Write 120° in radians.", ["3π/2", "2π/3", "π/3", "4π/3"], 1, "120*pi/180", expl="120 × π/180 = 2π/3."),
        num("Convert π/4 radians to degrees.", "45", "(pi/4)*180/pi", "basic", "π/4 × 180/π = 45."),
        mc("Find the arc length of a sector with radius 6 and angle π/3.", ["π", "2π", "6π", "π/3"], 1, "6*pi/3", "standard",
           "l = rθ = 6 × π/3 = 2π."),
        mc("Find the area of a sector with radius 4 and angle π/2.", ["8π", "2π", "4π", "16π"], 2, "Rational(1, 2)*4**2*pi/2", "standard",
           "A = ½ × 16 × π/2 = 4π."),
    ]))

T.append(topic(
    "qm_m1_020", "The unit circle in radians and exact values", "methods", T4, "conceptual",
    "Use the unit circle to evaluate sine, cosine and tangent at multiples of π/6 and π/4 in radians.",
    ["Locates angles in radians on the unit circle", "Recalls exact values", "Uses quadrant signs and symmetry"],
    S(4, 2), unit=1,
    pre=[("qm_m1_019", "hard", "Angles are now in radians"), ("qm_10o_012", "hard", "Exact values and quadrant signs")], qs=[
        mc("cos(π/3) =", ["√3/2", "1/2", "√2/2", "0"], 1, "cos(pi/3)", expl="π/3 = 60°, and cos 60° = 1/2."),
        mc("sin(5π/6) =", ["−1/2", "√3/2", "1/2", "−√3/2"], 2, "sin(5*pi/6)", expl="Quadrant 2, related angle π/6, sine positive."),
        mc("tan(4π/3) =", ["−√3", "√3", "1/√3", "−1/√3"], 1, "tan(4*pi/3)", "standard", "Quadrant 3, related angle π/3, tangent positive."),
        mc("cos(7π/4) =", ["−√2/2", "1/2", "√2/2", "−1/2"], 2, "cos(7*pi/4)", "standard", "Quadrant 4, related angle π/4, cosine positive."),
    ]))

T.append(topic(
    "qm_m1_021", "Graphs of sine, cosine and tangent", "methods", T4, "conceptual",
    "Sketch y = sin x, y = cos x and y = tan x over extended domains, showing period, amplitude and asymptotes.",
    ["States period and amplitude", "Sketches each graph", "Locates the asymptotes of tan x"],
    S(4, 2), unit=1,
    pre=[("qm_m1_020", "hard", "Graph values come from the unit circle")], qs=[
        mc("What is the period of y = sin x?", ["π", "2π", "π/2", "4π"], 1, "periodicity(sin(x), x)", expl="sin x repeats every 2π."),
        num("What is the amplitude of y = 3 cos x?", "3", "maximum(3*cos(x), x)", "basic", "The graph goes from −3 to 3."),
        mc("What is the period of y = tan x?", ["2π", "π/2", "π", "4π"], 2, "periodicity(tan(x), x)", "standard", "tan x repeats every π."),
        mc("Where is y = tan x undefined for 0 ≤ x ≤ 2π?", ["x = 0, π, 2π", "x = π/2 and x = 3π/2", "x = π", "x = π/4"], 1, diff="standard",
           expl="tan x = sin x / cos x is undefined where cos x = 0."),
    ]))

T.append(topic(
    "qm_m1_022", "Transformations of trigonometric graphs", "methods", T4, "procedural",
    "Find the amplitude, period, phase shift and vertical shift of y = a sin(b(x − h)) + k and y = a cos(b(x − h)) + k.",
    ["Reads amplitude and vertical shift", "Finds the period 2π/b", "Sketches a transformed graph"],
    S(4, 2), unit=1,
    pre=[("qm_m1_021", "hard", "Transforms the basic graphs"), ("qm_9_010", "soft", "Same transformation ideas as for parabolas")], qs=[
        num("What is the amplitude of y = 4 sin(2x) − 1?", "4", "(maximum(4*sin(2*x) - 1, x) - minimum(4*sin(2*x) - 1, x))/2", "basic",
            "The amplitude is |a| = 4."),
        mc("What is the period of y = sin(3x)?", ["3π", "2π/3", "6π", "π/3"], 1, "periodicity(sin(3*x), x)", expl="2π ÷ 3."),
        num("What is the maximum value of y = 2 cos(x − π/4) + 5?", "7", "maximum(2*cos(x - pi/4) + 5, x)", "standard", "5 + 2 = 7."),
        mc("Which equation has amplitude 2, period π and is shifted up 1?", ["y = 2 sin(x/2) + 1", "y = sin(2x) + 2", "y = 2 sin(2x) + 1", "y = 2 sin(πx) + 1"], 2,
           "2*sin(2*x) + 1", "standard", "Period π needs b = 2; amplitude 2; shift up 1."),
    ]))

T.append(topic(
    "qm_m1_023", "Solving trigonometric equations", "methods", T4, "procedural",
    "Solve equations such as 2 cos x + √3 = 0 over a given domain, including with the identity sin²x + cos²x = 1.",
    ["Finds the related angle", "Uses quadrant signs to find every solution in the domain", "Uses the Pythagorean identity"],
    S(4, 2), unit=1,
    pre=[("qm_m1_020", "hard", "Exact values and quadrant signs"), ("qm_m1_021", "soft", "The graph shows how many solutions there are")], qs=[
        mc("Solve sin x = 1/2 for 0 ≤ x ≤ 2π.", ["x = π/6, 7π/6", "x = π/6, 5π/6", "x = π/3, 2π/3", "x = π/6, 11π/6"], 1,
           "solveset(sin(x) - Rational(1, 2), x, Interval(0, 2*pi))", expl="Sine is positive in quadrants 1 and 2."),
        mc("Solve cos x = 0 for 0 ≤ x ≤ 2π.", ["x = 0, π", "x = π/2, 3π/2", "x = π", "x = π/2"], 1,
           "solveset(cos(x), x, Interval(0, 2*pi))", expl="cos x = 0 at the top and bottom of the unit circle."),
        mc("Solve 2 cos x + √3 = 0 for 0 ≤ x ≤ 2π.", ["x = π/6, 11π/6", "x = 5π/6, 7π/6", "x = 2π/3, 4π/3", "x = 5π/6, 11π/6"], 1,
           "solveset(2*cos(x) + sqrt(3), x, Interval(0, 2*pi))", "standard", "cos x = −√3/2: related angle π/6 in quadrants 2 and 3."),
        mc("Solve sin²x + cos x = 1 for 0 ≤ x ≤ 2π.", ["x = π/2, 3π/2", "x = 0, π, 2π", "x = 0, 2π", "x = 0, π/2, 3π/2, 2π"], 3,
           "solveset(sin(x)**2 + cos(x) - 1, x, Interval(0, 2*pi))", "advanced",
           "Use sin²x = 1 − cos²x: cos x(1 − cos x) = 0, so cos x = 0 or cos x = 1."),
    ]))

TIDE = "The water depth at a jetty is d(t) = 3 sin(πt/6) + 5 metres, t hours after midnight. "

T.append(topic(
    "qm_m1_024", "Trigonometric models", "methods", T4, "application",
    "Model periodic situations such as tides and temperatures with sine and cosine functions and interpret the parameters.",
    ["Interprets amplitude, period and centre line in context", "Evaluates the model", "Solves for times when a value is reached"],
    S(4, 2), unit=1,
    pre=[("qm_m1_022", "hard", "Parameters of transformed graphs"), ("qm_m1_023", "soft", "Finding times means solving trig equations")], qs=[
        num(TIDE + "What is the maximum depth, in metres?", "8", "maximum(3*sin(pi*t/6) + 5, t)", "basic", "5 + 3 = 8 m."),
        num(TIDE + "What is the period, in hours?", "12", "periodicity(3*sin(pi*t/6) + 5, t)", "basic", "2π ÷ (π/6) = 12 hours."),
        num(TIDE + "Find the depth at 1 am, in metres.", "13/2", "(3*sin(pi*t/6) + 5).subs(t, 1)", "standard", "3 × sin(π/6) + 5 = 1.5 + 5 = 6.5 m."),
        num(TIDE + "How many hours after midnight is the depth first 8 m?", "3", "min([s for s in solve(3*sin(pi*t/6) + 5 - 8, t) if s > 0])", "standard",
            "sin(πt/6) = 1 when πt/6 = π/2, so t = 3."),
    ]))

# ------------------------------------------------------------------ T5 Probability

DIE = "A fair die is rolled. A = {even number} and B = {number greater than 3}. "

T.append(topic(
    "qm_m1_025", "Sample spaces, events and set notation", "methods", T5, "conceptual",
    "Describe events as sets of outcomes and use complement, intersection, union and Venn diagrams.",
    ["Lists a sample space", "Uses A′, A ∩ B and A ∪ B", "Recognises mutually exclusive events"],
    S(5, 1), unit=1,
    pre=[("qm_9_015", "hard", "Venn diagrams for 'and' and 'or'")], qs=[
        num(DIE + "How many outcomes are in A ∩ B?", "2", "len({2, 4, 6} & {4, 5, 6})", "basic", "A ∩ B = {4, 6}."),
        mc("A′ means:", ["the complement of A", "A and B", "A or B", "A given B"], 0, expl="A′ is every outcome not in A."),
        num(DIE + "How many outcomes are in A ∪ B?", "4", "len({2, 4, 6} | {4, 5, 6})", "standard", "A ∪ B = {2, 4, 5, 6}."),
        mc("Events A and B are mutually exclusive when:", ["A ∩ B = ∅", "A ∪ B is the whole sample space", "P(A) = P(B)", "P(A ∩ B) = P(A)P(B)"], 0,
           diff="standard", expl="They cannot both happen, so they share no outcomes."),
    ]))

T.append(topic(
    "qm_m1_026", "Rules of probability", "methods", T5, "procedural",
    "Use P(A′) = 1 − P(A) and P(A ∪ B) = P(A) + P(B) − P(A ∩ B).",
    ["Uses the complement rule", "Uses the addition rule", "Simplifies it for mutually exclusive events"],
    S(5, 2), unit=1,
    pre=[("qm_m1_025", "hard", "Rules are stated in set notation")], qs=[
        num("P(A) = 0.3. Find P(A′).", "0.7", "1 - Rational(3, 10)", "basic", "1 − 0.3 = 0.7."),
        num("P(A) = 0.5, P(B) = 0.4 and P(A ∩ B) = 0.2. Find P(A ∪ B).", "0.7", "Rational(5, 10) + Rational(4, 10) - Rational(2, 10)", "basic",
            "0.5 + 0.4 − 0.2 = 0.7."),
        num("A and B are mutually exclusive with P(A) = 0.25 and P(B) = 0.35. Find P(A ∪ B).", "0.6", "Rational(25, 100) + Rational(35, 100)", "standard",
            "P(A ∩ B) = 0, so 0.25 + 0.35."),
        num("P(A ∪ B) = 0.8, P(A) = 0.5 and P(B) = 0.6. Find P(A ∩ B).", "0.3", "Rational(5, 10) + Rational(6, 10) - Rational(8, 10)", "standard",
            "0.5 + 0.6 − 0.8 = 0.3."),
    ]))

T.append(topic(
    "qm_m1_027", "Conditional probability", "methods", T5, "procedural",
    "Use P(A | B) = P(A ∩ B)/P(B), restrict the sample space, and use tree diagrams for multi-stage problems.",
    ["Applies the conditional probability formula", "Restricts the sample space", "Uses the multiplication rule P(A ∩ B) = P(A)P(B | A)"],
    S(5, 2), unit=1,
    pre=[("qm_m1_026", "hard", "Uses the probability rules"), ("qm_10_010", "hard", "Conditional language and two-way tables")], qs=[
        num("P(A ∩ B) = 0.12 and P(B) = 0.4. Find P(A | B).", "0.3", "Rational(12, 100)/Rational(4, 10)", "basic", "0.12 ÷ 0.4 = 0.3."),
        num("Two fair dice are rolled. Given that the sum is 8, find P(both dice are even).", "3/5",
            "Rational(len([1 for i in range(1, 7) for j in range(1, 7) if i + j == 8 and i % 2 == 0 and j % 2 == 0]), len([1 for i in range(1, 7) for j in range(1, 7) if i + j == 8]))",
            "basic", "Sum 8: (2,6), (3,5), (4,4), (5,3), (6,2); three are both even."),
        num("P(A) = 0.6 and P(B | A) = 0.5. Find P(A ∩ B).", "0.3", "Rational(6, 10)*Rational(5, 10)", "standard", "0.6 × 0.5 = 0.3."),
        num("A test is positive for 90% of people with a condition and for 5% of people without it. 2% of people have the condition. Find P(positive).",
            "0.067", "Rational(2, 100)*Rational(9, 10) + Rational(98, 100)*Rational(5, 100)", "standard", "0.02 × 0.9 + 0.98 × 0.05 = 0.067."),
    ]))

T.append(topic(
    "qm_m1_028", "Independent events", "methods", T5, "reasoning",
    "Test for independence with P(A ∩ B) = P(A)P(B) and use the multiplication rule for independent events.",
    ["Tests independence numerically", "Multiplies probabilities of independent events", "Uses complements for 'at least one'"],
    S(5, 2), unit=1,
    pre=[("qm_m1_027", "hard", "Independence means P(A | B) = P(A)")], qs=[
        num("A and B are independent with P(A) = 0.4 and P(B) = 0.5. Find P(A ∩ B).", "0.2", "Rational(4, 10)*Rational(5, 10)", "basic", "0.4 × 0.5."),
        mc("P(A) = 0.3, P(B) = 0.6 and P(A ∩ B) = 0.18. Are A and B independent?",
           ["Yes, because P(A ∩ B) = P(A)P(B)", "No, because P(A ∩ B) ≠ 0", "No, because P(A) + P(B) ≠ 1", "Yes, because they are mutually exclusive"], 0,
           expl="0.3 × 0.6 = 0.18."),
        num("A and B are independent with P(A) = 0.3 and P(B) = 0.6. Find P(A ∪ B).", "0.72", "Rational(3, 10) + Rational(6, 10) - Rational(18, 100)",
            "standard", "0.3 + 0.6 − 0.18 = 0.72."),
        num("A fair coin is tossed 4 times. Find P(at least one head).", "15/16", "1 - Rational(1, 2)**4", "standard", "1 − P(no heads) = 1 − 1/16."),
    ]))

SURVEY = "In a survey of 200 people, 60 like tea and coffee, 40 like tea only, 50 like coffee only and 50 like neither. "

T.append(topic(
    "qm_m1_029", "Probabilities and independence from data", "methods", T5, "application",
    "Use relative frequencies from tables as estimates of probabilities and conditional probabilities, and judge whether events appear independent.",
    ["Estimates probabilities from counts", "Estimates conditional probabilities", "Compares P(A | B) with P(A) to judge independence"],
    S(5, 2), unit=1,
    pre=[("qm_m1_028", "hard", "Uses the independence test"), ("qm_10_010", "soft", "Reading two-way tables")], qs=[
        num(SURVEY + "Estimate P(likes tea).", "1/2", "Rational(60 + 40, 200)", "basic", "100 of 200."),
        num(SURVEY + "Estimate P(likes coffee | likes tea).", "3/5", "Rational(60, 60 + 40)", "basic", "60 of the 100 tea drinkers."),
        num(SURVEY + "Estimate P(likes coffee).", "11/20", "Rational(60 + 50, 200)", "standard", "110 of 200."),
        mc(SURVEY + "Do liking tea and liking coffee appear independent?",
           ["No: P(coffee | tea) = 0.6 differs from P(coffee) = 0.55", "Yes: P(coffee | tea) = P(coffee)",
            "Yes: some people like both", "No: the events are mutually exclusive"], 0, diff="standard",
           expl="If independent, P(coffee | tea) would equal P(coffee). 0.6 ≠ 0.55, though the difference is small for a survey."),
    ]))
