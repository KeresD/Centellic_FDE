"The synthetic document corpus for the vector store."

from typing import Any

DOCUMENTS: list[dict[str, Any]] = [
    # ---------- Fund factsheets ----------
    {
        "id": "doc-001",
        "title": "Wrenford Sustainable Leaders Fund - Factsheet, September 2026",
        "type": "fund_factsheet",
        "date": "2026-09-30",
        "fund_id": 2,
        "body": (
            "Wrenford Sustainable Leaders Fund (fund ID 2). Factsheet as at 30 September 2026. "
            "Strategy: global sustainable equities. Asset class: equity. Reporting currency "
            "GBP, unhedged. "
            "Q3 2026 total return 4.6% net of fund costs, against 4.1% for the Wrenford "
            "Synthetic Sustainable Equity Index. Trailing 12 months: 11.2%. Adviser and "
            "platform fees are excluded and deducted once, at client level. "
            "Ongoing charges 1.0% a year; estimated transaction costs 0.08% a year. "
            "Risk rating 4 on the Wrenford 1 to 7 scale. The rating is an ordinal category, "
            "not a probability of loss. ESG score 86 out of 100, approved. "
            "Holdings disclosed to 100% of NAV at 30 September 2026. No holding carries a "
            "tobacco or weapons activity tag. "
            "Capital is at risk and past performance is not a reliable indicator of future "
            "results. This factsheet does not explain the causes of the return."
        ),
    },
    {
        "id": "doc-002",
        "title": "Wrenford Emerging Markets Opportunities Fund - Factsheet, September 2026",
        "type": "fund_factsheet",
        "date": "2026-09-30",
        "fund_id": 3,
        "body": (
            "Wrenford Emerging Markets Opportunities Fund (fund ID 3). Factsheet as at "
            "30 September 2026. Strategy: emerging-market equities. Asset class: equity. "
            "Reporting currency GBP, unhedged. "
            "Q3 2026 total return -2.4% net of fund costs, against 1.1% for the Wrenford "
            "Synthetic Emerging Markets Index. Trailing 12 months: 3.7%. Adviser and platform "
            "fees are excluded and deducted once, at client level. "
            "Ongoing charges 1.3% a year; estimated transaction costs 0.08% a year. "
            "Risk rating 6 on the Wrenford 1 to 7 scale. The rating is an ordinal category, "
            "not a probability of loss. ESG score pending review; there is no approved score. "
            "Holdings disclosed to 100% of NAV at 30 September 2026, including a 4.5% cash "
            "position. No holding carries a tobacco or weapons activity tag. "
            "Capital is at risk and past performance is not a reliable indicator of future "
            "results. This factsheet does not explain the causes of the return; see the Q3 "
            "manager commentary."
        ),
    },
    {
        "id": "doc-003",
        "title": "Wrenford UK Equity Income Fund - Factsheet, September 2026",
        "type": "fund_factsheet",
        "date": "2026-09-30",
        "fund_id": 4,
        "body": (
            "Wrenford UK Equity Income Fund (fund ID 4). Factsheet as at 30 September 2026. "
            "Strategy: UK dividend-paying equities. Asset class: equity. Reporting currency "
            "GBP, unhedged. "
            "Q3 2026 total return 2.1% net of fund costs, against 2.8% for the Wrenford "
            "Synthetic UK Dividend Index. Trailing 12 months: 6.8%. Adviser and platform fees "
            "are excluded and deducted once, at client level. "
            "Ongoing charges 0.75% a year; estimated transaction costs 0.08% a year. "
            "Risk rating 4 on the Wrenford 1 to 7 scale. The rating is an ordinal category, "
            "not a probability of loss. ESG score 67 out of 100, approved. "
            "Holdings disclosed to 100% of NAV at 30 September 2026. Redleaf Tobacco (6% of NAV) "
            "carries the tobacco activity tag and Ironvale Defence (4%) carries the weapons "
            "activity tag. "
            "Capital is at risk and past performance is not a reliable indicator of future "
            "results. This factsheet does not explain the causes of the return."
        ),
    },
    {
        "id": "doc-004",
        "title": "Wrenford Technology Innovation Fund - Factsheet, September 2026",
        "type": "fund_factsheet",
        "date": "2026-09-30",
        "fund_id": 5,
        "body": (
            "Wrenford Technology Innovation Fund (fund ID 5). Factsheet as at 30 September 2026. "
            "Strategy: global technology and digital infrastructure equities. Asset class: "
            "equity. Reporting currency GBP, unhedged. "
            "Q3 2026 total return 7.8% net of fund costs, against 8.6% for the Wrenford "
            "Synthetic Digital Innovation Index. Trailing 12 months: 18.3%. Adviser and "
            "platform fees are excluded and deducted once, at client level. "
            "Ongoing charges 1.35% a year; estimated transaction costs 0.08% a year. "
            "Risk rating 6 on the Wrenford 1 to 7 scale. The rating is an ordinal category, "
            "not a probability of loss. ESG score 66 out of 100, approved. "
            "Holdings disclosed to 100% of NAV at 30 September 2026. No holding carries a "
            "tobacco or weapons activity tag. "
            "Capital is at risk and past performance is not a reliable indicator of future "
            "results. This factsheet does not explain the causes of the return."
        ),
    },
    {
        "id": "doc-005",
        "title": "Wrenford Global Corporate Bond Fund - Factsheet, September 2026",
        "type": "fund_factsheet",
        "date": "2026-09-30",
        "fund_id": 6,
        "body": (
            "Wrenford Global Corporate Bond Fund (fund ID 6). Factsheet as at 30 September 2026. "
            "Strategy: developed-market investment-grade corporate bonds. Asset class: fixed "
            "income. Reporting currency GBP, GBP hedged. "
            "Q3 2026 total return 1.5% net of fund costs, against 1.2% for the Wrenford "
            "Synthetic Corporate Bond Index GBP Hedged. Trailing 12 months: 4.9%. Adviser and "
            "platform fees are excluded and deducted once, at client level. "
            "Ongoing charges 0.55% a year; estimated transaction costs 0.04% a year. "
            "Risk rating 3 on the Wrenford 1 to 7 scale. The rating is an ordinal category, "
            "not a probability of loss. ESG score 74 out of 100, approved. "
            "Holdings disclosed to 100% of NAV at 30 September 2026. No holding carries a "
            "tobacco or weapons activity tag. "
            "Capital is at risk and past performance is not a reliable indicator of future "
            "results. This factsheet does not explain the causes of the return."
        ),
    },
    # ---------- Manager commentary ----------
    {
        "id": "doc-006",
        "title": "Wrenford Emerging Markets Opportunities Fund - Q3 2026 manager commentary",
        "type": "manager_commentary",
        "date": "2026-09-30",
        "fund_id": 3,
        "body": (
            "Wrenford Asset Management investment review, Q3 2026. Emerging Markets "
            "Opportunities Fund (fund ID 3). "
            "Performance: the fund returned -2.4% net of fund costs against +1.1% for its "
            "benchmark, a relative shortfall of 3.5 percentage points. "
            "Holding contributions, given as quarter-start fund weight, quarter-start benchmark "
            "weight, holding return in GBP and gross contribution: "
            "Sundara Bank 26.7%, 5.9%, -8.19%, -2.185 pp. "
            "LotusGate Internet 25.3%, 14.6%, -3.19%, -0.807 pp. "
            "Pacifica Chips 20.1%, 21.5%, 0.00%, 0.000 pp. "
            "GBP Cash Reserve 4.4%, 5.6%, +0.90%, +0.039 pp. "
            "JadeRiver Commerce 23.6%, 52.5%, +3.81%, +0.898 pp. "
            "Gross contributions total -2.055 pp. Modelled fund-cost drag of 0.345 pp reconciles "
            "this to the -2.4% net return. The 4.5% closing cash position is disclosed. "
            "Against the benchmark, the fund started the quarter overweight Sundara Bank and "
            "LotusGate Internet, both of which fell, and underweight JadeRiver Commerce, which "
            "rose. "
            "Evidence policy: absolute holding contributions must not be described as relative "
            "attribution. Quarterly history supports calendar-year returns, quarterly volatility "
            "and quarter-end drawdown, but does not show intraquarter losses. The fund ESG score "
            "is pending review, so an ESG minimum cannot be confirmed. Do not infer exposure from "
            "issuer names, replace missing scores with zero, assert economic or currency causes "
            "without supporting evidence, or treat mandate compliance as suitability approval."
        ),
    },
    # ---------- Client mandates ----------
    {
        "id": "doc-007",
        "title": "Haven Cancer Support Responsible Growth Mandate",
        "type": "investment_mandate",
        "date": "2026-07-01",
        "mandate_id": 1,
        "body": (
            "Wrenford Asset Management. Haven Cancer Support Responsible Growth Mandate "
            "(mandate ID 1). Effective 1 July 2026, version 1.0, review date 1 July 2027. "
            "1. Client and objective. Haven Cancer Support Trust is a charity funding cancer "
            "care and patient support. The trustees exclude tobacco because it conflicts "
            "directly with the charity's purpose, and exclude weapons under their responsible "
            "investment statement. Portfolio: Haven Cancer Support Growth Portfolio. Objective: "
            "capital growth to fund the charity's mission over a 10-year horizon, with planned "
            "withdrawals of £100,000 a year. "
            "2. Applicable policies. Restrictions are measured under the Wrenford Responsible "
            "Investment and Exclusions Policy. Breaches, missing evidence and suitability are "
            "handled under the Wrenford Suitability and Mandate Oversight Rules. "
            "3. Restrictions. "
            "3.1 The portfolio shall have zero exposure to issuers classified as involved in "
            "tobacco. Any positive exposure breaches this restriction. "
            "3.2 The portfolio shall have zero exposure to issuers classified as involved in "
            "weapons. Any positive exposure breaches this restriction. "
            "3.3 Aggregate portfolio exposure to LumenArc Systems (issuer ID 1), across all "
            "securities issued by that company and all held funds, shall not exceed 5% of "
            "portfolio NAV. "
            "3.4 Aggregate portfolio exposure to the Technology sector shall not exceed 25% of "
            "portfolio NAV. Equity and bond positions both count toward issuer-sector exposure. "
            "3.5 Each held fund shall have an approved ESG score of at least 70 on the 0–100 "
            "scale. A missing score or a score pending review is insufficient evidence to "
            "determine compliance. Fund scores are assessed individually and shall not be "
            "replaced by a portfolio average. "
            "3.6 Each held fund shall have a risk rating no greater than 5 on the 1–7 scale. "
            "Fund risk ratings shall not be averaged for this rule."
        ),
    },
    {
        "id": "doc-008",
        "title": "Willow Community Responsible Investment Mandate",
        "type": "investment_mandate",
        "date": "2026-07-01",
        "mandate_id": 2,
        "body": (
            "Wrenford Asset Management. Willow Community Responsible Investment Mandate "
            "(mandate ID 2). Effective 1 July 2026, version 1.0, review date 1 July 2027. "
            "1. Client and objective. Willow Community Foundation is a charity making grants to "
            "local community groups. The trustees' responsible investment statement excludes "
            "tobacco and weapons and limits concentration in the Technology sector and in any "
            "single company. Portfolio: Willow Community Responsible Portfolio. Objective: "
            "responsible growth to fund community grants over a 10-year horizon, with planned "
            "withdrawals of £50,000 a year. "
            "2. Applicable policies. Restrictions are measured under the Wrenford Responsible "
            "Investment and Exclusions Policy. Breaches, missing evidence and suitability are "
            "handled under the Wrenford Suitability and Mandate Oversight Rules. "
            "3. Restrictions. "
            "3.1 The portfolio shall have zero exposure to issuers classified as involved in "
            "tobacco. Any positive exposure breaches this restriction. "
            "3.2 The portfolio shall have zero exposure to issuers classified as involved in "
            "weapons. Any positive exposure breaches this restriction. "
            "3.3 Aggregate portfolio exposure to LumenArc Systems (issuer ID 1), across all "
            "securities issued by that company and all held funds, shall not exceed 5% of "
            "portfolio NAV. "
            "3.4 Aggregate portfolio exposure to the Technology sector shall not exceed 25% of "
            "portfolio NAV. Equity and bond positions both count toward issuer-sector exposure. "
            "3.5 Each held fund shall have an approved ESG score of at least 70 on the 0–100 "
            "scale. A missing score or a score pending review is insufficient evidence to "
            "determine compliance. Fund scores are assessed individually and shall not be "
            "replaced by a portfolio average. "
            "3.6 Each held fund shall have a risk rating no greater than 5 on the 1–7 scale. "
            "Fund risk ratings shall not be averaged for this rule."
        ),
    },
    {
        "id": "doc-009",
        "title": "Hartwell Growth and Concentration Mandate",
        "type": "investment_mandate",
        "date": "2026-07-01",
        "mandate_id": 3,
        "body": (
            "Wrenford Asset Management. Hartwell Growth and Concentration Mandate (mandate ID 3). "
            "Effective 1 July 2026, version 1.0, review date 1 July 2027. "
            "1. Client and objective. Sofia Hartwell is a private client seeking long-term "
            "growth. She accepts concentration in growth sectors within the limits below. No "
            "activity exclusions apply. Portfolio: Hartwell Long-Term Growth Portfolio. "
            "Objective: long-term capital growth over a 15-year horizon, with no planned "
            "withdrawals. "
            "2. Applicable policies. Restrictions are measured under the Wrenford Responsible "
            "Investment and Exclusions Policy. Breaches, missing evidence and suitability are "
            "handled under the Wrenford Suitability and Mandate Oversight Rules. "
            "3. Restrictions. "
            "3.1 Aggregate portfolio exposure to LumenArc Systems (issuer ID 1), across all "
            "securities issued by that company and all held funds, shall not exceed 6% of "
            "portfolio NAV. "
            "3.2 Aggregate portfolio exposure to the Technology sector shall not exceed 40% of "
            "portfolio NAV. Equity and bond positions both count toward issuer-sector exposure. "
            "3.3 Each held fund shall have a risk rating no greater than 6 on the 1–7 scale. "
            "Fund risk ratings shall not be averaged for this rule. "
            "3.4 No individual fund shall account for more than 65% of total portfolio NAV."
        ),
    },
    {
        "id": "doc-010",
        "title": "Marlow Retirement Allocation Mandate",
        "type": "investment_mandate",
        "date": "2026-07-01",
        "mandate_id": 4,
        "body": (
            "Wrenford Asset Management. Marlow Retirement Allocation Mandate (mandate ID 4). "
            "Effective 1 July 2026, version 1.0, review date 1 July 2027. "
            "1. Client and objective. Evan Marlow is a private client drawing an income in "
            "retirement. Tolerance limits rather than full exclusions apply to tobacco and "
            "weapons. The fixed income minimum supports income and capital stability. "
            "Portfolio: Marlow Retirement Income Portfolio. Objective: retirement income and "
            "capital preservation over an 8-year horizon, with planned withdrawals of £24,000 "
            "a year. "
            "2. Applicable policies. Restrictions are measured under the Wrenford Responsible "
            "Investment and Exclusions Policy. Breaches, missing evidence and suitability are "
            "handled under the Wrenford Suitability and Mandate Oversight Rules. "
            "3. Restrictions. "
            "3.1 Aggregate portfolio exposure to issuers classified as involved in tobacco shall "
            "not exceed 2% of portfolio NAV. "
            "3.2 Aggregate portfolio exposure to issuers classified as involved in weapons shall "
            "not exceed 2% of portfolio NAV. "
            "3.3 Aggregate portfolio exposure to the Technology sector shall not exceed 20% of "
            "portfolio NAV. Equity and bond positions both count toward issuer-sector exposure. "
            "3.4 Each held fund shall have an approved ESG score of at least 60 on the 0–100 "
            "scale. A missing score or a score pending review is insufficient evidence to "
            "determine compliance. Fund scores are assessed individually and shall not be "
            "replaced by a portfolio average. "
            "3.5 Each held fund shall have a risk rating no greater than 4 on the 1–7 scale. "
            "Fund risk ratings shall not be averaged for this rule. "
            "3.6 At least 50% of total portfolio NAV shall be invested in the fixed_income asset "
            "class, measured by underlying security types; cash does not count as fixed income."
        ),
    },
    {
        "id": "doc-011",
        "title": "Ashcombe Research and Evidence Mandate",
        "type": "investment_mandate",
        "date": "2026-07-01",
        "mandate_id": 5,
        "body": (
            "Wrenford Asset Management. Ashcombe Research and Evidence Mandate (mandate ID 5). "
            "Effective 1 July 2026, version 1.0, review date 1 July 2027. "
            "1. Client and objective. Ashcombe Research Endowment funds scientific research in "
            "perpetuity. Restrictions focus on approved ESG evidence, fund risk and "
            "concentration. Portfolio: Ashcombe Research Allocation Portfolio. Objective: "
            "long-term funding of research grants over a 20-year horizon, with planned "
            "withdrawals of £90,000 a year. "
            "2. Applicable policies. Restrictions are measured under the Wrenford Responsible "
            "Investment and Exclusions Policy. Breaches, missing evidence and suitability are "
            "handled under the Wrenford Suitability and Mandate Oversight Rules. "
            "3. Restrictions. "
            "3.1 Each held fund shall have an approved ESG score of at least 65 on the 0–100 "
            "scale. A missing score or a score pending review is insufficient evidence to "
            "determine compliance. Fund scores are assessed individually and shall not be "
            "replaced by a portfolio average. "
            "3.2 Each held fund shall have a risk rating no greater than 6 on the 1–7 scale. "
            "Fund risk ratings shall not be averaged for this rule. "
            "3.3 No individual fund shall account for more than 50% of total portfolio NAV. "
            "3.4 Aggregate portfolio exposure to LumenArc Systems (issuer ID 1), across all "
            "securities issued by that company and all held funds, shall not exceed 5% of "
            "portfolio NAV."
        ),
    },
    # ---------- House policies ----------
    {
        "id": "doc-012",
        "title": "Wrenford Responsible Investment and Exclusions Policy",
        "type": "esg_policy",
        "date": "2026-07-01",
        "body": (
            "Wrenford Asset Management. Responsible Investment and Exclusions Policy. Effective "
            "1 July 2026, version 2.0, owner: Investment Risk. "
            "1. Purpose. This policy sets how client mandate restrictions on activities, "
            "sectors, companies, ESG scores and asset classes are measured across Wrenford "
            "funds and client portfolios. "
            "2. Activity classification. 2.1 Issuers are classified by activity tag. The tag "
            "tobacco covers manufacture of tobacco products. The tag weapons covers manufacture "
            "of weapons and weapon systems. 2.2 Tags are assigned at issuer level and apply to "
            "every security of that issuer, equity and bond. 2.3 Exposure is not inferred from "
            "issuer names or sector labels. Only recorded tags count. "
            "3. Measurement. 3.1 Percentage restrictions use total portfolio NAV, including "
            "cash. 3.2 Indirect exposure equals portfolio fund weight multiplied by fund "
            "holding weight, divided by 100. 3.3 Company exposure is aggregated by issuer ID "
            "across all equity and bond securities and all held funds. Variants of an issuer's "
            "name resolve to the same issuer ID. 3.4 Activity restrictions count the full "
            "market value of a tagged issuer's securities. 3.5 Cash has no company, sector or "
            "activity exposure and does not count as fixed income. 3.6 Inclusive limits permit "
            "values exactly equal to the threshold. "
            "4. ESG scores. 4.1 Fund ESG scores run from 0 to 100 and are approved by the "
            "Responsible Investment Committee before use. 4.2 A score pending review, or no "
            "score, is insufficient evidence. It must not be replaced by zero, an estimate or a "
            "portfolio average. 4.3 ESG scores do not apply to cash. "
            "5. Missing evidence. Missing classifications, weights or approved scores are "
            "recorded as insufficient evidence and referred to the portfolio manager. A rule "
            "with insufficient evidence is neither a pass nor a breach."
        ),
    },
    {
        "id": "doc-013",
        "title": "Wrenford Suitability and Mandate Oversight Rules",
        "type": "suitability_rules",
        "date": "2026-07-01",
        "body": (
            "Wrenford Asset Management. Suitability and Mandate Oversight Rules. Effective "
            "1 July 2026, version 1.3, owner: Compliance. "
            "1. Scope. These rules apply to advisers and portfolio managers reviewing client "
            "portfolios and fund holdings. "
            "2. Mandate checks. 2.1 Record the calculation, source section and result for each "
            "mandate rule. 2.2 Refer breaches and insufficient evidence to the portfolio "
            "manager. 2.3 Fund ESG scores and risk ratings are assessed fund by fund. A breach "
            "is not cured by averaging across the portfolio. "
            "3. Suitability. 3.1 Mandate compliance alone does not establish suitability. "
            "3.2 An adviser must separately review the client's investment objective, attitude "
            "to risk, capacity for loss, investment horizon, planned withdrawals, liquid assets "
            "outside the portfolio, and investment knowledge and experience. 3.3 A client "
            "assessment recorded as requiring adviser review is not approved until an adviser "
            "signs it off. "
            "4. Performance and fees. 4.1 Fund returns are reported net of fund costs. Adviser "
            "and platform fees are deducted once, after fund returns. 4.2 Explanations of "
            "performance must rest on holding contributions or manager commentary. Economic or "
            "currency causes are not asserted without supporting evidence. 4.3 Client "
            "communications state that past performance is not a reliable indicator of future "
            "results. "
            "5. Personal recommendations. Only an authorised adviser may make a personal "
            "recommendation. Research tools and automated screening produce information for "
            "adviser review, not advice to clients."
        ),
    },
]