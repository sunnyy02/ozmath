"""Year 9, Year 10 and optional Year 10 topics that Mathematical Methods builds on,
beyond the algebra in pilot_quadratics.py. 16 topics.

AI-drafted. Not reviewed by a teacher.
"""
from qlib import topic, num, mc

ROOT_Y9 = "Year 9 is the lowest level in this graph; Year 7-8 assumed knowledge is not modelled."
OPT = "Number and algebra (optional)"
OPT_M = "Measurement and statistics (optional)"

T = []

# ------------------------------------------------------------------ Year 9

T.append(topic(
    "qm_9_011", "Pythagoras' theorem", "y9", "Measurement", "procedural",
    "Use a² + b² = c² to find a missing side of a right-angled triangle and to test for right angles.",
    ["Identifies the hypotenuse", "Finds the hypotenuse or a shorter side", "Applies the theorem in context"],
    [("AC9M9M03", "exact")], root_reason=ROOT_Y9, qs=[
        num("A right-angled triangle has shorter sides 6 and 8. Find the hypotenuse.", "10", "sqrt(6**2 + 8**2)", "basic", "√(36 + 64) = √100 = 10."),
        num("A right-angled triangle has hypotenuse 13 and one side 5. Find the other side.", "12", "sqrt(13**2 - 5**2)", "basic", "√(169 − 25) = √144 = 12."),
        mc("Which side lengths form a right-angled triangle?", ["4, 5, 6", "5, 12, 13", "6, 7, 9", "3, 5, 7"], 1, diff="standard",
           expl="5² + 12² = 25 + 144 = 169 = 13²."),
        num("A 5 m ladder reaches 4 m up a vertical wall. How far is its foot from the wall, in metres?", "3", "sqrt(5**2 - 4**2)", "standard",
            "√(25 − 16) = 3 m."),
    ]))

T.append(topic(
    "qm_9_012", "Trigonometric ratios in right-angled triangles", "y9", "Measurement", "procedural",
    "Use sine, cosine and tangent to find unknown sides and angles in right-angled triangles.",
    ["Labels opposite, adjacent and hypotenuse", "Chooses the right ratio", "Finds a side or angle with a calculator"],
    [("AC9M9SP01", "exact"), ("AC9M9M03", "exact")], tech="either",
    pre=[("qm_9_011", "soft", "Right-angled triangle side names and relationships")], qs=[
        num("In a right-angled triangle the side opposite θ is 3 and the hypotenuse is 5. Find sin θ.", "3/5", "Rational(3, 5)", "basic",
            "sin θ = opposite/hypotenuse = 3/5."),
        mc("In a right-angled triangle, tan θ equals:", ["opposite/adjacent", "adjacent/opposite", "opposite/hypotenuse", "adjacent/hypotenuse"], 0,
           expl="tan θ = opposite ÷ adjacent."),
        num("The hypotenuse is 10 and the angle is 35°. Find the side opposite the angle, correct to 1 decimal place.", "5.7",
            "rnd(10*sin(35*pi/180), 1)", "standard", "10 sin 35° ≈ 5.74, so 5.7.", tech="active"),
        num("tan θ = 0.75. Find θ to the nearest degree.", "37", "rnd(atan(Rational(3, 4))*180/pi, 0)", "standard",
            "θ = tan⁻¹(0.75) ≈ 36.9°, so 37°.", tech="active"),
    ]))

T.append(topic(
    "qm_9_013", "Scientific notation", "y9", "Measurement", "procedural",
    "Write very large and very small numbers as a × 10ⁿ with 1 ≤ a < 10, and convert back.",
    ["Converts to and from scientific notation", "Uses negative powers of 10 for small numbers", "Multiplies and divides in scientific notation"],
    [("AC9M9M02", "exact")],
    pre=[("qm_9_003", "hard", "Small numbers need negative powers of 10")], qs=[
        mc("Write 0.00052 in scientific notation.", ["5.2 × 10⁻⁴", "5.2 × 10⁻³", "5.2 × 10⁻⁵", "5.2 × 10⁴"], 0, "Rational(52, 100000)",
           expl="Move the decimal point 4 places right: 5.2 × 10⁻⁴."),
        num("Write 3.1 × 10⁵ as an ordinary number.", "310000", "Rational(31, 10)*10**5", "basic", "Move the decimal point 5 places right."),
        mc("Calculate (4 × 10³) × (6 × 10⁵) in scientific notation.", ["2.4 × 10⁸", "2.4 × 10⁹", "2.4 × 10¹⁵", "1.0 × 10⁹"], 1,
           "(4*10**3)*(6*10**5)", "standard", "4 × 6 = 24 and 10³ × 10⁵ = 10⁸, so 24 × 10⁸ = 2.4 × 10⁹."),
        num("(9 × 10⁻²) ÷ (3 × 10⁴) = a × 10ⁿ in scientific notation. Find n.", "-6",
            "floor(log(Rational(9, 100)/30000, 10))", "standard", "9 ÷ 3 = 3 and 10⁻² ÷ 10⁴ = 10⁻⁶, so 3 × 10⁻⁶."),
    ]))

T.append(topic(
    "qm_9_014", "Compound events with and without replacement", "y9", "Probability", "procedural",
    "List outcomes of two-step experiments with tables or tree diagrams and find probabilities, with and without replacement.",
    ["Lists a sample space for two steps", "Multiplies along tree branches", "Adjusts probabilities when items are not replaced"],
    [("AC9M9P01", "exact")], root_reason=ROOT_Y9, qs=[
        num("Two fair coins are tossed. Find P(two heads).", "1/4", "Rational(1, 2)**2", "basic", "One outcome (HH) out of four equally likely."),
        num("A fair die is rolled twice. Find P(the sum is 7).", "1/6",
            "Rational(len([1 for i in range(1, 7) for j in range(1, 7) if i + j == 7]), 36)", "basic", "6 of the 36 outcomes add to 7."),
        num("A bag has 3 red and 2 blue balls. Two are drawn without replacement. Find P(both red).", "3/10",
            "Rational(3, 5)*Rational(2, 4)", "standard", "3/5 × 2/4 = 6/20 = 3/10."),
        num("A bag has 3 red and 2 blue balls. Two are drawn with replacement. Find P(both red).", "9/25",
            "Rational(3, 5)**2", "standard", "3/5 × 3/5 = 9/25."),
    ]))

T.append(topic(
    "qm_9_015", "Venn diagrams and relative frequency", "y9", "Probability", "procedural",
    "Use Venn diagrams for 'and' and 'or' events and estimate probabilities from relative frequencies.",
    ["Fills a two-set Venn diagram from counts", "Distinguishes inclusive and exclusive 'or'", "Estimates probability by relative frequency"],
    [("AC9M9P02", "exact")],
    pre=[("qm_9_014", "soft", "Builds on basic probability of events")], qs=[
        num("In a class of 30, 18 play sport, 12 play music and 5 do both. How many do neither?", "5", "30 - (18 + 12 - 5)", "basic",
            "18 + 12 − 5 = 25 do at least one, so 5 do neither."),
        num("A spinner landed on red 37 times in 200 spins. Estimate P(red) as a decimal.", "0.185", "Rational(37, 200)", "basic",
            "37 ÷ 200 = 0.185."),
        num("In a class of 30, 18 play sport, 12 play music and 5 do both. A student is chosen at random. Find P(sport or music).",
            "5/6", "Rational(18 + 12 - 5, 30)", "standard", "25 of 30 students, so 25/30 = 5/6."),
        num("In a class of 30, 18 play sport, 12 play music and 5 do both. Find P(music only).", "7/30", "Rational(12 - 5, 30)", "standard",
            "12 − 5 = 7 play only music."),
    ]))

# ------------------------------------------------------------------ Year 10

T.append(topic(
    "qm_10_007", "Exponential relations and equations", "y10", "Algebra", "conceptual",
    "Recognise and graph y = aˣ and solve simple exponential equations by writing both sides with the same base.",
    ["Evaluates aˣ for integer x", "Describes the shape and y-intercept of y = aˣ", "Solves equations such as 2ˣ⁺¹ = 32"],
    [("AC9M10A03", "exact")],
    pre=[("qm_9_002", "hard", "Uses the index laws"), ("qm_9_003", "hard", "Negative x gives negative exponents")], qs=[
        num("For y = 2ˣ, find y when x = −3.", "1/8", "Integer(2)**-3", "basic", "2⁻³ = 1/8."),
        num("Solve 3ˣ = 81.", "4", "solve(3**x - 81, x)", "basic", "81 = 3⁴."),
        mc("Which describes the graph of y = 3ˣ?", ["passes through (0, 1) and increases", "passes through (0, 3) and increases",
                                                    "passes through (1, 0) and increases", "passes through (0, 1) and decreases"], 0,
           diff="standard", expl="3⁰ = 1, and 3ˣ grows as x increases."),
        num("Solve 2ˣ⁺¹ = 32.", "4", "solve(2**(x + 1) - 32, x)", "standard", "32 = 2⁵, so x + 1 = 5."),
    ]))

T.append(topic(
    "qm_10_008", "Exponential growth and decay models", "y10", "Algebra", "application",
    "Model growth and decay, including compound interest and depreciation, with A = P(1 ± r)ⁿ.",
    ["Writes a growth or decay rule from a percentage rate", "Calculates compound interest", "Interprets the base as the growth factor"],
    [("AC9M10A04", "exact")], tech="either",
    pre=[("qm_10_007", "hard", "Models use exponential relations")], qs=[
        num("$1000 is invested at 5% p.a. compounded annually. What is it worth after 2 years, in dollars?", "1102.5",
            "1000*Rational(105, 100)**2", "basic", "1000 × 1.05² = 1102.50."),
        mc("A $20 000 car loses 15% of its value each year. Which rule gives its value after n years?",
           ["V = 20000(0.85)ⁿ", "V = 20000(1.15)ⁿ", "V = 20000 − 0.15n", "V = 20000(0.15)ⁿ"], 0,
           expl="Keeping 85% each year means multiplying by 0.85."),
        num("A population of 500 doubles every 3 years. What is it after 12 years?", "8000", "500*2**(12//3)", "standard",
            "12 years is 4 doublings: 500 × 2⁴ = 8000."),
        num("$5000 is invested at 6% p.a. compounded monthly for 3 years. Find its value to the nearest cent.", "5983.40",
            "rnd(5000*(1 + Rational(6, 1200))**36, 2)", "standard", "5000 × 1.005³⁶ ≈ 5983.40.", tech="active"),
    ]))

T.append(topic(
    "qm_10_009", "Trigonometry with elevation, depression and bearings", "y10", "Measurement", "application",
    "Solve practical right-angled triangle problems involving angles of elevation and depression and true bearings.",
    ["Draws a diagram from a description", "Uses angles of elevation and depression", "Uses three-figure true bearings"],
    [("AC9M10M03", "exact")], tech="active",
    pre=[("qm_9_012", "hard", "Uses the trigonometric ratios")], qs=[
        num("From 50 m away on level ground, the angle of elevation to the top of a tree is 30°. Find the tree's height to 1 decimal place.",
            "28.9", "rnd(50*tan(pi/6), 1)", "basic", "h = 50 tan 30° ≈ 28.9 m.", tech="active"),
        mc("A true bearing of 090° points:", ["east", "north", "south", "west"], 0, expl="Bearings are measured clockwise from north; 90° is east."),
        num("A ship sails 20 km on a bearing of 060°T. How far east has it travelled, to 1 decimal place?", "17.3",
            "rnd(20*sin(pi/3), 1)", "standard", "East component = 20 sin 60° ≈ 17.3 km.", tech="active"),
        num("From the top of a 40 m cliff, the angle of depression to a boat is 25°. How far is the boat from the base of the cliff, to 1 decimal place?",
            "85.8", "rnd(40/tan(25*pi/180), 1)", "standard", "d = 40 ÷ tan 25° ≈ 85.8 m.", tech="active"),
    ]))

TABLE = ("Of 100 students, 40 are in Year 10 and play sport, 20 are in Year 10 and do not, "
         "25 are in Year 11 and play sport, and 15 are in Year 11 and do not. ")

T.append(topic(
    "qm_10_010", "Conditional probability language and two-way tables", "y10", "Probability", "procedural",
    "Read conditional statements ('given', 'knowing that') and find conditional probabilities from two-way tables.",
    ["Builds a two-way table from counts", "Restricts the sample space for 'given' statements", "Translates words into P(A | B) notation"],
    [("AC9M10P01", "exact"), ("AC9M10ST04", "exact")],
    pre=[("qm_9_015", "hard", "Builds on 'and' and 'or' events and relative frequency")], qs=[
        num(TABLE + "Find P(plays sport | Year 10).", "2/3", "Rational(40, 40 + 20)", "basic", "40 of the 60 Year 10 students."),
        num(TABLE + "Find P(Year 10 | plays sport).", "8/13", "Rational(40, 40 + 25)", "basic", "40 of the 65 who play sport."),
        mc("'Given that it rains, the match is cancelled with probability 0.8.' In symbols:",
           ["P(cancelled | rain) = 0.8", "P(rain | cancelled) = 0.8", "P(rain and cancelled) = 0.8", "P(cancelled) = 0.8"], 0,
           diff="standard", expl="The condition (rain) goes after the bar."),
        num(TABLE + "Find P(Year 11 and does not play sport).", "3/20", "Rational(15, 100)", "standard", "15 of 100."),
    ]))

T.append(topic(
    "qm_10_011", "Comparing distributions with box plots", "y10", "Statistics", "procedural",
    "Find the five-number summary, interquartile range and outliers, and compare data sets using box plots.",
    ["Finds median and quartiles", "Calculates the IQR and outlier fences", "Compares centre and spread of two box plots"],
    [("AC9M10ST02", "exact")], root_reason="Earlier statistics (Years 7-9) is not modelled in this graph.", qs=[
        num("Find the median of 3, 5, 7, 8, 12, 15, 20.", "8", "median([3, 5, 7, 8, 12, 15, 20])", "basic", "The middle (4th) value is 8."),
        num("A data set has Q1 = 12 and Q3 = 20. Find the interquartile range.", "8", "20 - 12", "basic", "IQR = Q3 − Q1 = 8."),
        num("A data set has Q1 = 12 and Q3 = 20. Find the upper fence for outliers, Q3 + 1.5 × IQR.", "32", "20 + Rational(3, 2)*(20 - 12)",
            "standard", "20 + 1.5 × 8 = 32."),
        mc("Box plot A has median 50 and IQR 10. Box plot B has median 50 and IQR 25. Which is true?",
           ["B is more spread out", "A is more spread out", "B has a higher centre", "They have the same spread"], 0, diff="standard",
           expl="Same median, but B's middle 50% covers a wider range."),
    ]))

# ------------------------------------------------------------------ Year 10 optional

T.append(topic(
    "qm_10o_008", "Rational exponents", "y10opt", OPT, "procedural",
    "Interpret a^(m/n) as the nth root of aᵐ and evaluate or simplify with fractional and negative exponents.",
    ["Converts between roots and fractional exponents", "Evaluates a^(m/n) for perfect powers", "Applies index laws with fractional exponents"],
    [("acopt:A.01", "inferred")],
    pre=[("qm_9_003", "hard", "Extends negative and zero exponents"), ("qm_10o_001", "soft", "Roots and surds")], qs=[
        num("Evaluate 8^(1/3).", "2", "Integer(8)**Rational(1, 3)", "basic", "The cube root of 8 is 2."),
        num("Evaluate 16^(3/4).", "8", "Integer(16)**Rational(3, 4)", "basic", "Fourth root of 16 is 2, and 2³ = 8."),
        num("Evaluate 27^(−2/3).", "1/9", "Integer(27)**Rational(-2, 3)", "standard", "27^(2/3) = 3² = 9, so the answer is 1/9."),
        mc("Write √(x³) with a fractional exponent.", ["x^(2/3)", "x^(3/2)", "x^(1/6)", "x^(−3/2)"], 1, "x**Rational(3, 2)", "standard",
           "The square root is the power 1/2, so (x³)^(1/2) = x^(3/2)."),
    ]))

T.append(topic(
    "qm_10o_009", "Logarithms: definition and laws", "y10opt", OPT, "procedural",
    "Use logₐ y = x ⇔ aˣ = y and the product, quotient and power laws of logarithms.",
    ["Converts between index and log form", "Evaluates simple logarithms", "Combines logarithms with the laws"],
    [("acopt:A.07", "inferred")],
    pre=[("qm_10_007", "hard", "A logarithm is an exponent"), ("qm_10o_008", "soft", "Fractional answers such as log₄ 2 = 1/2")], qs=[
        num("Evaluate log₂ 32.", "5", "log(32, 2)", "basic", "2⁵ = 32."),
        num("Evaluate log₁₀ 0.001.", "-3", "log(Rational(1, 1000), 10)", "basic", "10⁻³ = 0.001."),
        num("Simplify log₃ 18 − log₃ 2.", "2", "log(18, 3) - log(2, 3)", "standard", "log₃(18/2) = log₃ 9 = 2."),
        mc("Write logₐ 5 + 2 logₐ 3 as a single logarithm.", ["logₐ 45", "logₐ 30", "logₐ 11", "logₐ 15"], 0, diff="standard",
           expl="2 logₐ 3 = logₐ 9, and logₐ 5 + logₐ 9 = logₐ 45."),
    ]))

T.append(topic(
    "qm_10o_010", "Polynomials: the factor and remainder theorems", "y10opt", OPT, "procedural",
    "Use P(a) to find the remainder on division by (x − a), and to find and use linear factors of cubics.",
    ["Evaluates P(a) for the remainder", "Finds a factor by testing values", "Fully factorises a cubic"],
    [("acopt:A.06", "inferred")],
    pre=[("qm_10_003", "hard", "Factorising the quadratic that remains"), ("qm_9_004", "soft", "Expanding to check")], qs=[
        num("Find the remainder when P(x) = x³ − 2x + 5 is divided by (x − 2).", "9", "(x**3 - 2*x + 5).subs(x, 2)", "basic",
            "P(2) = 8 − 4 + 5 = 9."),
        mc("Which is a factor of x³ − 6x² + 11x − 6?", ["x + 1", "x − 1", "x + 2", "x + 3"], 1, diff="basic",
           expl="P(1) = 1 − 6 + 11 − 6 = 0, so x − 1 is a factor."),
        num("x − 3 is a factor of x³ + kx − 6. Find k.", "-7", "solve(3**3 + 3*k - 6, k)", "standard", "27 + 3k − 6 = 0, so k = −7."),
        mc("Fully factorise x³ − 4x² + x + 6.", ["(x − 1)(x + 2)(x − 3)", "(x + 1)(x − 2)(x − 3)", "(x + 1)(x + 2)(x − 3)", "(x − 1)(x − 2)(x + 3)"], 1,
           "x**3 - 4*x**2 + x + 6", "standard", "P(−1) = 0, and dividing by (x + 1) leaves x² − 5x + 6 = (x − 2)(x − 3)."),
    ]))

T.append(topic(
    "qm_10o_011", "Circles and hyperbolas", "y10opt", OPT, "conceptual",
    "Graph circles (x − h)² + (y − k)² = r² and hyperbolas y = a/(x − h) + k, identifying centre, radius and asymptotes.",
    ["Reads centre and radius", "Completes the square to find a circle's centre", "Identifies hyperbola asymptotes"],
    [("acopt:A.05", "inferred")],
    pre=[("qm_10o_004", "hard", "Completing the square puts a circle in standard form"), ("qm_9_007", "soft", "Distance formula underlies the circle equation")], qs=[
        mc("Find the centre and radius of (x − 2)² + (y + 1)² = 9.", ["centre (2, −1), radius 3", "centre (−2, 1), radius 3",
                                                                  "centre (2, −1), radius 9", "centre (−2, 1), radius 9"], 0,
           expl="Compare with (x − h)² + (y − k)² = r²: h = 2, k = −1, r = 3."),
        mc("What are the asymptotes of y = 1/x + 2?", ["x = 0 and y = 2", "x = 2 and y = 0", "x = 0 and y = 0", "x = −2 and y = 2"], 0,
           expl="1/x is undefined at x = 0, and y approaches 2 as x grows."),
        num("Find the radius of x² + y² − 6x + 4y − 3 = 0.", "4", "sqrt(3 + 9 + 4)", "standard", "(x − 3)² + (y + 2)² = 3 + 9 + 4 = 16."),
        num("Find the x-values where y = 6/x meets y = x + 1.", "2, -3", "solve(6/x - x - 1, x)", "standard",
            "6 = x² + x, so x² + x − 6 = 0 and x = 2 or −3.", unordered=True),
    ]))

T.append(topic(
    "qm_10o_012", "The unit circle and exact values", "y10opt", OPT_M, "conceptual",
    "Define sine, cosine and tangent of any angle with the unit circle, use quadrant signs, and recall exact values for 30°, 45° and 60°.",
    ["Recalls exact values", "Uses symmetry to find values in all quadrants", "States the sign of each ratio by quadrant"],
    [("acopt:M.02", "inferred")],
    pre=[("qm_9_012", "hard", "Extends right-triangle ratios"), ("qm_9_011", "soft", "Exact values come from special triangles")], qs=[
        mc("sin 30° =", ["√3/2", "1/2", "√2/2", "1"], 1, "sin(pi/6)", expl="Half of an equilateral triangle gives sin 30° = 1/2."),
        mc("cos 150° =", ["√3/2", "−1/2", "−√3/2", "1/2"], 2, "cos(5*pi/6)", expl="150° is in quadrant 2, where cosine is negative: −cos 30°."),
        mc("tan 225° =", ["1", "−1", "√3", "−√3"], 0, "tan(5*pi/4)", "standard", "225° is in quadrant 3, where tangent is positive: tan 45° = 1."),
        mc("In which quadrant is sin θ positive and cos θ negative?", ["first", "second", "third", "fourth"], 1, diff="standard",
           expl="In quadrant 2, y > 0 and x < 0."),
    ]))

T.append(topic(
    "qm_10o_013", "The sine and cosine rules", "y10opt", OPT_M, "procedural",
    "Use the sine rule, cosine rule and ½ab sin C for non-right-angled triangles.",
    ["Chooses the sine or cosine rule", "Finds a side or angle", "Finds an area with ½ab sin C"],
    [("acopt:M.01", "inferred")], tech="active",
    pre=[("qm_9_012", "hard", "Uses sine and cosine of angles"), ("qm_10_009", "soft", "Practical triangle problems")], qs=[
        num("In triangle ABC, b = 5, c = 8 and A = 60°. Find a².", "49", "5**2 + 8**2 - 2*5*8*cos(pi/3)", "basic",
            "a² = 25 + 64 − 80 × 0.5 = 49.", tech="free"),
        num("Find the area of a triangle with sides 6 and 10 and an included angle of 30°.", "15", "Rational(1, 2)*6*10*sin(pi/6)", "basic",
            "½ × 6 × 10 × ½ = 15.", tech="free"),
        num("In triangle ABC, A = 40°, B = 65° and a = 10. Find b to 1 decimal place.", "14.1",
            "rnd(10*sin(65*pi/180)/sin(40*pi/180), 1)", "standard", "b = 10 sin 65° ÷ sin 40° ≈ 14.1.", tech="active"),
        num("A triangle has sides 7, 8 and 9. Find its largest angle to the nearest degree.", "73",
            "rnd(acos(Rational(49 + 64 - 81, 2*7*8))*180/pi, 0)", "standard",
            "The largest angle is opposite 9: cos C = (49 + 64 − 81)/112, so C ≈ 73°.", tech="active"),
    ]))

T.append(topic(
    "qm_10o_014", "Standard deviation", "y10opt", OPT_M, "procedural",
    "Calculate and interpret the standard deviation as a measure of spread about the mean.",
    ["Calculates the mean and standard deviation", "Interprets a larger standard deviation", "Knows how shifts and scalings change it"],
    [("acopt:ST.01", "inferred")],
    pre=[("qm_10_011", "soft", "Spread measured by the IQR first")], qs=[
        num("Find the mean of 2, 4, 4, 4, 5, 5, 7, 9.", "5", "mean([2, 4, 4, 4, 5, 5, 7, 9])", "basic", "Sum 40, divided by 8."),
        num("Find the population standard deviation of 2, 4, 4, 4, 5, 5, 7, 9.", "2", "sqrt(pvariance([2, 4, 4, 4, 5, 5, 7, 9]))", "basic",
            "Squared deviations from 5 sum to 32; 32/8 = 4 and √4 = 2."),
        mc("Every value in a data set is increased by 10. The standard deviation:", ["stays the same", "increases by 10", "is multiplied by 10", "increases by 100"], 0,
           diff="standard", expl="Shifting every value moves the mean too, so the deviations do not change."),
        mc("Data sets A and B have the same mean. A has standard deviation 2 and B has 8. Which is true?",
           ["B's values are more spread out from the mean", "A's values are more spread out", "B has larger values", "A has more values"], 0,
           diff="standard", expl="A larger standard deviation means values are typically further from the mean."),
    ]))
