"""Mathematical Methods Unit 2 (Year 11): Calculus and further functions.

AI-drafted from the QCAA Mathematical Methods 2025 syllabus. Not reviewed by a teacher.
"""
from qlib import topic, num, mc

T1 = "T1 Exponential functions"
T2 = "T2 Logarithms and logarithmic functions"
T3 = "T3 Introduction to differential calculus"
T4 = "T4 Applications of differential calculus"
T5 = "T5 Further differentiation"


def S(t, s):
    return [("qcaa25:MM.U2.T%d.S%d" % (t, s), "exact")]


T = []

# ------------------------------------------------------------------ T1 Exponential functions

T.append(topic(
    "qm_m2_001", "Index laws with negative and fractional indices", "methods", T1, "procedural",
    "Simplify expressions with negative and fractional indices and convert between radicals and index form.",
    ["Applies all index laws", "Converts radicals to fractional indices", "Writes answers with positive indices"],
    S(1, 1), unit=2,
    pre=[("qm_10o_008", "hard", "Builds on rational exponents")], qs=[
        num("Evaluate 32^(2/5).", "4", "Integer(32)**Rational(2, 5)", "basic", "Fifth root of 32 is 2, and 2² = 4."),
        mc("Simplify (a²b⁻³)⁻², with positive indices.", ["a⁴/b⁶", "b⁶/a⁴", "b⁵/a⁴", "1/(a⁴b⁶)"], 1, "(a**2*b**-3)**-2",
           expl="(a²)⁻² = a⁻⁴ and (b⁻³)⁻² = b⁶, giving b⁶/a⁴."),
        mc("Write 1/√x as a power of x.", ["x^(1/2)", "x^(−2)", "x^(−1/2)", "−x^(1/2)"], 2, "x**Rational(-1, 2)", "standard",
           "√x = x^(1/2), and the reciprocal gives a negative index."),
        num("Solve x^(3/2) = 27.", "9", "solve(x**Rational(3, 2) - 27, x)", "standard", "Raise both sides to the power 2/3: x = 27^(2/3) = 9."),
    ]))

T.append(topic(
    "qm_m2_002", "Calculating with scientific notation", "methods", T1, "procedural",
    "Multiply and divide numbers in scientific notation and interpret very large or small results.",
    ["Multiplies and divides in scientific notation", "Adjusts the result to standard form", "Uses it in measurement contexts"],
    S(1, 1), unit=2,
    pre=[("qm_9_013", "hard", "Scientific notation from Year 9"), ("qm_m2_001", "soft", "Index laws for the powers of 10")], qs=[
        mc("Calculate (3 × 10⁻⁴) × (2 × 10⁷).", ["6 × 10³", "6 × 10⁻²⁸", "5 × 10³", "6 × 10¹¹"], 0, "(3*Rational(1, 10**4))*(2*10**7)",
           expl="3 × 2 = 6 and 10⁻⁴ × 10⁷ = 10³."),
        num("Write 4.7 × 10⁻³ as a decimal.", "0.0047", "Rational(47, 10)/1000", "basic", "Move the decimal point 3 places left."),
        mc("Calculate (8 × 10⁵) ÷ (4 × 10⁻²).", ["2 × 10³", "4 × 10⁷", "2 × 10⁷", "2 × 10⁻⁷"], 2, "(8*10**5)/(4*Rational(1, 100))", "standard",
           "8 ÷ 4 = 2 and 10⁵ ÷ 10⁻² = 10⁷."),
        num("Light travels at 3.0 × 10⁸ m/s. How many seconds does it take to travel 1.5 × 10¹¹ m?", "500",
            "(Rational(15, 10)*10**11)/(3*10**8)", "standard", "1.5 × 10¹¹ ÷ 3 × 10⁸ = 0.5 × 10³ = 500 s."),
    ]))

T.append(topic(
    "qm_m2_003", "Graphs of exponential functions", "methods", T1, "conceptual",
    "Sketch y = aˣ and its transformations, showing the asymptote and intercepts.",
    ["Identifies the horizontal asymptote", "Finds intercepts", "Describes translations, dilations and reflections"],
    S(1, 2), unit=2,
    pre=[("qm_10_007", "hard", "Basic exponential graphs"), ("qm_m2_001", "soft", "Evaluating fractional powers"),
         ("qm_9_010", "soft", "Same transformation language as parabolas")], qs=[
        num("What is the horizontal asymptote of y = 2ˣ − 3? Give the value of y.", "-3", "limit(2**x - 3, x, -oo)", "basic",
            "2ˣ → 0 as x → −∞, so y → −3."),
        num("Find the y-intercept of y = 3 × 2ˣ + 1.", "4", "(3*2**x + 1).subs(x, 0)", "basic", "3 × 1 + 1 = 4."),
        mc("Compared with y = 2ˣ, the graph of y = 2^(x − 1) is:", ["translated 1 unit right", "translated 1 unit left",
                                                                 "translated 1 unit down", "reflected in the y-axis"], 0,
           diff="standard", expl="Replacing x by x − 1 shifts the graph right."),
        mc("Which rule gives a decreasing graph?", ["y = 2^x", "y = 0.5^x", "y = 3^x + 1", "y = 2^(x+1)"], 1, diff="standard",
           expl="A base between 0 and 1 gives decay."),
    ]))

T.append(topic(
    "qm_m2_004", "Solving exponential equations with a common base", "methods", T1, "procedural",
    "Solve exponential equations by writing both sides with the same base, including quadratic-type equations.",
    ["Rewrites numbers as powers of a common base", "Equates indices", "Substitutes u = aˣ for quadratic forms"],
    S(1, 2), unit=2,
    pre=[("qm_m2_001", "hard", "Rewriting with index laws")], qs=[
        num("Solve 2ˣ = 1/8.", "-3", "solve(2**x - Rational(1, 8), x)", "basic", "1/8 = 2⁻³."),
        num("Solve 9ˣ = 27.", "3/2", "[r for r in solve(9**x - 27, x) if r.is_real]", "basic", "3^(2x) = 3³, so 2x = 3."),
        num("Solve 4^(x + 1) = 8ˣ.", "2", "solve(4**(x + 1) - 8**x, x)", "standard", "2^(2x + 2) = 2^(3x), so 2x + 2 = 3x."),
        num("Solve 2^(2x) − 6 × 2ˣ + 8 = 0.", "1, 2", "[r for r in solve(2**(2*x) - 6*2**x + 8, x) if r.is_real]", "standard",
            "Let u = 2ˣ: u² − 6u + 8 = 0, so u = 2 or 4.", unordered=True),
    ]))

T.append(topic(
    "qm_m2_005", "Exponential models", "methods", T1, "application",
    "Model growth and decay with exponential functions and interpret the parameters.",
    ["Evaluates exponential models", "Interprets initial value and growth factor", "Solves for time in simple cases"],
    S(1, 2), unit=2, tech="either",
    pre=[("qm_m2_003", "hard", "Exponential graphs and transformations"), ("qm_10_008", "hard", "Growth and decay from Year 10")], qs=[
        num("A culture of 200 bacteria triples every hour: N = 200 × 3ᵗ. Find N after 2 hours.", "1800", "200*3**2", "basic", "200 × 9 = 1800."),
        num("The amount of a drug is A = 80(0.5)^(t/4) mg after t hours. Find A when t = 8.", "20", "80*Rational(1, 2)**(8//4)", "basic",
            "80 × 0.5² = 20 mg."),
        num("A car worth $30 000 depreciates by 12% each year. Find its value after 5 years, to the nearest dollar.", "15832",
            "rnd(30000*Rational(88, 100)**5, 0)", "standard", "30 000 × 0.88⁵ ≈ 15 832.", tech="active"),
        num("The amount of a drug is A = 80(0.5)^(t/4) mg. After how many hours is A = 10 mg?", "12",
            "solve(80*Rational(1, 2)**(t/4) - 10, t)", "standard", "0.5^(t/4) = 1/8 = 0.5³, so t/4 = 3."),
    ]))

# ------------------------------------------------------------------ T2 Logarithms

T.append(topic(
    "qm_m2_006", "Logarithm definition and laws", "methods", T2, "procedural",
    "Use logₐ y = x ⇔ aˣ = y and the logarithm laws to evaluate and simplify.",
    ["Converts between index and logarithmic forms", "Uses the product, quotient and power laws", "Evaluates logs exactly"],
    S(2, 1), unit=2,
    pre=[("qm_10o_009", "hard", "Builds on Year 10 logarithms"), ("qm_m2_001", "hard", "Logs of fractional powers")], qs=[
        num("Evaluate log₅ 125.", "3", "log(125, 5)", "basic", "5³ = 125."),
        num("Evaluate log₄ 2.", "1/2", "log(2, 4)", "basic", "4^(1/2) = 2."),
        num("Evaluate log₂ 40 − log₂ 5.", "3", "log(40, 2) - log(5, 2)", "standard", "log₂ 8 = 3."),
        num("Evaluate 2 log₃ 6 − log₃ 4.", "2", "2*log(6, 3) - log(4, 3)", "standard", "log₃(36/4) = log₃ 9 = 2."),
    ]))

T.append(topic(
    "qm_m2_007", "Solving exponential equations with logarithms", "methods", T2, "procedural",
    "Solve aˣ = b exactly with logarithms and approximately with technology.",
    ["Takes logs of both sides", "Gives exact answers in log form", "Finds decimal approximations"],
    S(2, 1), unit=2, tech="active",
    pre=[("qm_m2_006", "hard", "Uses the definition and laws"), ("qm_m2_004", "hard", "Exponential equations")], qs=[
        mc("Solve 3ˣ = 10 exactly.", ["x = log₃ 10", "x = log₁₀ 3", "x = 10/3", "x = 3¹⁰"], 0, expl="By definition, x = log₃ 10."),
        num("Solve 2ˣ = 20, correct to 2 decimal places.", "4.32", "rnd(log(20)/log(2), 2)", "basic", "x = log 20 ÷ log 2 ≈ 4.32.", tech="active"),
        num("Solve 5^(x − 1) = 30, correct to 2 decimal places.", "3.11", "rnd(1 + log(30)/log(5), 2)", "standard",
            "x − 1 = log₅ 30 ≈ 2.11.", tech="active"),
        num("$2000 grows at 4% p.a. compounded annually. After how many whole years does it first exceed $3000?", "11",
            "ceiling(log(Rational(3, 2))/log(Rational(104, 100)))", "standard", "1.04ⁿ > 1.5 gives n > 10.3, so 11 years.", tech="active"),
    ]))

T.append(topic(
    "qm_m2_008", "Graphs of logarithmic functions", "methods", T2, "conceptual",
    "Sketch y = logₐ x and its transformations, showing the vertical asymptote and intercepts, and relate it to y = aˣ.",
    ["Identifies the vertical asymptote", "Finds intercepts", "Recognises log and exponential graphs as reflections in y = x"],
    S(2, 2), unit=2,
    pre=[("qm_m2_006", "hard", "Evaluating logarithms"), ("qm_m2_003", "hard", "Inverse of the exponential graph")], qs=[
        mc("What is the vertical asymptote of y = log₂(x − 3)?", ["x = 3", "x = −3", "y = 3", "x = 0"], 0, expl="The log is defined only for x − 3 > 0."),
        num("Find the x-intercept of y = log₂ x.", "1", "solve(log(x, 2), x)", "basic", "log₂ 1 = 0."),
        num("Find the x-intercept of y = log₂(x − 3).", "4", "solve(log(x - 3, 2), x)", "standard", "x − 3 = 1."),
        mc("The graphs of y = log₂ x and y = 2ˣ are reflections of each other in:", ["the x-axis", "the y-axis", "the line y = x", "the origin"], 2,
           diff="standard", expl="They are inverse functions."),
    ]))

T.append(topic(
    "qm_m2_009", "Solving logarithmic equations", "methods", T2, "procedural",
    "Solve equations involving logarithms and check solutions lie in the domain.",
    ["Converts a log equation to index form", "Combines logs before solving", "Rejects solutions outside the domain"],
    S(2, 2), unit=2,
    pre=[("qm_m2_006", "hard", "Uses the definition and laws")], qs=[
        num("Solve log₃ x = 4.", "81", "solve(log(x, 3) - 4, x)", "basic", "x = 3⁴."),
        num("Solve log₂(x + 1) = 3.", "7", "solve(log(x + 1, 2) - 3, x)", "basic", "x + 1 = 8."),
        num("Solve log₁₀ x + log₁₀(x − 3) = 1.", "5", "[r for r in solve(x*(x - 3) - 10, x) if r > 3]", "standard",
            "x(x − 3) = 10 gives x = 5 or −2; only 5 is in the domain."),
        num("Solve log₂(3x − 1) = log₂(x + 5).", "3", "solve(3*x - 1 - (x + 5), x)", "standard", "3x − 1 = x + 5."),
    ]))

T.append(topic(
    "qm_m2_010", "Logarithmic models", "methods", T2, "application",
    "Use logarithmic scales such as decibels, pH and the Richter scale and interpret changes on them.",
    ["Evaluates a logarithmic model", "Interprets a change of 1 unit as a multiplicative change", "Solves for the original quantity"],
    S(2, 2), unit=2,
    pre=[("qm_m2_007", "hard", "Solving with logarithms")], qs=[
        num("Sound level is L = 10 log₁₀(I/I₀) dB. Find L when I = 10⁶ I₀.", "60", "10*log(10**6, 10)", "basic", "10 × 6 = 60 dB."),
        num("pH = −log₁₀[H⁺]. Find the pH when [H⁺] = 10⁻³.", "3", "-log(Rational(1, 1000), 10)", "basic", "−(−3) = 3."),
        num("On the Richter scale M = log₁₀(A/A₀). How many times larger is the amplitude of a magnitude 7 earthquake than a magnitude 5?",
            "100", "10**(7 - 5)", "standard", "Each unit is a factor of 10, so 10²."),
        num("Using L = 10 log₁₀(I/I₀), how many decibels are added when the intensity is multiplied by 1000?", "30", "10*log(1000, 10)", "standard",
            "10 log₁₀ 1000 = 30."),
    ]))

# ------------------------------------------------------------------ T3 Introduction to differential calculus

T.append(topic(
    "qm_m2_011", "Average rate of change", "methods", T3, "procedural",
    "Calculate the average rate of change of a function over an interval and interpret it in context.",
    ["Uses (f(b) − f(a))/(b − a)", "Interprets the answer with units"],
    S(3, 1), unit=2,
    pre=[("qm_9_007", "hard", "The average rate is the gradient of a chord")], qs=[
        num("Find the average rate of change of f(x) = x² from x = 1 to x = 3.", "4", "((x**2).subs(x, 3) - (x**2).subs(x, 1))/(3 - 1)", "basic",
            "(9 − 1)/2 = 4."),
        num("A car travels 150 km in 2.5 hours. What is its average speed in km/h?", "60", "150/Rational(5, 2)", "basic", "150 ÷ 2.5 = 60."),
        num("Find the average rate of change of f(x) = x³ − x from x = −1 to x = 2.", "2",
            "((x**3 - x).subs(x, 2) - (x**3 - x).subs(x, -1))/(2 - (-1))", "standard", "(6 − 0)/3 = 2."),
        num("A town had 1200 people in 2020 and 1500 in 2026. Find the average rate of change in people per year.", "50", "(1500 - 1200)/Integer(6)",
            "standard", "300 ÷ 6 = 50."),
    ]))

T.append(topic(
    "qm_m2_012", "The derivative from first principles", "methods", T3, "reasoning",
    "Use f′(x) = lim (h → 0) [f(x + h) − f(x)]/h to differentiate simple polynomials.",
    ["States the limit definition", "Simplifies the difference quotient", "Takes the limit as h → 0"],
    S(3, 1), unit=2,
    pre=[("qm_m2_011", "hard", "The derivative is the limit of average rates"), ("qm_10_001", "hard", "Expanding and simplifying")], qs=[
        mc("The derivative of f at x is defined as:", ["lim (h → 0) [f(x + h) − f(x)]/h", "[f(x + h) − f(x)]/h",
                                                       "lim (h → 0) [f(x) − f(h)]/x", "f(x + h) − f(x)"], 0,
           expl="The gradient of a chord as its width h shrinks to 0."),
        mc("For f(x) = x², the difference quotient [f(x + h) − f(x)]/h simplifies to:", ["2x", "2x + h", "x + h", "2xh + h²"], 1,
           "simplify(((x + h)**2 - x**2)/h)", expl="(x² + 2xh + h² − x²)/h = 2x + h."),
        mc("Using first principles, the derivative of f(x) = 3x² − x is:", ["6x", "3x − 1", "6x − 1", "6x² − 1"], 2,
           "limit((3*(x + h)**2 - (x + h) - (3*x**2 - x))/h, h, 0)", "standard", "The difference quotient is 6x + 3h − 1, which tends to 6x − 1."),
        num("For f(x) = x³, [f(2 + h) − f(2)]/h = 12 + 6h + h². What is f′(2)?", "12", "limit(((2 + h)**3 - 8)/h, h, 0)", "standard",
            "Let h → 0."),
    ]))

T.append(topic(
    "qm_m2_013", "The derivative as rate of change and gradient", "methods", T3, "conceptual",
    "Interpret f′(a) as the instantaneous rate of change and as the gradient of the tangent at x = a.",
    ["Interprets f′(a) in context", "Links the sign of f′ to increasing and decreasing", "Recognises f′(a) = 0 as a horizontal tangent"],
    S(3, 1), unit=2,
    pre=[("qm_m2_012", "hard", "The derivative comes from the limit")], qs=[
        num("f′(x) = 2x. What is the gradient of the tangent at x = 3?", "6", "(2*x).subs(x, 3)", "basic", "f′(3) = 6."),
        mc("If f′(2) = 0, then at x = 2 the tangent is:", ["horizontal", "vertical", "undefined", "steepest"], 0, expl="Gradient 0 means horizontal."),
        num("A ball's height is h(t) = 20t − 5t² metres, so h′(t) = 20 − 10t. Find the rate of change of height at t = 1, in m/s.", "10",
            "diff(20*t - 5*t**2, t).subs(t, 1)", "standard", "20 − 10 = 10 m/s upwards."),
        mc("If f′(x) < 0 on an interval, then on that interval f is:", ["decreasing", "increasing", "concave up", "zero"], 0, diff="standard",
           expl="Negative gradient means the function is going down."),
    ]))

T.append(topic(
    "qm_m2_014", "The power rule and derivatives of polynomials", "methods", T3, "procedural",
    "Differentiate polynomials using d/dx(xⁿ) = nxⁿ⁻¹ with the sum and constant-multiple properties.",
    ["Applies the power rule", "Differentiates term by term", "Expands before differentiating products"],
    S(3, 1), unit=2,
    pre=[("qm_m2_013", "hard", "Knows what a derivative means")], qs=[
        mc("d/dx (x⁵) =", ["x⁴", "5x⁴", "5x⁵", "4x⁵"], 1, "diff(x**5, x)", expl="Bring down the power and subtract 1."),
        mc("Differentiate y = 3x⁴ − 2x² + 7.", ["12x³ − 4x", "12x³ − 4x + 7", "3x³ − 2x", "12x⁴ − 4x²"], 0, "diff(3*x**4 - 2*x**2 + 7, x)",
           expl="The constant 7 has derivative 0."),
        num("f(x) = 2x³ − 5x + 1. Find f′(2).", "19", "diff(2*x**3 - 5*x + 1, x).subs(x, 2)", "standard", "f′(x) = 6x² − 5, so 24 − 5 = 19."),
        mc("Differentiate y = (x + 3)(2x − 1) by expanding first.", ["2", "4x − 5", "2x + 5", "4x + 5"], 3, "diff((x + 3)*(2*x - 1), x)", "standard",
           "y = 2x² + 5x − 3, so dy/dx = 4x + 5."),
    ]))

# ------------------------------------------------------------------ T4 Applications of differential calculus

T.append(topic(
    "qm_m2_015", "Tangents and normals", "methods", T4, "procedural",
    "Find the equations of the tangent and normal to a curve at a point.",
    ["Finds the gradient at a point", "Writes the tangent with y − y₁ = m(x − x₁)", "Uses −1/m for the normal"],
    S(4, 1), unit=2,
    pre=[("qm_m2_014", "hard", "Needs the derivative"), ("qm_9_007", "hard", "Equation of a line from gradient and point")], qs=[
        num("Find the gradient of the tangent to y = x² − 3x at x = 4.", "5", "diff(x**2 - 3*x, x).subs(x, 4)", "basic", "2(4) − 3 = 5."),
        mc("Find the equation of the tangent to y = x² at (1, 1).", ["y = 2x + 1", "y = x", "y = 2x − 1", "y = 2x"], 2, "2*(x - 1) + 1",
           expl="Gradient 2, so y − 1 = 2(x − 1)."),
        mc("Find the equation of the normal to y = x² at (1, 1).", ["y = −2x + 3", "y = −x/2 + 3/2", "y = x/2 + 1/2", "y = −x/2 + 1"], 1,
           "-(x - 1)/2 + 1", "standard", "The normal gradient is −1/2: y − 1 = −½(x − 1)."),
        num("At what x-value does y = x² − 6x + 2 have a tangent with gradient 4?", "5", "solve(diff(x**2 - 6*x + 2, x) - 4, x)", "standard",
            "2x − 6 = 4."),
    ]))

MOTION = "A particle moves so that its displacement is x(t) = t³ − 6t² + 9t metres after t seconds. "

T.append(topic(
    "qm_m2_016", "Displacement and velocity", "methods", T4, "application",
    "Interpret velocity as the derivative of displacement, and use it to find when a particle is at rest or changes direction.",
    ["Differentiates displacement to get velocity", "Finds when velocity is zero", "Interprets signs of velocity"],
    S(4, 1), unit=2,
    pre=[("qm_m2_014", "hard", "Velocity is a derivative")], qs=[
        mc(MOTION + "Find the velocity function.", ["t² − 6t + 9", "3t² − 12t + 9", "3t² − 12t", "6t − 12"], 1, "diff(t**3 - 6*t**2 + 9*t, t)",
           expl="Differentiate each term."),
        num(MOTION + "Find the velocity at t = 2, in m/s.", "-3", "diff(t**3 - 6*t**2 + 9*t, t).subs(t, 2)", "basic", "12 − 24 + 9 = −3."),
        num(MOTION + "At what times is the particle at rest?", "1, 3", "solve(diff(t**3 - 6*t**2 + 9*t, t), t)", "standard",
            "3t² − 12t + 9 = 3(t − 1)(t − 3) = 0.", unordered=True),
        num(MOTION + "Find the displacement at t = 3.", "0", "(t**3 - 6*t**2 + 9*t).subs(t, 3)", "standard", "27 − 54 + 27 = 0."),
    ]))

T.append(topic(
    "qm_m2_017", "Stationary points and their nature", "methods", T4, "procedural",
    "Find stationary points by solving f′(x) = 0 and classify them with the first derivative test.",
    ["Solves f′(x) = 0", "Uses the sign of f′ either side", "Recognises stationary points of inflection"],
    S(4, 1), unit=2,
    pre=[("qm_m2_014", "hard", "Needs the derivative"), ("qm_m1_002", "hard", "f′(x) = 0 is often quadratic")], qs=[
        num("Find the x-coordinate of the stationary point of y = x² − 8x + 3.", "4", "solve(diff(x**2 - 8*x + 3, x), x)", "basic", "2x − 8 = 0."),
        num("Find the x-coordinates of the stationary points of y = x³ − 3x.", "1, -1", "solve(diff(x**3 - 3*x, x), x)", "basic",
            "3x² − 3 = 0.", unordered=True),
        mc("For y = x³ − 3x, the stationary point at x = −1 is a:", ["local minimum", "local maximum", "stationary point of inflection", "not stationary"], 1,
           diff="standard", expl="f′ changes from positive to negative at x = −1."),
        mc("At x = 0, the curve y = x³ has:", ["a local minimum", "a local maximum", "a stationary point of inflection", "no stationary point"], 2,
           diff="standard", expl="f′(0) = 0 but f′ is positive on both sides."),
    ]))

T.append(topic(
    "qm_m2_018", "Sketching polynomials and global extrema", "methods", T4, "procedural",
    "Sketch polynomials up to degree 4 using stationary points and end behaviour, and find global maxima and minima on an interval.",
    ["Combines intercepts, stationary points and end behaviour in a sketch", "Compares endpoint and stationary values for global extrema"],
    S(4, 1), unit=2,
    pre=[("qm_m2_017", "hard", "Uses stationary points"), ("qm_m1_011", "soft", "Shapes of cubic graphs")], qs=[
        num("Find the local maximum value of y = −x² + 4x.", "4", "(-x**2 + 4*x).subs(x, 2)", "basic", "At x = 2, y = −4 + 8 = 4."),
        num("Find the x-coordinates of the stationary points of y = x⁴ − 2x².", "0, 1, -1", "solve(diff(x**4 - 2*x**2, x), x)", "basic",
            "4x³ − 4x = 4x(x − 1)(x + 1) = 0.", unordered=True),
        num("Find the global maximum of f(x) = x³ − 3x on −2 ≤ x ≤ 3.", "18", "maximum(x**3 - 3*x, x, Interval(-2, 3))", "standard",
            "Compare f(−2) = −2, f(−1) = 2, f(1) = −2 and f(3) = 18."),
        num("Find the global minimum of f(x) = x³ − 3x on −2 ≤ x ≤ 3.", "-2", "minimum(x**3 - 3*x, x, Interval(-2, 3))", "standard",
            "f(−2) = f(1) = −2 is the lowest value."),
    ]))

# ------------------------------------------------------------------ T5 Further differentiation

T.append(topic(
    "qm_m2_019", "The chain rule", "methods", T5, "procedural",
    "Differentiate composite power and polynomial functions with dy/dx = dy/du × du/dx.",
    ["Identifies the inner and outer functions", "Applies the chain rule", "Differentiates roots as fractional powers"],
    S(5, 1), unit=2,
    pre=[("qm_m2_014", "hard", "Power rule for each layer"), ("qm_m2_001", "hard", "Roots as fractional powers")], qs=[
        mc("d/dx (2x + 1)⁵ =", ["5(2x + 1)⁴", "10(2x + 1)⁴", "10(2x + 1)⁵", "2(2x + 1)⁴"], 1, "diff((2*x + 1)**5, x)",
           expl="5(2x + 1)⁴ × 2."),
        mc("d/dx (x² + 1)³ =", ["3(x² + 1)²", "6x(x² + 1)³", "2x(x² + 1)²", "6x(x² + 1)²"], 3, "diff((x**2 + 1)**3, x)",
           expl="3(x² + 1)² × 2x."),
        mc("d/dx √(x² + 9) =", ["x/√(x² + 9)", "1/(2√(x² + 9))", "2x/√(x² + 9)", "x√(x² + 9)"], 0, "diff(sqrt(x**2 + 9), x)", "standard",
           "½(x² + 9)^(−1/2) × 2x."),
        num("f(x) = (3x − 5)⁴. Find f′(2).", "12", "diff((3*x - 5)**4, x).subs(x, 2)", "standard", "f′(x) = 12(3x − 5)³, and 12 × 1³ = 12."),
    ]))

T.append(topic(
    "qm_m2_020", "The product rule", "methods", T5, "procedural",
    "Differentiate products with (uv)′ = u′v + uv′ and give the result in factorised form.",
    ["Identifies u and v", "Applies the product rule", "Factorises the result"],
    S(5, 1), unit=2,
    pre=[("qm_m2_014", "hard", "Differentiates each factor"), ("qm_m2_019", "soft", "Factors are often composite")], qs=[
        mc("d/dx [x²(x + 1)³] =", ["6x(x + 1)²", "x(x + 1)²(5x + 2)", "2x(x + 1)³", "x(x + 1)²(5x + 3)"], 1, "diff(x**2*(x + 1)**3, x)",
           expl="2x(x + 1)³ + 3x²(x + 1)² = x(x + 1)²(2x + 2 + 3x)."),
        num("f(x) = x(x − 2)². Find f′(1).", "-1", "diff(x*(x - 2)**2, x).subs(x, 1)", "basic", "f′(x) = (x − 2)² + 2x(x − 2), so 1 − 2 = −1."),
        mc("d/dx [x√(x + 1)] =", ["1/(2√(x + 1))", "(x + 2)/(2√(x + 1))", "(3x + 2)/(2√(x + 1))", "(3x + 1)/(2√(x + 1))"], 2,
           "diff(x*sqrt(x + 1), x)", "standard", "√(x + 1) + x/(2√(x + 1)) = (2(x + 1) + x)/(2√(x + 1))."),
        num("y = (2x + 1)(x² − 3). Find dy/dx at x = 1.", "2", "diff((2*x + 1)*(x**2 - 3), x).subs(x, 1)", "standard",
            "2(x² − 3) + (2x + 1)(2x) = 2(−2) + 3(2) = 2."),
    ]))

T.append(topic(
    "qm_m2_021", "The quotient rule", "methods", T5, "procedural",
    "Differentiate quotients with (u/v)′ = (u′v − uv′)/v².",
    ["Identifies u and v", "Applies the quotient rule with the correct order of subtraction", "Simplifies the numerator"],
    S(5, 1), unit=2,
    pre=[("qm_m2_014", "hard", "Differentiates numerator and denominator")], qs=[
        mc("d/dx [x/(x + 1)] =", ["−1/(x + 1)²", "1/(x + 1)²", "x/(x + 1)²", "1/(x + 1)"], 1, "diff(x/(x + 1), x)",
           expl="(1(x + 1) − x(1))/(x + 1)² = 1/(x + 1)²."),
        num("f(x) = (x + 2)/(x − 1). Find f′(2).", "-3", "diff((x + 2)/(x - 1), x).subs(x, 2)", "basic", "f′(x) = −3/(x − 1)², so −3."),
        mc("d/dx [(2x − 1)/(x² + 1)] =", ["(2x² − 2x + 2)/(x² + 1)²", "(−2x² + 2x + 2)/(x² + 1)²", "(−2x² + 2x − 2)/(x² + 1)²", "1/x"], 1,
           "diff((2*x - 1)/(x**2 + 1), x)", "standard", "(2(x² + 1) − (2x − 1)(2x))/(x² + 1)² = (−2x² + 2x + 2)/(x² + 1)²."),
        num("y = x²/(x + 3). Find dy/dx at x = 1.", "7/16", "diff(x**2/(x + 3), x).subs(x, 1)", "standard", "(2x(x + 3) − x²)/(x + 3)² = (8 − 1)/16."),
    ]))

T.append(topic(
    "qm_m2_022", "Combining differentiation rules", "methods", T5, "procedural",
    "Choose and combine the chain, product and quotient rules, giving derivatives in simplest factorised form.",
    ["Recognises which rules apply", "Applies two rules in one derivative", "Factorises fully"],
    S(5, 1), unit=2,
    pre=[("qm_m2_019", "hard", "Chain rule"), ("qm_m2_020", "hard", "Product rule"), ("qm_m2_021", "hard", "Quotient rule")], qs=[
        mc("d/dx [x(2x + 1)³] =", ["(2x + 1)²(6x + 1)", "3(2x + 1)²", "(2x + 1)²(8x + 1)", "(2x + 1)³(8x + 1)"], 2, "diff(x*(2*x + 1)**3, x)",
           expl="(2x + 1)³ + 6x(2x + 1)² = (2x + 1)²(2x + 1 + 6x)."),
        mc("d/dx [(x + 1)²/x] =", ["(x² − 1)/x²", "(x + 1)²/x²", "2(x + 1)/x", "(x² + 1)/x²"], 0, "diff((x + 1)**2/x, x)",
           expl="(2(x + 1)x − (x + 1)²)/x² = (x + 1)(x − 1)/x²."),
        num("f(x) = x²(1 − x)⁴. Find f′(2).", "20", "diff(x**2*(1 - x)**4, x).subs(x, 2)", "standard",
            "f′(x) = 2x(1 − x)⁴ − 4x²(1 − x)³, so 4(1) − 16(−1) = 20."),
        mc("d/dx [x²/(x + 1)²] =", ["2x/(x + 1)²", "x/(x + 1)³", "2x/(x + 1)³", "2/(x + 1)³"], 2, "diff(x**2/(x + 1)**2, x)", "standard",
           "(2x(x + 1)² − 2x²(x + 1))/(x + 1)⁴ = 2x(x + 1)/(x + 1)⁴."),
    ]))
