"""Mathematical Methods Unit 4 (Year 12): Further calculus, trigonometry and statistics.

AI-drafted from the QCAA Mathematical Methods 2025 syllabus. Not reviewed by a teacher.
"""
from qlib import topic, num, mc

T1 = "T1 Further integration"
T2 = "T2 Trigonometry"
T3 = "T3 Continuous random variables and the normal distribution"
T4 = "T4 Sampling and proportions"
T5 = "T5 Interval estimates for proportions"


def S(t, s):
    return [("qcaa25:MM.U4.T%d.S%d" % (t, s), "exact")]


T = []

# ------------------------------------------------------------------ T1 Further integration

T.append(topic(
    "qm_m4_001", "Estimating area with rectangles", "methods", T1, "procedural",
    "Estimate the area under a curve with sums of rectangles using left or right endpoints.",
    ["Calculates left and right endpoint sums", "Explains why more rectangles improve the estimate"],
    S(1, 1), unit=4,
    pre=[("qm_m3_012", "soft", "Integration and area are linked later by the fundamental theorem")], qs=[
        num("Estimate the area under y = x² from x = 0 to x = 2 using 2 rectangles of width 1 and left endpoints.", "1", "0**2 + 1**2", "basic",
            "Heights f(0) = 0 and f(1) = 1."),
        num("Estimate the area under y = x² from x = 0 to x = 2 using 2 rectangles of width 1 and right endpoints.", "5", "1**2 + 2**2", "basic",
            "Heights f(1) = 1 and f(2) = 4."),
        mc("As the number of rectangles increases (and their width shrinks), the sum:", ["approaches the exact area", "always increases",
                                                                                          "always decreases", "stays the same"], 0,
           diff="standard", expl="The definite integral is the limit of these sums."),
        num("Estimate the area under y = 1/x from x = 1 to x = 3 with 4 rectangles of width 0.5 using right endpoints.", "0.95",
            "Rational(1, 2)*sum(1/(1 + Rational(k, 2)) for k in range(1, 5))", "standard", "0.5 × (1/1.5 + 1/2 + 1/2.5 + 1/3) = 0.95."),
    ]))

T.append(topic(
    "qm_m4_002", "The fundamental theorem and definite integrals", "methods", T1, "procedural",
    "Evaluate definite integrals with ∫ₐᵇ f(x) dx = F(b) − F(a).",
    ["Finds an anti-derivative", "Substitutes the limits correctly", "Evaluates exact values with e, ln and π"],
    S(1, 1), unit=4,
    pre=[("qm_m3_013", "hard", "Standard anti-derivatives"), ("qm_m3_014", "hard", "Linear composites"), ("qm_m4_001", "soft", "Area as a limit of sums")], qs=[
        num("Evaluate ∫₀² 3x² dx.", "8", "integrate(3*x**2, (x, 0, 2))", "basic", "[x³] from 0 to 2 = 8."),
        num("Evaluate ∫₁³ (2x + 1) dx.", "10", "integrate(2*x + 1, (x, 1, 3))", "basic", "[x² + x] = 12 − 2."),
        num("Evaluate ∫₀^π sin x dx.", "2", "integrate(sin(x), (x, 0, pi))", "standard", "[−cos x] = 1 − (−1)."),
        mc("Evaluate ∫₀¹ e^(2x) dx.", ["e² − 1", "(e² − 1)/2", "2e²", "(e² + 1)/2"], 1, "integrate(exp(2*x), (x, 0, 1))", "standard",
           "[e^(2x)/2] from 0 to 1."),
    ]))

T.append(topic(
    "qm_m4_003", "Area between a curve and the x-axis", "methods", T1, "procedural",
    "Find areas bounded by a curve and the x-axis, splitting the integral where the curve crosses the axis.",
    ["Finds where the curve crosses the axis", "Splits the integral at each crossing", "Adds absolute values of the parts"],
    S(1, 2), unit=4,
    pre=[("qm_m4_002", "hard", "Definite integrals"), ("qm_m1_011", "soft", "Finding intercepts and sketching")], qs=[
        num("Find the area between y = x² and the x-axis from x = 0 to x = 3.", "9", "integrate(x**2, (x, 0, 3))", "basic", "[x³/3] = 9."),
        num("Find the area enclosed by y = 4 − x² and the x-axis.", "32/3", "integrate(4 - x**2, (x, -2, 2))", "basic", "Intercepts ±2; [4x − x³/3] from −2 to 2."),
        num("Find the area enclosed by y = x(x − 2) and the x-axis.", "4/3", "-integrate(x*(x - 2), (x, 0, 2))", "standard",
            "The curve is below the axis between 0 and 2; the integral is −4/3."),
        num("Find the total area between y = x³ and the x-axis from x = −1 to x = 2.", "17/4",
            "-integrate(x**3, (x, -1, 0)) + integrate(x**3, (x, 0, 2))", "standard", "1/4 below the axis plus 4 above."),
    ]))

T.append(topic(
    "qm_m4_004", "Area between two curves", "methods", T1, "procedural",
    "Find the area between two curves by integrating (upper − lower) between their intersections.",
    ["Finds intersection points", "Identifies the upper curve", "Integrates the difference"],
    S(1, 2), unit=4,
    pre=[("qm_m4_003", "hard", "Area with definite integrals"), ("qm_m1_006", "soft", "Finding where curves meet")], qs=[
        num("Find the area between y = x and y = x² from x = 0 to x = 1.", "1/6", "integrate(x - x**2, (x, 0, 1))", "basic", "∫(x − x²) = 1/2 − 1/3."),
        num("Find the area enclosed by y = 4 and y = x².", "32/3", "integrate(4 - x**2, (x, -2, 2))", "basic", "They meet at x = ±2."),
        num("Find the area enclosed by y = x² and y = x + 2.", "9/2", "integrate(x + 2 - x**2, (x, -1, 2))", "standard",
            "They meet at x = −1 and 2; integrate (x + 2 − x²)."),
        mc("Find the area between y = cos x and y = sin x from x = 0 to x = π/4.", ["√2", "√2 − 1", "1", "2 − √2"], 1,
           "integrate(cos(x) - sin(x), (x, 0, pi/4))", "standard", "[sin x + cos x] from 0 to π/4 = √2 − 1."),
    ]))

T.append(topic(
    "qm_m4_005", "The trapezoidal rule", "methods", T1, "procedural",
    "Approximate definite integrals with the trapezoidal rule and judge over- or underestimates.",
    ["Applies the trapezoidal rule with equal strips", "Explains over- and underestimates from concavity"],
    S(1, 2), unit=4, tech="either",
    pre=[("qm_m4_001", "hard", "Area estimates with strips")], qs=[
        num("Use the trapezoidal rule with 2 strips to estimate ∫₀² x² dx.", "3", "Rational(1, 2)*(0 + 2*1 + 4)", "basic", "h/2 × (f₀ + 2f₁ + f₂) = ½(0 + 2 + 4)."),
        num("A trapezium has parallel sides 3 and 5 and width 2. Find its area.", "8", "Rational(1, 2)*(3 + 5)*2", "basic", "½ × (3 + 5) × 2."),
        num("Use the trapezoidal rule with 4 strips to estimate ∫₀⁴ √x dx, correct to 2 decimal places.", "5.15",
            "rnd(Rational(1, 2)*(sqrt(0) + 2*(sqrt(1) + sqrt(2) + sqrt(3)) + sqrt(4)), 2)", "standard",
            "½(0 + 2(1 + 1.414 + 1.732) + 2) ≈ 5.15.", tech="active"),
        mc("For a curve that is concave up over the interval, the trapezoidal rule:", ["underestimates the integral", "overestimates the integral",
                                                                                        "is exact", "could over- or underestimate"], 1,
           diff="standard", expl="The straight tops of the trapezia lie above a concave-up curve."),
    ]))

T.append(topic(
    "qm_m4_006", "Total change and motion with definite integrals", "methods", T1, "application",
    "Find total change by integrating a rate, and displacement and distance travelled from velocity.",
    ["Integrates a rate over an interval", "Distinguishes displacement from distance", "Splits the integral where velocity changes sign"],
    S(1, 2), unit=4,
    pre=[("qm_m4_002", "hard", "Definite integrals"), ("qm_m3_016", "hard", "Motion with anti-derivatives")], qs=[
        num("Water flows into a tank at r(t) = 2t + 3 L/min. How many litres flow in from t = 0 to t = 4?", "28", "integrate(2*t + 3, (t, 0, 4))", "basic",
            "[t² + 3t] = 16 + 12."),
        num("v(t) = 3t² m/s. Find the displacement from t = 0 to t = 2.", "8", "integrate(3*t**2, (t, 0, 2))", "basic", "[t³] = 8 m."),
        num("v(t) = t − 2 m/s for 0 ≤ t ≤ 4. Find the total distance travelled.", "4", "integrate(Abs(t - 2), (t, 0, 4))", "standard",
            "2 m backwards then 2 m forwards."),
        num("v(t) = t − 2 m/s. Find the displacement from t = 0 to t = 4.", "0", "integrate(t - 2, (t, 0, 4))", "standard", "The two parts cancel."),
    ]))

# ------------------------------------------------------------------ T2 Trigonometry

T.append(topic(
    "qm_m4_007", "The sine rule and the ambiguous case", "methods", T2, "procedural",
    "Use the sine rule to find sides and angles, including the ambiguous case with two possible triangles.",
    ["Uses the sine rule for sides and angles", "Recognises when two triangles are possible", "Finds both angles in the ambiguous case"],
    S(2, 1), unit=4, tech="active",
    pre=[("qm_10o_013", "hard", "Introduces the sine rule")], qs=[
        num("In triangle ABC, A = 30°, B = 45° and a = 5. Find b to 2 decimal places.", "7.07", "rnd(5*sin(pi/4)/sin(pi/6), 2)", "basic",
            "b = 5 sin 45° ÷ sin 30°.", tech="active"),
        mc("The sine rule states:", ["a/sin A = b/sin B", "a sin A = b sin B", "a/sin B = b/sin A", "a² = b² + c² − 2bc cos A"], 0,
           expl="Each side over the sine of its opposite angle is constant."),
        mc("In triangle ABC, A = 30°, a = 6 and b = 10. How many triangles are possible?", ["0", "1", "2", "3"], 2, diff="standard",
           expl="sin B = 10 × 0.5 ÷ 6 ≈ 0.833, so B ≈ 56.4° or 123.6°, and both fit with A = 30°."),
        num("In triangle ABC, A = 40°, a = 8 and b = 10. Find the acute value of B to the nearest degree.", "53",
            "rnd(asin(10*sin(40*pi/180)/8)*180/pi, 0)", "standard", "sin B = 10 sin 40° ÷ 8 ≈ 0.80.", tech="active"),
    ]))

T.append(topic(
    "qm_m4_008", "The cosine rule and the area rule", "methods", T2, "procedural",
    "Use a² = b² + c² − 2bc cos A and Area = ½bc sin A.",
    ["Finds a side with the cosine rule", "Finds an angle from three sides", "Finds area with ½bc sin A"],
    S(2, 1), unit=4, tech="either",
    pre=[("qm_10o_013", "hard", "Introduces the cosine rule")], qs=[
        num("In triangle ABC, b = 3, c = 4 and A = 90°. Use the cosine rule to find a².", "25", "3**2 + 4**2 - 2*3*4*cos(pi/2)", "basic",
            "cos 90° = 0, so it reduces to Pythagoras."),
        num("Find the area of a triangle with sides 8 and 5 and an included angle of 150°.", "10", "Rational(1, 2)*8*5*sin(5*pi/6)", "basic",
            "½ × 40 × sin 150° = 20 × ½."),
        num("In triangle ABC, b = 7, c = 10 and A = 50°. Find a to 2 decimal places.", "7.68", "rnd(sqrt(49 + 100 - 140*cos(50*pi/180)), 2)", "standard",
            "a² = 149 − 140 cos 50° ≈ 59.0.", tech="active"),
        num("A triangle has sides 5, 7 and 8. Find the angle opposite the side of length 7, in degrees.", "60",
            "acos(Rational(25 + 64 - 49, 2*5*8))*180/pi", "standard", "cos θ = (25 + 64 − 49)/80 = 1/2."),
    ]))

T.append(topic(
    "qm_m4_009", "Trigonometry problems with bearings and in 3D", "methods", T2, "application",
    "Solve two- and three-dimensional problems with bearings, elevation and depression using the sine and cosine rules.",
    ["Draws and labels a diagram from bearings", "Chooses the right triangle and rule", "Works in three dimensions"],
    S(2, 1), unit=4, tech="active",
    pre=[("qm_m4_007", "hard", "Sine rule"), ("qm_m4_008", "hard", "Cosine rule"), ("qm_10_009", "hard", "Bearings, elevation and depression")], qs=[
        num("A boat sails 8 km east and then 6 km north. How far is it from its start?", "10", "sqrt(8**2 + 6**2)", "basic", "√(64 + 36).", tech="free"),
        mc("A true bearing of 135° points:", ["south-east", "north-east", "south-west", "north-west"], 0, expl="Halfway between east (090°) and south (180°)."),
        num("Ship A sails 10 km on a bearing of 040°T and ship B sails 15 km on a bearing of 130°T from the same port. How far apart are they, to 1 decimal place?",
            "18.0", "rnd(sqrt(10**2 + 15**2 - 2*10*15*cos(pi/2)), 1)", "standard", "The angle between the paths is 90°, so √(100 + 225) ≈ 18.0 km.",
            tech="active"),
        num("A box measures 3 cm × 4 cm × 12 cm. Find the length of its space diagonal.", "13", "sqrt(3**2 + 4**2 + 12**2)", "standard",
            "√(9 + 16 + 144) = 13 cm.", tech="free"),
    ]))

# ------------------------------------------------------------------ T3 Continuous random variables and the normal distribution

T.append(topic(
    "qm_m4_010", "Continuous random variables and probability density functions", "methods", T3, "conceptual",
    "Use probability density functions, with probabilities as areas under the curve found by integration.",
    ["Checks a pdf integrates to 1", "Finds probabilities by integrating", "Knows P(X = a) = 0"],
    S(3, 1), unit=4,
    pre=[("qm_m4_002", "hard", "Probabilities are definite integrals"), ("qm_m3_017", "soft", "Discrete random variables")], qs=[
        num("f(x) = kx for 0 ≤ x ≤ 2 (and 0 elsewhere) is a probability density function. Find k.", "1/2", "solve(integrate(k*x, (x, 0, 2)) - 1, k)",
            "basic", "∫₀² kx dx = 2k = 1."),
        num("f(x) = x/2 for 0 ≤ x ≤ 2. Find P(X ≤ 1).", "1/4", "integrate(x/2, (x, 0, 1))", "basic", "[x²/4] from 0 to 1."),
        num("f(x) = 3x² for 0 ≤ x ≤ 1. Find P(0.5 ≤ X ≤ 1).", "7/8", "integrate(3*x**2, (x, Rational(1, 2), 1))", "standard", "1 − 1/8."),
        mc("For a continuous random variable X, P(X = 1) is:", ["f(1)", "0", "1", "undefined"], 1, diff="standard",
           expl="The area over a single point is 0."),
    ]))

T.append(topic(
    "qm_m4_011", "Mean and variance of a continuous random variable", "methods", T3, "procedural",
    "Calculate E(X) = ∫x f(x) dx and Var(X) = E(X²) − [E(X)]².",
    ["Calculates E(X) by integration", "Calculates Var(X) and the standard deviation"],
    S(3, 1), unit=4,
    pre=[("qm_m4_010", "hard", "Works with the pdf"), ("qm_m3_019", "soft", "Same formulas as the discrete case")], qs=[
        num("f(x) = x/2 for 0 ≤ x ≤ 2. Find E(X).", "4/3", "integrate(x*x/2, (x, 0, 2))", "basic", "∫ x²/2 dx = 8/6."),
        num("f(x) = 3x² for 0 ≤ x ≤ 1. Find E(X).", "3/4", "integrate(x*3*x**2, (x, 0, 1))", "basic", "∫ 3x³ dx = 3/4."),
        num("f(x) = 3x² for 0 ≤ x ≤ 1. Find Var(X).", "3/80", "integrate(x**2*3*x**2, (x, 0, 1)) - integrate(x*3*x**2, (x, 0, 1))**2", "standard",
            "E(X²) = 3/5, so 3/5 − 9/16 = 3/80."),
        num("X is uniform on [0, 10], so f(x) = 1/10. Find E(X).", "5", "integrate(x/10, (x, 0, 10))", "standard", "The midpoint, 5."),
    ]))

T.append(topic(
    "qm_m4_012", "Standardised scores (z-scores)", "methods", T3, "procedural",
    "Calculate z = (x − μ)/σ and use z-scores to compare values from different distributions.",
    ["Calculates z-scores", "Converts back from z to x", "Compares relative standing"],
    S(3, 1), unit=4,
    pre=[("qm_10o_014", "hard", "Mean and standard deviation")], qs=[
        num("μ = 70 and σ = 5. Find the z-score of x = 80.", "2", "(80 - 70)/Integer(5)", "basic", "(80 − 70)/5."),
        num("μ = 50 and σ = 8. Find x when z = −1.5.", "38", "50 + Rational(-3, 2)*8", "basic", "50 − 12."),
        mc("A student scores 75 in Maths (mean 65, standard deviation 5) and 80 in English (mean 70, standard deviation 10). In which did they do better relative to the class?",
           ["English", "Maths", "Equally well", "Cannot tell"], 1, diff="standard", expl="z = 2 in Maths and z = 1 in English."),
        num("μ = 100 and σ = 15. Find the z-score of x = 91.", "-0.6", "(91 - 100)/Integer(15)", "standard", "−9/15."),
    ]))

T.append(topic(
    "qm_m4_013", "Features of the normal distribution", "methods", T3, "conceptual",
    "Describe the normal curve N(μ, σ²) and use the 68–95–99.7% rule for quick estimates.",
    ["Reads μ and σ from N(μ, σ²)", "Uses the 68–95–99.7% rule", "Recognises symmetry about the mean"],
    S(3, 2), unit=4,
    pre=[("qm_m4_012", "hard", "Distances from the mean in standard deviations"), ("qm_m4_010", "soft", "Normal is a continuous distribution")], qs=[
        num("X ~ N(50, 16), so σ = 4. Approximately what percentage of values lie between 46 and 54?", "68", "rnd(100*(Phi(1) - Phi(-1)), 0)", "basic",
            "46 to 54 is within 1 standard deviation of the mean."),
        num("X ~ N(50, 16), so σ = 4. Approximately what percentage of values lie above 58?", "2.5", "Rational(100 - 95, 2)", "basic",
            "58 is 2σ above the mean; 5% lie beyond ±2σ, half of it above."),
        mc("In a normal distribution, the mean, median and mode:", ["are all different", "are all equal", "satisfy mean > median", "satisfy median > mode"], 1,
           diff="standard", expl="The curve is symmetric with a single peak at the mean."),
        num("X ~ N(100, 225), so σ = 15. Approximately what percentage of values lie between 85 and 130?", "81.5", "Rational(68, 2) + Rational(95, 2)",
            "standard", "85 to 100 is 34%, and 100 to 130 is 47.5%."),
    ]))

T.append(topic(
    "qm_m4_014", "Normal probabilities and quantiles", "methods", T3, "procedural",
    "Use technology to calculate normal probabilities and the value with a given probability below it.",
    ["Calculates P(a < X < b) with technology", "Finds quantiles (inverse normal)", "Standardises to compare with the standard normal"],
    S(3, 2), unit=4, tech="active",
    pre=[("qm_m4_013", "hard", "Understands the normal model")], qs=[
        mc("Z ~ N(0, 1). P(Z < 1) is approximately:", ["0.3413", "0.8413", "0.1587", "0.6827"], 1, "rnd(Phi(1), 4)",
           expl="Half the area (0.5) plus the area from 0 to 1 (0.3413).", tech="free"),
        mc("Z ~ N(0, 1). P(−1.96 < Z < 1.96) is approximately:", ["0.975", "0.90", "0.95", "0.99"], 2, "rnd(Phi(Rational(196, 100)) - Phi(Rational(-196, 100)), 2)",
           expl="1.96 is the standard 95% value.", tech="free"),
        num("X ~ N(60, 25), so σ = 5. Find P(X > 67) correct to 4 decimal places.", "0.0808", "rnd(1 - Phi(Rational(7, 5)), 4)", "standard",
            "z = 1.4 and 1 − 0.9192 = 0.0808.", tech="active"),
        num("X ~ N(500, 100²). Find k such that P(X < k) = 0.9, to the nearest whole number.", "628",
            "rnd(500 + 100*sqrt(2)*erfinv(Rational(4, 5)), 0)", "standard", "z ≈ 1.2816, so k ≈ 500 + 128.2.", tech="active"),
    ]))

# ------------------------------------------------------------------ T4 Sampling and proportions

T.append(topic(
    "qm_m4_015", "Random sampling and bias", "methods", T4, "conceptual",
    "Describe random samples, sources of bias, and procedures that make a sample random.",
    ["Identifies simple random samples", "Names sources of sampling bias", "Explains why larger samples vary less"],
    S(4, 1), unit=4,
    pre=[("qm_10_011", "soft", "Describing and comparing data")], qs=[
        mc("Which is a simple random sample of a school's students?", ["Drawing 50 student ID numbers at random from all IDs", "Surveying the first 50 students at the canteen",
                                                                       "Asking for volunteers in an online poll", "Surveying 50 students from one class"], 0,
           expl="Every student has the same chance of being chosen."),
        mc("An online poll on a sports website asks whether sport should get more funding. It is likely to be biased because:",
           ["respondents choose themselves and are interested in sport", "the sample is too random", "online polls are always unbiased", "the population is too small"], 0,
           expl="Self-selected samples over-represent people with strong views."),
        mc("To reduce the variation between sample results, you should:", ["decrease the sample size", "increase the sample size", "use volunteers", "survey only one group"], 1,
           diff="standard", expl="Larger random samples give less variable estimates."),
        mc("A sample statistic is:", ["a value calculated from a sample to estimate a population parameter", "a fixed property of the population",
                                      "always equal to the population value", "the size of the sample"], 0, diff="standard",
           expl="Statistics vary from sample to sample; parameters are fixed."),
    ]))

T.append(topic(
    "qm_m4_016", "The sample proportion", "methods", T4, "procedural",
    "Treat the sample proportion p̂ as a random variable with mean p and standard deviation √(p(1 − p)/n).",
    ["Calculates p̂ from a sample", "Calculates the mean and standard deviation of p̂", "Explains how n affects the spread"],
    S(4, 2), unit=4,
    pre=[("qm_m3_020", "hard", "Each response is a Bernoulli trial"), ("qm_m4_015", "soft", "Random samples")], qs=[
        num("In a random sample of 200 people, 46 say yes. Find the sample proportion p̂.", "0.23", "Rational(46, 200)", "basic", "46 ÷ 200."),
        num("The population proportion is p = 0.4 and n = 100. What is the mean of p̂?", "0.4", "Rational(4, 10)", "basic", "E(p̂) = p."),
        mc("The population proportion is p = 0.4 and n = 100. The standard deviation of p̂ is:", ["0.24", "√(0.0024)", "√0.24", "0.0024"], 1,
           "sqrt(Rational(4, 10)*Rational(6, 10)/100)", "standard", "√(0.4 × 0.6 ÷ 100) = √0.0024 ≈ 0.049."),
        num("If the sample size is multiplied by 4, the standard deviation of p̂ is multiplied by:", "1/2", "1/sqrt(4)", "standard",
            "It depends on 1/√n."),
    ]))

T.append(topic(
    "qm_m4_017", "Approximate normality of the sample proportion", "methods", T4, "conceptual",
    "Use the approximately normal distribution of p̂ for large samples to estimate probabilities.",
    ["Knows when the normal approximation is reasonable", "Standardises p̂", "Estimates probabilities for p̂"],
    S(4, 2), unit=4, tech="either",
    pre=[("qm_m4_016", "hard", "Mean and standard deviation of p̂"), ("qm_m4_014", "hard", "Normal probabilities")], qs=[
        mc("For large random samples, the distribution of p̂ is approximately:", ["uniform", "normal", "Bernoulli", "exponential"], 1,
           expl="Repeated sampling gives a bell-shaped distribution of p̂."),
        mc("The normal approximation for p̂ works best when:", ["n is large and p is not close to 0 or 1", "n is small", "p is close to 0", "p = 1"], 0,
           expl="Both np and n(1 − p) should be reasonably large."),
        num("p = 0.5 and n = 100. Standardise p̂ = 0.6: find z.", "2", "(Rational(6, 10) - Rational(1, 2))/sqrt(Rational(1, 4)/100)", "standard",
            "The standard deviation is 0.05, so z = 0.1/0.05."),
        num("p = 0.5 and n = 100. Find the approximate value of P(p̂ > 0.6), to 3 decimal places.", "0.023", "rnd(1 - Phi(2), 3)", "standard",
            "z = 2, and 1 − 0.977 ≈ 0.023.", tech="active"),
    ]))

# ------------------------------------------------------------------ T5 Interval estimates for proportions

T.append(topic(
    "qm_m4_018", "Confidence intervals for a proportion", "methods", T5, "procedural",
    "Calculate an approximate confidence interval p̂ ± z√(p̂(1 − p̂)/n) for a population proportion.",
    ["Calculates p̂ and its standard error", "Uses the right z for the confidence level", "States the interval"],
    S(5, 1), unit=4, tech="either",
    pre=[("qm_m4_017", "hard", "Uses the normal approximation for p̂")], qs=[
        num("In a random sample of 400, 100 support a policy. Find p̂.", "0.25", "Rational(100, 400)", "basic", "100 ÷ 400."),
        mc("An approximate 95% confidence interval uses z ≈", ["1.645", "1.96", "2.576", "1"], 1, "rnd(sqrt(2)*erfinv(Rational(95, 100)), 2)",
           expl="95% of the standard normal lies between −1.96 and 1.96."),
        mc("n = 400 and p̂ = 0.25. Find the approximate 95% confidence interval for p, to 3 decimal places.",
           ["(0.229, 0.271)", "(0.208, 0.292)", "(0.236, 0.264)", "(0.150, 0.350)"], 1, diff="standard",
           expl="Standard error √(0.25 × 0.75/400) ≈ 0.0217; 1.96 × 0.0217 ≈ 0.042.", tech="active"),
        num("A 95% confidence interval for p is (0.31, 0.39). What was p̂?", "0.35", "(Rational(31, 100) + Rational(39, 100))/2", "standard",
            "The interval is centred on p̂."),
    ]))

T.append(topic(
    "qm_m4_019", "Margin of error, confidence level and sample size", "methods", T5, "reasoning",
    "Relate the margin of error to the confidence level and sample size, and find the sample size needed for a given margin.",
    ["Calculates the margin of error", "Explains the effect of confidence level and n", "Finds a required sample size"],
    S(5, 1), unit=4, tech="either",
    pre=[("qm_m4_018", "hard", "The margin is half the interval width")], qs=[
        num("A confidence interval is (0.31, 0.39). What is the margin of error?", "0.04", "(Rational(39, 100) - Rational(31, 100))/2", "basic",
            "Half the width."),
        mc("For the same sample, increasing the confidence level from 95% to 99% makes the interval:", ["narrower", "wider", "the same", "shift to the right"], 1,
           expl="A larger z is needed."),
        num("To halve the margin of error, the sample size must be multiplied by:", "4", "(2)**2", "standard", "The margin depends on 1/√n."),
        num("Using p̂ = 0.5 and z = 1.96, find the smallest sample size giving a margin of error of at most 0.05.", "385",
            "ceiling((Rational(196, 100)*sqrt(Rational(1, 4))/Rational(5, 100))**2)", "standard", "n ≥ (1.96 × 0.5 ÷ 0.05)² = 384.16, so 385.",
            tech="active"),
    ]))

T.append(topic(
    "qm_m4_020", "Interpreting confidence intervals", "methods", T5, "reasoning",
    "Interpret confidence intervals correctly, including that they vary between samples and that most, but not all, contain p.",
    ["States the repeated-sampling meaning of 95% confidence", "Uses an interval to judge a claim", "Expects some intervals to miss p"],
    S(5, 1), unit=4,
    pre=[("qm_m4_018", "hard", "Knows how intervals are built")], qs=[
        mc("A 95% confidence interval for p is (0.42, 0.50). Which statement is correct?",
           ["If many samples were taken, about 95% of such intervals would contain p", "There is a 95% chance that p equals 0.46",
            "95% of people have values between 0.42 and 0.50", "p̂ is between 0.42 and 0.50 with probability 0.95"], 0,
           expl="Confidence describes the method over repeated samples."),
        mc("Twenty random samples each give a 95% confidence interval for p. About how many would you expect to contain p?", ["20", "19", "1", "10"], 1,
           expl="95% of 20 is 19."),
        mc("A council claims 60% of residents support a plan. A survey gives a 95% confidence interval of (0.48, 0.56). The best conclusion is:",
           ["The data do not support the claim, because 0.60 is outside the interval", "The claim is supported",
            "The interval proves exactly 52% support", "Nothing can be concluded"], 0, diff="standard",
           expl="0.60 is not a plausible value given this interval."),
        num("1000 samples are taken and a 90% confidence interval is built from each. About how many intervals are expected NOT to contain p?", "100",
            "1000*Rational(10, 100)", "standard", "10% of 1000."),
    ]))
