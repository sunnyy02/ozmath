#!/usr/bin/env python3
"""Write data/standards.json: the curriculum layer every topic maps to.

Sources and their status
------------------------
* AC v9.0 Years 9 and 10 (codes AC9M9.., AC9M10..)
  Text here is a SHORT PARAPHRASE (verbatim: false). It was transcribed from the
  QCAA "Comparison of AC v8.4 to v9.0" documents, which could not be copied word
  for word. Replace it with the official wording by running
  `scripts/ingest_mrac.py <mrac-mathematics.jsonld>`, which keeps ids and
  only overwrites `text` and sets `verbatim: true`.

* AC v9.0 "Optional content for post-Year 10 Mathematics pathways"
  v9.0 has no coded 10A strand any more; ACARA publishes optional content as a
  support DOCX without codes. The `acopt:` ids below are ours, the list is
  INFERRED from common 10A/pathway content and must be checked against that DOCX.

* QCAA 2025 senior syllabuses (General, Methods, Specialist) at unit/topic level,
  titles from the official syllabus PDFs. Methods also has sub-topics (kind
  "subtopic", official titles, notional hours) with a one-line PARAPHRASE of
  their subject matter (`verbatim: false`). General and Specialist sub-topics are
  not yet ingested; see docs/sources.md.

Run:  python3 scripts/standards_seed.py
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "data", "standards.json")

AC_SOURCE = "AC v9.0 Mathematics (paraphrase via QCAA comparison docs, June 2023)"

Y9 = [
    ("AC9M9N01", "Number", "Recognise that the real number system includes rational and irrational numbers; solve problems with real numbers using digital tools."),
    ("AC9M9A01", "Algebra", "Apply the exponent laws to numerical expressions with integer exponents and extend to variables."),
    ("AC9M9A02", "Algebra", "Simplify algebraic expressions, expand binomial products and factorise monic quadratic expressions."),
    ("AC9M9A03", "Algebra", "Find the distance, gradient and midpoint of line segments on the Cartesian plane."),
    ("AC9M9A04", "Algebra", "Identify and graph quadratic functions; solve quadratic equations graphically and numerically, including with digital tools."),
    ("AC9M9A05", "Algebra", "Use mathematical modelling to solve problems involving change, choosing between linear and quadratic functions."),
    ("AC9M9A06", "Algebra", "Experiment with the effects of varying parameters on graphs of related functions, using digital tools."),
    ("AC9M9M01", "Measurement", "Solve problems involving the volume and surface area of right prisms and cylinders."),
    ("AC9M9M02", "Measurement", "Express very small and very large measurements and time scales in scientific notation."),
    ("AC9M9M03", "Measurement", "Solve spatial problems using angle properties, scale, similarity, Pythagoras' theorem and trigonometry."),
    ("AC9M9M04", "Measurement", "Calculate and interpret absolute, relative and percentage errors in measurement."),
    ("AC9M9M05", "Measurement", "Use mathematical modelling to solve problems involving direct proportion, rates, ratio and scale."),
    ("AC9M9SP01", "Space", "Use similar right-angled triangles to explain why sine, cosine and tangent ratios are constant."),
    ("AC9M9SP02", "Space", "Apply the enlargement transformation and describe what changes and what stays the same."),
    ("AC9M9SP03", "Space", "Design, test and refine algorithms based on geometric constructions, using digital tools."),
    ("AC9M9ST01", "Statistics", "Analyse how survey data was obtained in reports, including possible sources of bias."),
    ("AC9M9ST02", "Statistics", "Explain how sampling methods and representations can affect survey results."),
    ("AC9M9ST03", "Statistics", "Compare the distributions of multiple numerical data sets."),
    ("AC9M9ST04", "Statistics", "Choose and justify appropriate data displays for the data and question."),
    ("AC9M9ST05", "Statistics", "Plan and conduct statistical investigations involving samples of a population."),
    ("AC9M9P01", "Probability", "List all outcomes of compound events with and without replacement and determine probabilities."),
    ("AC9M9P02", "Probability", "Use relative frequencies to estimate probabilities of 'and', inclusive 'or' and exclusive 'or' events."),
    ("AC9M9P03", "Probability", "Design and conduct repeated experiments and simulations comparing simple and compound events."),
]

Y10 = [
    ("AC9M10N01", "Number", "Recognise the effect of approximations of real numbers in repeated calculations and compare with exact results."),
    ("AC9M10A01", "Algebra", "Expand, factorise and simplify expressions and solve equations algebraically, applying exponent laws and the distributive property."),
    ("AC9M10A02", "Algebra", "Solve linear inequalities and simultaneous linear equations in two variables; interpret solutions graphically."),
    ("AC9M10A03", "Algebra", "Connect algebraic and graphical representations of exponential relations; solve related exponential equations."),
    ("AC9M10A04", "Algebra", "Use mathematical modelling for growth and decay, using linear, quadratic and exponential functions, including financial contexts."),
    ("AC9M10A05", "Algebra", "Experiment with functions and relations using digital tools, making and testing conjectures."),
    ("AC9M10M01", "Measurement", "Solve problems involving the surface area and volume of composite objects."),
    ("AC9M10M02", "Measurement", "Interpret and use logarithmic scales in applied contexts."),
    ("AC9M10M03", "Measurement", "Solve practical problems with Pythagoras' theorem and trigonometry, including bearings and angles of elevation and depression."),
    ("AC9M10M04", "Measurement", "Identify the impact of measurement errors on the accuracy of results."),
    ("AC9M10M05", "Measurement", "Use mathematical modelling to solve problems involving proportion and scaling."),
    ("AC9M10SP01", "Space", "Use deductive reasoning to prove results about plane shapes and apply theorems to solve spatial problems."),
    ("AC9M10SP02", "Space", "Interpret networks and describe connectedness in situations."),
    ("AC9M10SP03", "Space", "Design, test and refine solutions to spatial problems using algorithms and digital tools."),
    ("AC9M10ST01", "Statistics", "Analyse claims, inferences and conclusions in statistical reports in the media, including possible bias."),
    ("AC9M10ST02", "Statistics", "Compare distributions of continuous numerical data using displays including boxplots; discuss centre, spread, shape and outliers."),
    ("AC9M10ST03", "Statistics", "Construct scatterplots and comment on the association between two numerical variables."),
    ("AC9M10ST04", "Statistics", "Construct two-way tables and discuss possible relationships between categorical variables."),
    ("AC9M10ST05", "Statistics", "Plan and conduct statistical investigations of bivariate data and report findings."),
    ("AC9M10P01", "Probability", "Use the language of conditional probability ('if ... then', 'given', 'knowing that') to describe and interpret situations."),
    ("AC9M10P02", "Probability", "Design and conduct repeated chance experiments and simulations with digital tools to model conditional probability."),
]

# Optional content for post-Year 10 pathways (ids are ours; INFERRED list)
OPT = [
    ("acopt:N.01", "Number", "Define rational and irrational numbers; simplify surds and perform operations with surds, including rationalising denominators."),
    ("acopt:A.01", "Algebra", "Use rational exponents and connect them with roots."),
    ("acopt:A.02", "Algebra", "Factorise non-monic quadratics; solve quadratic equations by completing the square and the quadratic formula."),
    ("acopt:A.03", "Algebra", "Use the discriminant to determine the number of real solutions of a quadratic equation."),
    ("acopt:A.04", "Algebra", "Sketch parabolas in turning-point form and identify key features."),
    ("acopt:A.05", "Algebra", "Graph and describe circles, hyperbolas and exponential relations; solve simple equations involving them."),
    ("acopt:A.06", "Algebra", "Investigate polynomials: add, subtract, multiply; use the remainder and factor theorems."),
    ("acopt:A.07", "Algebra", "Define logarithms and use the logarithm laws."),
    ("acopt:M.01", "Measurement", "Use the sine rule, cosine rule and area rule for non-right-angled triangles."),
    ("acopt:M.02", "Measurement", "Use the unit circle to define trigonometric ratios for angles beyond 90 degrees; recall exact values."),
    ("acopt:SP.01", "Space", "Prove and apply circle theorems."),
    ("acopt:ST.01", "Statistics", "Calculate and interpret standard deviation; use the line of best fit for prediction."),
]

QCAA_SOURCE = {
    "general": "QCAA General Mathematics 2025 v1.3 (Jan 2026)",
    "methods": "QCAA Mathematical Methods 2025 syllabus (official PDF; sub-topic summaries paraphrased)",
    "specialist": "QCAA Specialist Mathematics 2025 v1.4 (Mar 2026)",
}
# Methods sub-topics: (unit, topic) -> [(title, hours, paraphrase of subject matter)]
MM_SUB = {
    (1, 1): [("Surds", 4, "Surds as irrational roots; simplify, rationalise denominators, four operations."),
             ("Quadratic functions", 7, "Features and sketches of parabolas; solve by factorising, formula, completing the square, technology; discriminant; models.")],
    (1, 2): [("Binomial expansion", 3, "Combinations, Pascal's triangle and nCr; binomial theorem expansions."),
             ("Cubic functions", 9, "Degree and coefficients; expand from factors; cubic graph features and end behaviour; solve cubics; models.")],
    (1, 3): [("Introduction to functions and relations", 5, "Relations and functions, vertical line test, function notation, domain and range, piecewise functions."),
             ("Graphs of relations", 4, "Circles (centre, radius), parabolas and other relations; sketch and model."),
             ("Reciprocal functions", 2, "Hyperbolic graphs: intercepts, asymptotes, end behaviour; models.")],
    (1, 4): [("Circular measure and radian measure", 2, "Radians and degrees; arc length and sector area."),
             ("Introduction to trigonometric functions", 8, "Unit circle, periodicity, exact values, graphs and transformations of sin, cos, tan; solve equations incl. Pythagorean identity; models.")],
    (1, 5): [("Language of events and sets", 4, "Outcomes, sample spaces, events; complement, intersection, union, mutually exclusive; Venn diagrams."),
             ("Conditional probability and independence", 7, "Probability rules; conditional probability P(A|B); independence and the multiplication rule; relative frequencies; models.")],
    (2, 1): [("Indices and index laws", 4, "Negative and fractional indices, index laws, radicals and indices, scientific notation."),
             ("Introduction to exponential functions", 6, "Graphs of y = a^x and transformations; solve exponential equations; models.")],
    (2, 2): [("Logarithms and logarithmic laws", 5, "Logarithms as indices; logarithm laws; solve index equations with logarithms."),
             ("Logarithmic functions", 7, "Graphs and transformations of logarithmic functions; solve log equations; models such as decibels and the Richter scale.")],
    (2, 3): [("Rates of change and the concept of derivatives", 10, "Average and instantaneous rates of change; first principles; derivative as gradient of tangent; power rule; derivatives of polynomials.")],
    (2, 4): [("Graphical applications of derivatives", 12, "Tangents and normals; displacement and velocity; stationary points and their nature; sketch polynomials up to degree 4; local and global extrema.")],
    (2, 5): [("Differentiation rules", 11, "Chain, product and quotient rules for power and polynomial functions, in simplest factorised form.")],
    (3, 1): [("Calculus of exponential functions", 6, "The number e; derivative of e^x and related forms."),
             ("Calculus of logarithmic functions", 8, "ln as the inverse of e^x; solve base-e equations; derivative of ln x; models.")],
    (3, 2): [("Calculus of trigonometric functions", 5, "Derivatives of sin x, cos x and tan x; models."),
             ("Differentiation rules", 5, "Chain, product and quotient rules with exponential, logarithmic and trigonometric functions.")],
    (3, 3): [("The second derivative and applications of differentiation", 10, "Second derivative, acceleration, concavity and inflection points; second derivative test; sketching; optimisation.")],
    (3, 4): [("Anti-differentiation", 9, "Anti-derivatives and indefinite integrals of powers, e^x, 1/x, sin, cos and linear composites; initial conditions; displacement from velocity or acceleration.")],
    (3, 5): [("General discrete random variables", 5, "Discrete random variables and probability functions; mean, variance and standard deviation; models."),
             ("Bernoulli distributions", 2, "Bernoulli random variables; mean p and variance p(1 - p)."),
             ("Binomial distributions", 5, "Binomial probabilities, mean np and variance np(1 - p); at least / at most language; models.")],
    (4, 1): [("Fundamental theorem of calculus and definite integrals", 3, "Rectangle sums; definite integral as a limit of sums; fundamental theorem; area under a non-negative curve."),
             ("Applications of integration", 8, "Area between curve and axis and between curves; trapezoidal rule; total change; motion.")],
    (4, 2): [("Cosine and sine rules", 10, "Sine rule incl. ambiguous case, cosine rule, area formula; 2D and 3D problems with bearings, elevation and depression.")],
    (4, 3): [("General continuous random variables", 6, "Probability density and cumulative distribution functions; probabilities, mean and variance by integration; z-scores."),
             ("Normal distributions", 6, "Normal curve features, N(mu, sigma^2), standard normal; probabilities and quantiles with technology.")],
    (4, 4): [("Random sampling", 3, "Random samples, sources of bias, procedures that ensure randomness, simulated samples."),
             ("Sample proportions", 8, "The sample proportion as a random variable with mean p and sd sqrt(p(1 - p)/n); approximate normality for large n.")],
    (4, 5): [("Confidence intervals for proportions", 11, "Approximate confidence interval for p; margin of error; relation to confidence level and sample size; interpretation.")],
}

QCAA = {
    "general": ("GM", [
        ("Money, measurement, algebra and linear equations", ["Consumer arithmetic", "Shape and measurement", "Similarity and scale", "Algebra", "Linear equations and their graphs"]),
        ("Applications of linear equations and trigonometry, matrices and univariate data analysis", ["Applications of linear equations and their graphs", "Applications of trigonometry", "Matrices", "Univariate data analysis 1", "Univariate data analysis 2"]),
        ("Bivariate data and time series analysis, sequences and Earth geometry", ["Bivariate data analysis 1", "Bivariate data analysis 2", "Time series analysis", "Growth and decay in sequences", "Earth geometry and time zones"]),
        ("Investing and networking", ["Loans, investments and annuities 1", "Loans, investments and annuities 2", "Graphs and networks", "Networks and decision mathematics 1", "Networks and decision mathematics 2"]),
    ]),
    "methods": ("MM", [
        ("Surds, algebra, functions and probability", ["Surds and quadratic functions", "Binomial expansion and cubic functions", "Functions and relations", "Trigonometric functions", "Probability"]),
        ("Calculus and further functions", ["Exponential functions", "Logarithms and logarithmic functions", "Introduction to differential calculus", "Applications of differential calculus", "Further differentiation"]),
        ("Further calculus and introduction to statistics", ["Differentiation of exponential and logarithmic functions", "Differentiation of trigonometric functions and differentiation rules", "Further applications of differentiation", "Introduction to integration", "Discrete random variables"]),
        ("Further calculus, trigonometry and statistics", ["Further integration", "Trigonometry", "Continuous random variables and the normal distribution", "Sampling and proportions", "Interval estimates for proportions"]),
    ]),
    "specialist": ("SM", [
        ("Combinatorics, proof, vectors and matrices", ["Combinatorics", "Introduction to proof", "Vectors in the plane", "Algebra of vectors in two dimensions", "Matrices"]),
        ("Complex numbers, further proof, trigonometry, functions and transformations", ["Complex numbers", "Complex arithmetic and algebra", "Circle and geometric proofs", "Trigonometry and functions", "Matrices and transformations"]),
        ("Further complex numbers, proof, vectors and matrices", ["Further complex numbers", "Mathematical induction and trigonometric proofs", "Vectors in two and three dimensions", "Vector calculus", "Further matrices"]),
        ("Further calculus and statistical inference", ["Integration techniques", "Applications of integral calculus", "Rates of change and differential equations", "Modelling motion", "Statistical inference"]),
    ]),
}


def main():
    items = []
    for band, year, rows in (("y9", 9, Y9), ("y10", 10, Y10)):
        for code, strand, text in rows:
            items.append({"id": code, "framework": "ac9", "band": band, "year": year, "strand": strand,
                          "text": text, "verbatim": False, "source": AC_SOURCE})
    for code, strand, text in OPT:
        items.append({"id": code, "framework": "ac9-optional", "band": "y10opt", "year": 10, "strand": strand,
                      "text": text, "verbatim": False, "status": "inferred",
                      "source": "Inferred from ACARA 'Optional content for post-Year 10 Mathematics pathways' (to verify)"})
    for band, (code, units) in QCAA.items():
        for u, (utitle, topics) in enumerate(units, 1):
            items.append({"id": "qcaa25:%s.U%d" % (code, u), "framework": "qcaa2025", "band": band, "unit": u,
                          "kind": "unit", "text": "Unit %d: %s" % (u, utitle), "verbatim": True,
                          "title_status": "official",
                          "source": QCAA_SOURCE[band]})
            for t, title in enumerate(topics, 1):
                items.append({"id": "qcaa25:%s.U%d.T%d" % (code, u, t), "framework": "qcaa2025", "band": band,
                              "unit": u, "topic": t, "kind": "topic", "text": "Topic %d: %s" % (t, title),
                              "verbatim": True,
                              "title_status": "official",
                              "source": QCAA_SOURCE[band]})
                for k, (stitle, hours, para) in enumerate(MM_SUB.get((u, t), []) if band == "methods" else [], 1):
                    items.append({"id": "qcaa25:%s.U%d.T%d.S%d" % (code, u, t, k), "framework": "qcaa2025", "band": band,
                                  "unit": u, "topic": t, "subtopic": k, "kind": "subtopic", "hours": hours,
                                  "text": "%s: %s" % (stitle, para), "verbatim": False, "title_status": "official",
                                  "source": QCAA_SOURCE[band]})
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print("wrote %d standards items -> %s" % (len(items), os.path.relpath(OUT, ROOT)))


if __name__ == "__main__":
    main()
