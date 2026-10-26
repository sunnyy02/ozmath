"""Pilot slice: Year 9 and 10 algebra -> Year 10 optional -> Methods Unit 1 Topic 1
(Surds and quadratic functions). 30 topics.

AI-drafted. Not reviewed by a teacher. Prerequisite strengths are judgement calls.
"""
from qlib import topic, num, mc

ALG, NUM = "Algebra", "Number"
MM1 = "T1 Surds and quadratic functions"
ROOT_Y9 = "Year 9 is the lowest level in this graph; Year 7-8 assumed knowledge is not modelled."

T = []

# ------------------------------------------------------------------ Year 9

T.append(topic(
    "qm_9_001", "Rational and irrational numbers", "y9", NUM, "conceptual",
    "Tell rational numbers (fractions, terminating or recurring decimals) from irrational ones such as √2 and π, and estimate square roots.",
    ["Classifies numbers as rational or irrational", "Writes terminating decimals as fractions", "Places a square root between two whole numbers"],
    [("AC9M9N01", "exact")], root_reason=ROOT_Y9, qs=[
        mc("Which of these numbers is irrational?", ["√16", "0.25", "√7", "3/8"], 2,
           expl="7 is not a perfect square, so √7 cannot be written as a fraction. √16 = 4."),
        mc("Which of these numbers is rational?", ["π", "√2", "√10", "√49"], 3,
           expl="√49 = 7, a whole number, so it is rational."),
        num("Write 0.375 as a fraction in simplest form.", "3/8", "Rational(375, 1000)", "standard",
            "0.375 = 375/1000 = 3/8."),
        mc("Between which two consecutive whole numbers does √40 lie?", ["5 and 6", "6 and 7", "7 and 8", "20 and 21"], 1,
           diff="standard", expl="6² = 36 and 7² = 49, and 36 < 40 < 49."),
    ]))

T.append(topic(
    "qm_9_002", "Index laws with positive integer exponents", "y9", ALG, "procedural",
    "Multiply, divide and raise powers with the same base, for numbers and variables.",
    ["Adds exponents when multiplying powers of the same base", "Subtracts exponents when dividing", "Multiplies exponents for a power of a power"],
    [("AC9M9A01", "exact")], root_reason=ROOT_Y9, qs=[
        num("Evaluate 2⁵ × 2² ÷ 2⁴.", "8", "2**5 * 2**2 / Integer(2)**4", "basic",
            "2⁵ × 2² ÷ 2⁴ = 2^(5+2−4) = 2³ = 8."),
        mc("Simplify a⁴ × a³.", ["a⁷", "a¹²", "2a⁷", "a"], 0, "a**4 * a**3",
           expl="Same base: add the exponents, 4 + 3 = 7."),
        mc("Simplify (3x²)³.", ["9x⁶", "3x⁶", "27x⁶", "27x⁵"], 2, "(3*x**2)**3", "standard",
           "Cube both factors: 3³ = 27 and (x²)³ = x⁶."),
        num("Evaluate (5⁴ × 5²) ÷ (5³)².", "1", "(5**4 * 5**2) / Integer(5**3)**2", "standard",
            "Numerator 5⁶, denominator 5⁶, so the result is 1."),
    ]))

T.append(topic(
    "qm_9_003", "Zero and negative exponents", "y9", ALG, "procedural",
    "Use a⁰ = 1 and a⁻ⁿ = 1/aⁿ, and write answers with positive exponents.",
    ["Evaluates zero and negative powers of numbers", "Simplifies expressions with negative exponents"],
    [("AC9M9A01", "exact")],
    pre=[("qm_9_002", "hard", "The zero and negative exponent rules come from extending the index laws")], qs=[
        num("Evaluate 7⁰.", "1", "Integer(7)**0", "basic", "Any non-zero number to the power 0 is 1."),
        num("Evaluate 2⁻³. Give your answer as a fraction.", "1/8", "Integer(2)**-3", "basic", "2⁻³ = 1/2³ = 1/8."),
        mc("Simplify x⁻² × x⁵.", ["x⁻¹⁰", "x³", "x⁷", "1/x³"], 1, "x**-2 * x**5", "standard",
           "Add the exponents: −2 + 5 = 3."),
        num("Evaluate (2/3)⁻².", "9/4", "Rational(2, 3)**-2", "standard", "(2/3)⁻² = (3/2)² = 9/4."),
    ]))

T.append(topic(
    "qm_9_004", "Expanding binomial products", "y9", ALG, "procedural",
    "Expand products such as (x + a)(x + b) and (ax + b)(cx + d) and collect like terms.",
    ["Multiplies every term in one bracket by every term in the other", "Collects like terms correctly, including signs"],
    [("AC9M9A02", "exact")], root_reason=ROOT_Y9, qs=[
        mc("Expand (x + 3)(x + 5).", ["x² + 15x + 8", "x² + 8x + 15", "x² + 8x + 8", "2x + 8"], 1,
           "expand((x + 3)*(x + 5))", expl="x² + 5x + 3x + 15 = x² + 8x + 15."),
        mc("Expand (x − 4)(x + 2).", ["x² − 2x − 8", "x² + 2x − 8", "x² − 6x − 8", "x² − 2x + 8"], 0,
           "expand((x - 4)*(x + 2))", expl="x² + 2x − 4x − 8 = x² − 2x − 8."),
        mc("Expand (2x + 1)(x − 3).", ["2x² − 6x − 3", "2x² + 5x − 3", "2x² − 5x − 3", "2x² − 7x − 3"], 2,
           "expand((2*x + 1)*(x - 3))", "standard", "2x² − 6x + x − 3 = 2x² − 5x − 3."),
        num("When (x + 6)(x − 2) is expanded to x² + bx + c, what is b + c?", "-8",
            "(lambda p: p.coeff(x, 1) + p.coeff(x, 0))(expand((x + 6)*(x - 2)))", "standard",
            "x² + 4x − 12, so b + c = 4 + (−12) = −8."),
    ]))

T.append(topic(
    "qm_9_005", "Factorising by taking out a common factor", "y9", ALG, "procedural",
    "Take out the highest common factor of the terms, including variables.",
    ["Finds the HCF of numbers and pronumerals", "Checks a factorisation by expanding"],
    [("AC9M9A02", "inferred")],
    pre=[("qm_9_004", "soft", "Factorising reverses expanding, so expanding is used to check")], qs=[
        mc("Factorise 6x + 9.", ["6(x + 9)", "3(2x + 3)", "3(2x + 9)", "9(x + 1)"], 1, "6*x + 9",
           expl="The HCF of 6 and 9 is 3: 6x + 9 = 3(2x + 3)."),
        mc("Factorise x² − 5x.", ["x(x − 5)", "x(x + 5)", "5x(x − 1)", "x²(1 − 5)"], 0, "x**2 - 5*x",
           expl="Both terms contain x: x² − 5x = x(x − 5)."),
        num("8a²b − 12ab = k·ab(2a − 3). What is k?", "4", "gcd(8, 12)", "standard",
            "The HCF of 8a²b and 12ab is 4ab, and 4ab(2a − 3) = 8a²b − 12ab."),
        num("15x² + 10x factorises fully as 5x(px + q). What is p + q?", "5", "3 + 2", "standard",
            "15x² + 10x = 5x(3x + 2), so p + q = 3 + 2 = 5."),
    ]))

T.append(topic(
    "qm_9_006", "Factorising monic quadratics", "y9", ALG, "procedural",
    "Factorise x² + bx + c by finding two numbers that multiply to c and add to b.",
    ["Finds the factor pair of c that adds to b, including negatives", "Checks the factorisation by expanding"],
    [("AC9M9A02", "exact")],
    pre=[("qm_9_004", "hard", "Factorising a quadratic means finding the binomial product that expands to it"),
         ("qm_9_005", "soft", "Common-factor factorising is the simpler first case")], qs=[
        mc("Factorise x² + 7x + 12.", ["(x + 2)(x + 6)", "(x + 1)(x + 12)", "(x − 3)(x − 4)", "(x + 3)(x + 4)"], 3,
           "x**2 + 7*x + 12", expl="3 × 4 = 12 and 3 + 4 = 7."),
        mc("Factorise x² − x − 6.", ["(x − 3)(x + 2)", "(x + 3)(x − 2)", "(x − 6)(x + 1)", "(x − 3)(x − 2)"], 0,
           "x**2 - x - 6", expl="−3 × 2 = −6 and −3 + 2 = −1."),
        mc("Factorise x² − 10x + 21.", ["(x + 3)(x + 7)", "(x − 3)(x − 7)", "(x − 1)(x − 21)", "(x − 3)(x + 7)"], 1,
           "x**2 - 10*x + 21", "standard", "−3 × −7 = 21 and −3 + (−7) = −10."),
        num("x² + bx − 20 = (x + 5)(x − 4). What is b?", "1", "expand((x + 5)*(x - 4)).coeff(x, 1)", "standard",
            "(x + 5)(x − 4) = x² + x − 20, so b = 1."),
    ]))

T.append(topic(
    "qm_9_007", "Gradient, midpoint and distance", "y9", ALG, "procedural",
    "Find the gradient, midpoint and length of a line segment from the coordinates of its end points.",
    ["Uses rise over run for gradient", "Averages coordinates for the midpoint", "Uses Pythagoras' theorem for distance"],
    [("AC9M9A03", "exact")], root_reason=ROOT_Y9, qs=[
        num("Find the gradient of the line through (1, 2) and (3, 8).", "3", "Rational(8 - 2, 3 - 1)", "basic",
            "Rise 6, run 2, gradient 6/2 = 3."),
        num("Find the midpoint of the segment joining (−2, 4) and (6, 0). Write it as (x, y).", "(2, 2)",
            "(Rational(-2 + 6, 2), Rational(4 + 0, 2))", "basic", "((−2 + 6)/2, (4 + 0)/2) = (2, 2)."),
        num("Find the distance between (1, 1) and (4, 5).", "5", "sqrt((4 - 1)**2 + (5 - 1)**2)", "standard",
            "√(3² + 4²) = √25 = 5."),
        num("A line through (0, 3) and (4, k) has gradient −1/2. Find k.", "1", "3 + 4*Rational(-1, 2)", "standard",
            "(k − 3)/4 = −1/2, so k − 3 = −2 and k = 1."),
    ]))

T.append(topic(
    "qm_9_008", "Graphing quadratic functions", "y9", ALG, "conceptual",
    "Graph y = x² + bx + c from a table of values and read off intercepts and the turning point, using the symmetry of the parabola.",
    ["Plots a parabola from a table of values", "Reads intercepts from the rule or graph", "Uses symmetry to locate the turning point"],
    [("AC9M9A04", "exact")], root_reason=ROOT_Y9, qs=[
        num("For y = x² − 4, what is the y-intercept?", "-4", "(x**2 - 4).subs(x, 0)", "basic", "Put x = 0: y = 0 − 4 = −4."),
        num("For y = x² − 4, find both x-intercepts.", "-2, 2", "solve(x**2 - 4, x)", "basic",
            "x² = 4, so x = −2 or x = 2.", unordered=True),
        mc("Which point lies on the graph of y = x² + 2x?", ["(2, 6)", "(1, 3)", "(−1, 1)", "(3, 12)"], 1, diff="standard",
           expl="When x = 1, y = 1 + 2 = 3. Check the others: x = 2 gives 8, x = −1 gives −1, x = 3 gives 15."),
        num("The x-intercepts of y = x² − 6x + 5 are 1 and 5. Use symmetry to find the x-coordinate of the turning point.",
            "3", "Rational(1 + 5, 2)", "standard", "The turning point is halfway between the intercepts: (1 + 5)/2 = 3."),
    ]))

T.append(topic(
    "qm_9_009", "Solving monic quadratic equations by factorising", "y9", ALG, "procedural",
    "Rearrange to = 0, factorise and use the null factor law.",
    ["Rearranges a quadratic equation to = 0", "Applies the null factor law to each factor"],
    [("AC9M9A04", "inferred")],
    pre=[("qm_9_006", "hard", "The equation must be factorised before the null factor law can be used")], qs=[
        num("Solve (x − 3)(x + 5) = 0.", "3, -5", "solve((x - 3)*(x + 5), x)", "basic",
            "x − 3 = 0 or x + 5 = 0, so x = 3 or x = −5.", unordered=True),
        num("Solve x² − 5x + 6 = 0.", "2, 3", "solve(x**2 - 5*x + 6, x)", "basic",
            "(x − 2)(x − 3) = 0, so x = 2 or x = 3.", unordered=True),
        num("Solve x² + 4x = 0.", "0, -4", "solve(x**2 + 4*x, x)", "standard",
            "x(x + 4) = 0, so x = 0 or x = −4. Do not divide by x, or you lose x = 0.", unordered=True),
        num("Solve x² − 2x = 15.", "5, -3", "solve(x**2 - 2*x - 15, x)", "standard",
            "x² − 2x − 15 = 0, (x − 5)(x + 3) = 0, so x = 5 or x = −3.", unordered=True),
    ]))

T.append(topic(
    "qm_9_010", "Transformations of y = x²", "y9", ALG, "conceptual",
    "Describe how a, h and k in y = a(x − h)² + k dilate, reflect and translate the graph of y = x².",
    ["Describes vertical and horizontal translations", "Describes dilation and reflection from a", "Reads the turning point from the rule"],
    [("AC9M9A06", "exact")],
    pre=[("qm_9_008", "hard", "Transformations are described relative to the graph of y = x²")], qs=[
        mc("How is the graph of y = x² + 3 related to the graph of y = x²?",
           ["Translated 3 units up", "Translated 3 units right", "Translated 3 units down", "Dilated by a factor of 3"], 0,
           expl="Adding 3 to every y-value moves the graph up 3 units."),
        mc("Which equation is y = x² translated 2 units to the right?", ["y = (x + 2)²", "y = x² − 2", "y = (x − 2)²", "y = x² + 2"], 2,
           "(x - 2)**2", expl="Replacing x with x − 2 moves the graph 2 units right."),
        num("What are the coordinates of the turning point of y = (x + 1)² − 4? Write them as (x, y).", "(-1, -4)",
            "(lambda f: (lambda s: (s, f.subs(x, s)))(solve(diff(f, x), x)[0]))((x + 1)**2 - 4)", "standard", "y = (x − (−1))² + (−4), so the turning point is (−1, −4)."),
        mc("Compared with y = x², the graph of y = 3x² is:", ["wider", "narrower", "reflected in the x-axis", "translated 3 units up"], 1,
           diff="standard", expl="Each y-value is tripled, so the graph rises faster and looks narrower."),
    ]))

# ------------------------------------------------------------------ Year 10

T.append(topic(
    "qm_10_001", "Expanding and simplifying with index laws", "y10", ALG, "procedural",
    "Expand, simplify and solve using the distributive law together with the index laws.",
    ["Expands and collects like terms in longer expressions", "Combines index laws with expanding", "Solves linear equations with brackets"],
    [("AC9M10A01", "exact")],
    pre=[("qm_9_002", "hard", "Terms are simplified with the index laws"),
         ("qm_9_004", "hard", "Builds on expanding binomial products")], qs=[
        mc("Expand and simplify 3x(2x − 5) − x(x + 1).", ["5x² − 14x", "7x² − 16x", "5x² − 16x", "5x² − 15x + 1"], 2,
           "expand(3*x*(2*x - 5) - x*(x + 1))", expl="6x² − 15x − x² − x = 5x² − 16x."),
        mc("Simplify (2a³b)² × 3ab⁻¹.", ["12a⁷b", "6a⁷b", "12a⁶b", "12a⁷b³"], 0, "(2*a**3*b)**2 * 3*a*b**-1",
           expl="(2a³b)² = 4a⁶b², then × 3ab⁻¹ gives 12a⁷b."),
        num("Expand and simplify (x + 2)² − (x − 2)². What is the coefficient of x?", "8",
            "expand((x + 2)**2 - (x - 2)**2).coeff(x, 1)", "standard", "(x² + 4x + 4) − (x² − 4x + 4) = 8x."),
        num("Solve 3(2x − 1) − 2(x + 4) = 9.", "5", "solve(3*(2*x - 1) - 2*(x + 4) - 9, x)", "standard",
            "6x − 3 − 2x − 8 = 9, so 4x = 20 and x = 5."),
    ]))

T.append(topic(
    "qm_10_002", "Difference of two squares and perfect squares", "y10", ALG, "procedural",
    "Recognise and use a² − b² = (a − b)(a + b) and (a ± b)² = a² ± 2ab + b².",
    ["Factorises a difference of two squares", "Expands and recognises perfect squares", "Uses the identities for mental arithmetic"],
    [("AC9M10A01", "exact")],
    pre=[("qm_9_004", "hard", "Both identities are special cases of expanding binomial products")], qs=[
        mc("Factorise x² − 49.", ["(x − 7)²", "(x − 7)(x + 7)", "(x + 7)²", "(x − 49)(x + 1)"], 1, "x**2 - 49",
           expl="x² − 7² = (x − 7)(x + 7)."),
        mc("Expand (x − 5)².", ["x² − 10x + 25", "x² − 25", "x² + 25", "x² − 5x + 25"], 0, "expand((x - 5)**2)",
           expl="(x − 5)² = x² − 2(5)x + 25 = x² − 10x + 25."),
        mc("Factorise 9x² − 16.", ["(9x − 4)(x + 4)", "(3x − 4)²", "(3x − 8)(3x + 2)", "(3x − 4)(3x + 4)"], 3, "9*x**2 - 16",
           "standard", "9x² − 16 = (3x)² − 4² = (3x − 4)(3x + 4)."),
        num("Use a difference of two squares to evaluate 53² − 47².", "600", "53**2 - 47**2", "standard",
            "(53 − 47)(53 + 47) = 6 × 100 = 600."),
    ]))

T.append(topic(
    "qm_10_003", "Factorising non-monic quadratics", "y10", ALG, "procedural",
    "Factorise ax² + bx + c with a ≠ 1, taking out any common factor first.",
    ["Takes out a common factor first", "Factorises ax² + bx + c by splitting the middle term or by inspection"],
    [("AC9M10A01", "inferred")],
    pre=[("qm_9_006", "hard", "Extends the monic factorising method")], qs=[
        mc("Factorise 2x² + 7x + 3.", ["(2x + 3)(x + 1)", "(2x + 1)(x + 3)", "(2x + 1)(x + 7)", "(x + 1)(x + 3)"], 1,
           "2*x**2 + 7*x + 3", expl="(2x + 1)(x + 3) = 2x² + 6x + x + 3 = 2x² + 7x + 3."),
        mc("Fully factorise 2x² − 8x − 10.", ["(2x − 5)(x + 2)", "2(x + 5)(x − 1)", "(x − 5)(2x + 1)", "2(x − 5)(x + 1)"], 3,
           "2*x**2 - 8*x - 10", expl="Take out 2 first: 2(x² − 4x − 5) = 2(x − 5)(x + 1)."),
        mc("Factorise 3x² − 10x − 8.", ["(3x − 2)(x + 4)", "(3x + 2)(x − 4)", "(3x − 4)(x + 2)", "(3x + 4)(x − 2)"], 1,
           "3*x**2 - 10*x - 8", "standard", "(3x + 2)(x − 4) = 3x² − 12x + 2x − 8 = 3x² − 10x − 8."),
        num("6x² + x − 2 = (ax + 2)(bx − 1), where a and b are positive integers. Find a + b.", "5", "3 + 2", "standard",
            "(3x + 2)(2x − 1) = 6x² − 3x + 4x − 2 = 6x² + x − 2, so a = 3, b = 2."),
    ]))

T.append(topic(
    "qm_10_004", "Solving quadratic equations algebraically", "y10", ALG, "procedural",
    "Solve quadratic equations by factorising, including non-monic cases and the difference of two squares.",
    ["Chooses an appropriate factorisation", "Solves equations with fractional or zero roots", "Rearranges equations to = 0 first"],
    [("AC9M10A01", "exact")],
    pre=[("qm_9_009", "hard", "Uses the null factor law"),
         ("qm_10_003", "hard", "Many equations need non-monic factorising"),
         ("qm_10_002", "soft", "Some equations are a difference of two squares")], qs=[
        num("Solve 2x² − 18 = 0.", "3, -3", "solve(2*x**2 - 18, x)", "basic", "x² = 9, so x = ±3.", unordered=True),
        num("Solve x² + x − 12 = 0.", "-4, 3", "solve(x**2 + x - 12, x)", "basic", "(x + 4)(x − 3) = 0.", unordered=True),
        num("Solve 2x² + 7x + 3 = 0.", "-1/2, -3", "solve(2*x**2 + 7*x + 3, x)", "standard",
            "(2x + 1)(x + 3) = 0, so x = −1/2 or x = −3.", unordered=True),
        num("Solve x(x − 4) = 5.", "5, -1", "solve(x*(x - 4) - 5, x)", "standard",
            "x² − 4x − 5 = 0, (x − 5)(x + 1) = 0.", unordered=True),
    ]))

T.append(topic(
    "qm_10_005", "Simultaneous linear equations", "y10", ALG, "procedural",
    "Solve two linear equations in two unknowns by substitution or elimination, and interpret the solution as the intersection of two lines.",
    ["Solves by substitution", "Solves by elimination", "Interprets the solution as a point of intersection"],
    [("AC9M10A02", "exact")],
    pre=[("qm_9_007", "soft", "Lines and their gradients give the graphical meaning of a solution")], qs=[
        num("Solve y = 2x + 1 and y = x + 4. Write the solution as (x, y).", "(3, 7)", "(lambda s: (s[x], s[y]))(solve([y - 2*x - 1, y - x - 4], [x, y]))", "basic",
            "2x + 1 = x + 4 gives x = 3, then y = 7."),
        num("Solve x + y = 10 and x − y = 4. Write the solution as (x, y).", "(7, 3)", "(lambda s: (s[x], s[y]))(solve([x + y - 10, x - y - 4], [x, y]))", "basic",
            "Adding gives 2x = 14, so x = 7 and y = 3."),
        num("Solve 2x + 3y = 12 and x − y = 1. Write the solution as (x, y).", "(3, 2)",
            "(lambda s: (s[x], s[y]))(solve([2*x + 3*y - 12, x - y - 1], [x, y]))", "standard",
            "x = y + 1, so 2(y + 1) + 3y = 12, 5y = 10, y = 2 and x = 3."),
        num("Adult tickets cost $12 and child tickets cost $8. 20 tickets cost $200 in total. How many adult tickets were sold?",
            "10", "solve([a + c - 20, 12*a + 8*c - 200], [a, c])[a]", "standard",
            "a + c = 20 and 12a + 8c = 200. Substituting c = 20 − a gives 4a = 40, so a = 10."),
    ]))

T.append(topic(
    "qm_10_006", "Linear inequalities", "y10", ALG, "procedural",
    "Solve linear inequalities, reversing the inequality sign when multiplying or dividing by a negative number.",
    ["Solves inequalities with the same steps as equations", "Reverses the sign when multiplying or dividing by a negative"],
    [("AC9M10A02", "exact")], root_reason="Builds on solving linear equations (Year 7-8), which is not modelled in this graph.", qs=[
        mc("Solve 3x − 5 < 7.", ["x < 4", "x > 4", "x < 2/3", "x ≤ 4"], 0, expl="3x < 12, so x < 4."),
        mc("Solve −2x ≥ 6.", ["x ≥ −3", "x ≤ −3", "x ≤ 3", "x ≥ 3"], 1,
           expl="Dividing by −2 reverses the sign: x ≤ −3."),
        num("What is the smallest integer n that satisfies 5n + 2 > 3n + 11?", "5", "floor(Rational(9, 2)) + 1", "standard",
            "2n > 9, so n > 4.5. The smallest integer is 5."),
        mc("Solve (x − 1)/3 > 2 − x.", ["x < 7/4", "x > 5/4", "x > 7/2", "x > 7/4"], 3, diff="standard",
           expl="Multiply by 3: x − 1 > 6 − 3x, so 4x > 7 and x > 7/4."),
    ]))

# ------------------------------------------------------------------ Year 10 optional (post-Year 10 pathways)

OPT = "Number and algebra (optional)"

T.append(topic(
    "qm_10o_001", "Simplifying surds", "y10opt", OPT, "procedural",
    "Write √n in simplest form a√b by taking out the largest square factor.",
    ["Finds the largest square factor", "Writes a surd in simplest form", "Converts a√b back to √n"],
    [("acopt:N.01", "inferred")],
    pre=[("qm_9_001", "hard", "Surds are irrational square roots"),
         ("qm_9_002", "soft", "√(ab) = √a × √b parallels the index laws")], qs=[
        mc("Simplify √50.", ["2√5", "5√2", "25√2", "10√5"], 1, "sqrt(50)", expl="√50 = √25 × √2 = 5√2."),
        mc("Simplify √72.", ["4√2", "2√6", "6√2", "12√6"], 2, "sqrt(72)", expl="72 = 36 × 2, so √72 = 6√2."),
        num("√48 = a√3. Find a.", "4", "sqrt(48)/sqrt(3)", "standard", "√48 = √16 × √3 = 4√3."),
        mc("Write 3√5 as the square root of a single whole number.", ["√15", "√45", "√75", "√8"], 1, "3*sqrt(5)",
           "standard", "3√5 = √9 × √5 = √45."),
    ]))

T.append(topic(
    "qm_10o_002", "Adding, subtracting and multiplying surds", "y10opt", OPT, "procedural",
    "Collect like surds and expand products involving surds.",
    ["Simplifies before collecting like surds", "Multiplies surds using √a × √b = √(ab)", "Expands brackets containing surds"],
    [("acopt:N.01", "inferred")],
    pre=[("qm_10o_001", "hard", "Surds must be simplified before like surds can be collected"),
         ("qm_9_004", "soft", "Expanding surd brackets uses the same method as binomial products")], qs=[
        mc("Simplify 3√2 + 5√2.", ["8√4", "15√2", "8√2", "8"], 2, "3*sqrt(2) + 5*sqrt(2)", expl="Like surds: 3 + 5 = 8, so 8√2."),
        mc("Simplify √12 + √27.", ["5√3", "√39", "6√3", "13√3"], 0, "sqrt(12) + sqrt(27)", expl="2√3 + 3√3 = 5√3."),
        num("Expand and simplify (2 + √3)(2 − √3).", "1", "expand((2 + sqrt(3))*(2 - sqrt(3)))", "standard",
            "Difference of two squares: 4 − 3 = 1."),
        mc("Expand and simplify (1 + √5)².", ["6", "1 + 5√5", "6 + √5", "6 + 2√5"], 3, "expand((1 + sqrt(5))**2)",
           "standard", "1 + 2√5 + 5 = 6 + 2√5."),
    ]))

T.append(topic(
    "qm_10o_003", "Rationalising a single-surd denominator", "y10opt", OPT, "procedural",
    "Multiply by √b/√b to remove a surd from the denominator.",
    ["Rationalises a/√b", "Simplifies the result fully"],
    [("acopt:N.01", "inferred")],
    pre=[("qm_10o_002", "hard", "Uses multiplication and simplification of surds")], qs=[
        mc("Rationalise the denominator of 1/√3.", ["3/√3", "√3", "√3/3", "1/3"], 2, "1/sqrt(3)",
           expl="Multiply top and bottom by √3: √3/3."),
        mc("Rationalise and simplify 6/√2.", ["3√2", "6√2", "√2/6", "3"], 0, "6/sqrt(2)", expl="6√2/2 = 3√2."),
        mc("Simplify 10/√5 + √20.", ["2√5", "4√5", "√5", "10"], 1, "10/sqrt(5) + sqrt(20)", "standard",
           "10/√5 = 2√5 and √20 = 2√5, so the total is 4√5."),
        num("√2/√8 is a rational number. What is it?", "1/2", "sqrt(2)/sqrt(8)", "standard", "√(2/8) = √(1/4) = 1/2."),
    ]))

T.append(topic(
    "qm_10o_004", "Completing the square", "y10opt", OPT, "procedural",
    "Rewrite x² + bx + c as (x + b/2)² + k and use it to solve equations.",
    ["Adds and subtracts (b/2)²", "Writes a monic quadratic as (x + h)² + k", "Solves an equation by completing the square"],
    [("acopt:A.02", "inferred")],
    pre=[("qm_10_002", "hard", "Completing the square builds a perfect square"),
         ("qm_9_006", "soft", "Same coefficient reasoning as monic factorising")], qs=[
        num("What number must be added to x² + 8x to make a perfect square?", "16", "(Rational(8, 2))**2", "basic",
            "(8/2)² = 16, and x² + 8x + 16 = (x + 4)²."),
        mc("Write x² + 6x + 5 in the form (x + h)² + k.", ["(x + 3)² + 5", "(x + 3)² − 4", "(x + 6)² − 31", "(x − 3)² − 4"], 1,
           "x**2 + 6*x + 5", expl="x² + 6x + 9 − 9 + 5 = (x + 3)² − 4."),
        mc("Write x² − 4x − 1 in the form (x − h)² + k.", ["(x − 2)² − 1", "(x − 4)² − 17", "(x + 2)² − 5", "(x − 2)² − 5"], 3,
           "x**2 - 4*x - 1", "standard", "x² − 4x + 4 − 4 − 1 = (x − 2)² − 5."),
        mc("Solve x² + 2x − 2 = 0 by completing the square.", ["x = 1 ± √3", "x = −1 ± √3", "x = −1 ± √2", "x = −2 ± √3"], 1,
           "solve(x**2 + 2*x - 2, x)", "standard", "(x + 1)² − 3 = 0, so x + 1 = ±√3."),
    ]))

T.append(topic(
    "qm_10o_005", "The quadratic formula", "y10opt", OPT, "procedural",
    "Solve ax² + bx + c = 0 with x = (−b ± √(b² − 4ac))/(2a) and simplify the surd.",
    ["Identifies a, b and c with their signs", "Substitutes correctly into the formula", "Simplifies exact answers"],
    [("acopt:A.02", "inferred")],
    pre=[("qm_10o_004", "hard", "The formula is derived by completing the square"),
         ("qm_10o_001", "hard", "Exact answers need simplified surds")], qs=[
        num("For 2x² − 3x − 4 = 0, what is the value of b² − 4ac?", "41", "(-3)**2 - 4*2*(-4)", "basic",
            "(−3)² − 4(2)(−4) = 9 + 32 = 41."),
        mc("Solve x² − 4x + 1 = 0.", ["x = −2 ± √3", "x = 2 ± √3", "x = 4 ± √3", "x = 2 ± √5"], 1, "solve(x**2 - 4*x + 1, x)",
           expl="x = (4 ± √12)/2 = (4 ± 2√3)/2 = 2 ± √3."),
        mc("Solve 2x² + 2x − 1 = 0.", ["x = −1 ± √3", "x = (1 ± √3)/2", "x = (−1 ± √3)/2", "x = (−1 ± √5)/2"], 2,
           "solve(2*x**2 + 2*x - 1, x)", "standard", "x = (−2 ± √12)/4 = (−2 ± 2√3)/4 = (−1 ± √3)/2."),
        num("Solve 3x² − 5x − 1 = 0 and give the larger solution correct to 2 decimal places.", "1.85",
            "rnd((5 + sqrt(37))/6, 2)", "standard", "x = (5 ± √37)/6. The larger is (5 + 6.083)/6 ≈ 1.85.", tech="active"),
    ]))

T.append(topic(
    "qm_10o_006", "The discriminant and the number of real solutions", "y10opt", OPT, "reasoning",
    "Use Δ = b² − 4ac to decide whether a quadratic equation has two, one or no real solutions.",
    ["Calculates the discriminant", "Links the sign of Δ to the number of real solutions"],
    [("acopt:A.03", "inferred")],
    pre=[("qm_10o_005", "hard", "The discriminant is the expression under the square root in the formula")], qs=[
        num("Find the discriminant of x² + 3x + 5.", "-11", "3**2 - 4*1*5", "basic", "9 − 20 = −11."),
        mc("How many real solutions does x² − 6x + 9 = 0 have?", ["2", "1", "0", "infinitely many"], 1,
           "len(solve(x**2 - 6*x + 9, x))", expl="Δ = 36 − 36 = 0, so there is exactly one solution, x = 3."),
        mc("How many real solutions does 2x² + x + 3 = 0 have?", ["0", "1", "2", "3"], 0,
           "len([r for r in solve(2*x**2 + x + 3, x) if r.is_real])", "standard", "Δ = 1 − 24 = −23 < 0, so there are none."),
        mc("Which equation has two distinct real solutions?",
           ["x² + 2x + 1 = 0", "x² + 2x + 3 = 0", "x² + 2x − 1 = 0", "x² + 1 = 0"], 2, diff="standard",
           expl="Its discriminant is 4 + 4 = 8 > 0. The others give 0, −8 and −4."),
    ]))

T.append(topic(
    "qm_10o_007", "Turning point form and sketching parabolas", "y10opt", OPT, "conceptual",
    "Sketch y = a(x − h)² + k showing the turning point, intercepts and whether it is a maximum or minimum.",
    ["Reads the turning point and its nature", "Finds intercepts from turning point form", "Converts general form to turning point form"],
    [("acopt:A.04", "inferred")],
    pre=[("qm_10o_004", "hard", "Turning point form comes from completing the square"),
         ("qm_9_010", "hard", "Uses transformations of y = x²")], qs=[
        num("State the turning point of y = (x − 3)² + 2. Write it as (x, y).", "(3, 2)", "(lambda f: (lambda s: (s, f.subs(x, s)))(solve(diff(f, x), x)[0]))((x - 3)**2 + 2)", "basic",
            "h = 3 and k = 2."),
        mc("Describe the turning point of y = −(x + 1)² + 4.",
           ["minimum at (−1, 4)", "maximum at (1, 4)", "maximum at (−1, 4)", "minimum at (1, −4)"], 2,
           expl="a = −1 < 0 so the parabola opens down, and the turning point is a maximum at (−1, 4)."),
        num("Find the x-intercepts of y = (x − 1)² − 9.", "4, -2", "solve((x - 1)**2 - 9, x)", "standard",
            "(x − 1)² = 9, so x − 1 = ±3.", unordered=True),
        mc("Write y = x² − 8x + 10 in turning point form.", ["y = (x − 4)² + 10", "y = (x − 4)² − 6", "y = (x + 4)² − 6", "y = (x − 8)² − 54"], 1,
           "x**2 - 8*x + 10", "standard", "x² − 8x + 16 − 16 + 10 = (x − 4)² − 6."),
    ]))

# ------------------------------------------------------------------ Methods Unit 1 Topic 1

T.append(topic(
    "qm_m1_001", "Rationalising binomial surd denominators", "methods", MM1, "procedural",
    "Use the conjugate to rationalise denominators such as a + √b, and write results in the form p + q√r.",
    ["Identifies the conjugate", "Multiplies by conjugate over conjugate", "Simplifies to p + q√r"],
    [("qcaa25:MM.U1.T1.S1", "exact")], unit=1,
    pre=[("qm_10o_003", "hard", "Extends rationalising a single-surd denominator"),
         ("qm_10_002", "hard", "The conjugate product is a difference of two squares")], qs=[
        mc("What is the conjugate of 3 + √2?", ["3 − √2", "−3 + √2", "−3 − √2", "3 + √2"], 0, "3 - sqrt(2)",
           expl="Change the sign between the terms: 3 − √2."),
        mc("Rationalise 1/(√5 − 2).", ["√5 − 2", "√5 + 2", "(√5 + 2)/3", "(√5 + 2)/9"], 1, "1/(sqrt(5) - 2)",
           expl="Multiply by (√5 + 2)/(√5 + 2). The denominator is 5 − 4 = 1."),
        mc("Express 4/(3 − √5) in the form a + b√5.", ["12 + 4√5", "3 + √5", "3 − √5", "(3 + √5)/4"], 1, "4/(3 - sqrt(5))",
           "standard", "4(3 + √5)/(9 − 5) = 3 + √5."),
        mc("Simplify (√3 + 1)/(√3 − 1).", ["1 + √3", "4 + 2√3", "2 − √3", "2 + √3"], 3, "(sqrt(3) + 1)/(sqrt(3) - 1)",
           "standard", "(√3 + 1)²/(3 − 1) = (4 + 2√3)/2 = 2 + √3."),
    ]))

T.append(topic(
    "qm_m1_002", "Solving quadratic equations: choosing a method", "methods", MM1, "procedural",
    "Choose between factorising, square roots, completing the square and the formula, and give exact solutions.",
    ["Selects an efficient method", "Gives exact answers in simplest surd form", "Solves equations reducible to quadratics"],
    [("qcaa25:MM.U1.T1.S2", "exact")], unit=1,
    pre=[("qm_10_004", "hard", "Factorising methods"),
         ("qm_10o_005", "hard", "Quadratic formula for equations that do not factorise")], qs=[
        num("Solve (2x − 1)² = 9.", "2, -1", "solve((2*x - 1)**2 - 9, x)", "basic",
            "2x − 1 = ±3, so x = 2 or x = −1.", unordered=True),
        num("Solve x² = 7x.", "0, 7", "solve(x**2 - 7*x, x)", "basic", "x² − 7x = 0, x(x − 7) = 0.", unordered=True),
        mc("Solve x² + 6x + 4 = 0, giving exact answers.", ["x = 3 ± √5", "x = −3 ± √13", "x = −3 ± √5", "x = −6 ± √5"], 2,
           "solve(x**2 + 6*x + 4, x)", "standard", "(x + 3)² = 5, so x = −3 ± √5."),
        num("Solve 3x² − 2x − 8 = 0.", "2, -4/3", "solve(3*x**2 - 2*x - 8, x)", "standard",
            "(3x + 4)(x − 2) = 0.", unordered=True),
        num("Solve x⁴ − 5x² + 4 = 0.", "1, -1, 2, -2", "solve(x**4 - 5*x**2 + 4, x)", "advanced",
            "Let u = x²: u² − 5u + 4 = 0 gives u = 1 or 4, so x = ±1 or ±2.", unordered=True),
    ]))

T.append(topic(
    "qm_m1_003", "The discriminant with an unknown coefficient", "methods", MM1, "reasoning",
    "Find the values of a parameter that give a quadratic two, one or no real solutions.",
    ["Writes the discriminant in terms of the parameter", "Solves the resulting equation or inequality"],
    [("qcaa25:MM.U1.T1.S2", "exact")], unit=1,
    pre=[("qm_10o_006", "hard", "Uses the discriminant conditions"),
         ("qm_10_006", "hard", "The condition becomes an inequality to solve")], qs=[
        num("For x² + 6x + k = 0, find the value of k that gives exactly one real solution.", "9",
            "solve(6**2 - 4*k, k)", "basic", "36 − 4k = 0, so k = 9."),
        mc("The discriminant of kx² + 2x + 1 = 0 is:", ["4 + 4k", "4 − 4k", "2 − 4k", "4k − 4"], 1, "2**2 - 4*k*1",
           expl="b² − 4ac = 4 − 4k."),
        mc("For which values of k does x² − 4x + k = 0 have two distinct real solutions?", ["k > 4", "k ≤ 4", "k < 4", "k < 16"], 2,
           diff="standard", expl="16 − 4k > 0, so k < 4."),
        num("Find the positive value of m for which x² + mx + 16 = 0 has exactly one real solution.", "8",
            "max(solve(m**2 - 64, m))", "standard", "m² − 64 = 0, so m = ±8. The positive value is 8."),
    ]))

T.append(topic(
    "qm_m1_004", "Key features of a quadratic in general form", "methods", MM1, "procedural",
    "From y = ax² + bx + c, find intercepts, the axis of symmetry x = −b/(2a) and the turning point.",
    ["Finds the axis of symmetry", "Finds the turning point", "Finds all intercepts"],
    [("qcaa25:MM.U1.T1.S2", "exact")], unit=1,
    pre=[("qm_10o_007", "hard", "Connects the general form to turning point features"),
         ("qm_m1_002", "soft", "x-intercepts require solving the quadratic")], qs=[
        num("Find the axis of symmetry of y = x² − 10x + 7. Give the value of x.", "5", "Rational(10, 2)", "basic",
            "x = −b/(2a) = 10/2 = 5."),
        num("Find the y-intercept of y = 2x² − 3x + 5.", "5", "(2*x**2 - 3*x + 5).subs(x, 0)", "basic", "Put x = 0: y = 5."),
        num("Find the turning point of y = 2x² − 8x + 3. Write it as (x, y).", "(2, -5)",
            "(2, 2*2**2 - 8*2 + 3)", "standard", "x = 8/4 = 2, then y = 8 − 16 + 3 = −5."),
        mc("Where does y = −x² + 4x + 5 cross the x-axis?",
           ["x = 1 and x = −5", "x = −1 and x = −5", "x = −1 and x = 5", "x = 2 and x = 9"], 2,
           "solve(-x**2 + 4*x + 5, x)", "standard", "x² − 4x − 5 = 0, (x − 5)(x + 1) = 0."),
    ]))

T.append(topic(
    "qm_m1_005", "Finding a quadratic rule from given features", "methods", MM1, "reasoning",
    "Determine a quadratic's rule from its turning point, intercepts or points on the graph.",
    ["Chooses turning point form or intercept form to suit the information", "Solves for unknown coefficients"],
    [("qcaa25:MM.U1.T1.S2", "exact")], unit=1,
    pre=[("qm_10o_007", "hard", "Uses turning point form"),
         ("qm_10_005", "soft", "Two unknown coefficients can lead to simultaneous equations")], qs=[
        mc("A parabola has turning point (2, −3) and passes through (0, 1). Its equation is:",
           ["y = (x + 2)² − 3", "y = 2(x − 2)² − 3", "y = (x − 2)² + 1", "y = (x − 2)² − 3"], 3, "(x - 2)**2 - 3",
           expl="y = a(x − 2)² − 3. At (0, 1): 4a − 3 = 1, so a = 1."),
        num("A parabola has x-intercepts −1 and 3 and y-intercept −6. Find a in y = a(x + 1)(x − 3).", "2",
            "solve(k*(0 + 1)*(0 - 3) + 6, k)", "basic", "At x = 0: a(1)(−3) = −6, so a = 2."),
        num("y = x² + bx + c passes through (1, 0) and (3, 4). Find b and c, written as b = …, c = ….", "b=-2, c=1",
            "(lambda s: (s[b], s[c]))(solve([1 + b + c, 9 + 3*b + c - 4], [b, c]))", "standard",
            "1 + b + c = 0 and 9 + 3b + c = 4. Subtracting: 8 + 2b = 4, so b = −2 and c = 1."),
        num("A parabola with turning point (−1, 4) passes through (1, 0). Find a in y = a(x + 1)² + 4.", "-1",
            "solve(k*(1 + 1)**2 + 4, k)", "standard", "4a + 4 = 0, so a = −1."),
    ]))

T.append(topic(
    "qm_m1_006", "Intersections of a line and a parabola", "methods", MM1, "procedural",
    "Find where a line meets a parabola by substitution, and use the discriminant to count intersections.",
    ["Substitutes to form a quadratic equation", "Solves for the intersection points", "Uses the discriminant to decide tangency"],
    [("qcaa25:MM.U1.T1.S2", "exact")], unit=1,
    pre=[("qm_m1_002", "hard", "The intersection condition is a quadratic equation"),
         ("qm_10_005", "soft", "Same substitution idea as simultaneous linear equations"),
         ("qm_m1_003", "soft", "Tangency is a discriminant condition")], qs=[
        num("Find the x-coordinates where y = x² and y = x + 2 meet.", "2, -1", "solve(x**2 - x - 2, x)", "basic",
            "x² = x + 2, x² − x − 2 = 0, (x − 2)(x + 1) = 0.", unordered=True),
        num("Find the x-coordinates where y = x² − 2x and y = 2x − 3 meet.", "1, 3", "solve(x**2 - 4*x + 3, x)", "basic",
            "x² − 2x = 2x − 3 gives x² − 4x + 3 = 0.", unordered=True),
        mc("How many times does the line y = 2x − 5 meet the parabola y = x² − 4x + 4?", ["0", "1", "2", "3"], 1,
           "len(solve(x**2 - 4*x + 4 - (2*x - 5), x))", "standard",
           "x² − 6x + 9 = 0 has Δ = 0, so the line is a tangent and meets the parabola once."),
        num("For what value of c is the line y = 4x + c a tangent to y = x²?", "-4", "solve(16 + 4*c, c)", "advanced",
            "x² − 4x − c = 0 needs Δ = 16 + 4c = 0, so c = −4."),
    ]))

T.append(topic(
    "qm_m1_007", "Quadratic models: maximum and minimum problems", "methods", MM1, "application",
    "Build a quadratic model from a situation and use its turning point to find a maximum or minimum.",
    ["Writes a quadratic model from a description", "Finds and interprets the turning point in context"],
    [("qcaa25:MM.U1.T1.S2", "exact")], unit=1,
    pre=[("qm_m1_004", "hard", "The optimum is the turning point")], qs=[
        num("Find the maximum value of y = −x² + 6x − 5.", "4", "(lambda t: -t**2 + 6*t - 5)(3)", "basic",
            "Axis x = 3, so y = −9 + 18 − 5 = 4."),
        num("A ball's height is h = −5t² + 20t metres after t seconds. What is its maximum height in metres?", "20",
            "(lambda t: -5*t**2 + 20*t)(2)", "basic", "The maximum is at t = 20/10 = 2, where h = −20 + 40 = 20."),
        num("Two numbers add to 30. What is the largest possible value of their product?", "225",
            "(lambda t: t*(30 - t))(15)", "standard", "P = n(30 − n) has its maximum at n = 15, giving 225."),
        num("A farmer has 40 m of fencing to make a rectangular pen against a long wall, so only three sides need fencing. What is the largest possible area in m²?",
            "200", "(lambda w: w*(40 - 2*w))(10)", "standard",
            "Area = w(40 − 2w). The maximum is at w = 10, giving 10 × 20 = 200 m²."),
    ]))
