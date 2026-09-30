# Personal Project Breakdown

## Domain Choice:
### E. Asset and Wealth Management: fund research and mandate compliance

**The problem.** A portfolio manager must decide whether a holding fits a client mandate, and an
adviser must explain fund performance and risk in plain language.

- **Records:** funds (strategy, fees, risk rating), portfolios, client mandates with restrictions.
- **Documents:** fund factsheets, manager commentary, investment mandates, ESG policies,
  regulatory suitability rules.
- **Questions:** "Does this fund breach the client's no tobacco restriction?",
  "Explain why the emerging market fund underperformed last quarter."
- **Differ it:** add a tool that screens a portfolio against mandate restrictions. Provide a
  fund comparison view in the UI. Streaming summary is a client-friendly fund update, so tone
  and plain language become part of your prompt design.

------------------------------------------------------
### Problem:
- Portfolio manager needs to check wehether investments follow a client's mandate and investement restrictions.

- Client advisor also needs to explain fund performance, fees and risks to clients in simple language.

- The system that will be built needs to help both tasks by combining structured fund data, mandate rules, documents, compliance screening and LLM generated explanations.

### Key concepts to understand:
- Fund - pools money from mutiple investors and invests it across assets such as shares, bonds or other securities.

### Users:
- Portfolio manager = works for an asset management firm and makes investment decisions for client portfolios. Also, needs to know whether investments in a portfolio follow the client's rules and restrictions.

- Client Advisor: communicates with clients and explains information about their investments. They need clear explanations of fund performance, risk, fees and other important information without too much financial jargon.

### Entities:
- Funds contain information such as:
    - fund name
    - investment strategy
    - fees
    - risk rating
    - esg score
    - holdings (holding = a company or investment owned by the fund. So if a fund has 60 different investments/positions across companies then that means that fund has 60 holdings. Each holding has a weight showing what % of the fund = invested in that company.)
        e.g., A fund with 60 holdings might own Microsoft, Apple, Nvidia, HSBC, Shell, etc., making 60 separate investment positions. BUT the fund may actually own millions of individual Microsoft shares.

- Portfolios:
    Portfolio contains funds owned by a client and how much of the portfolio = invested in each fund.
    E.g.,
    - 50% in Fund A
    - 30% in Fund B
    - 20% in Fund C

    Portfolio can then be checked against the client's mandate. A portfolio's % always = 100%.

    - One main reason portfolios contain many investments = diversification.
    - Portfolio examines how combining different investments can provide better risk/reward relationship than concentrating everything in one security.

- Issuers and Securities
    - Issuer = company that issues shares or bonds. The record will store company details - e.g., name, sector, esg score, etc.
        - Helps calculate total exposure to same company across funds and check mandate restrictions.
    E.g., Issuer = LumenArc Systems, purpose = stores the company’s identity, sector, ESG score and activity tags

        [
        {
            "issuer_id": 1,
            "name": "LumenArc Systems",
            "sector": "Technology",
            "country": "United States",
            "esg_score": 88,
            "activity_tags": [],
            "classification_as_of": "2026-09-30",
            "classification_status": "verified"
        },
        {
            "issuer_id": 12,
            "name": "Redleaf Tobacco",
            "sector": "Tobacco",
            "country": "United Kingdom",
            "esg_score": 22,
            "activity_tags": ["tobacco"],
            "classification_as_of": "2026-09-30",
            "classification_status": "verified"
        }
        ]

    - Securities = specific investment issued by the issuer company, such as its shares or a specific bond.
    - The record will store the investment type and for bonds, the interest rate and repayment date
        Security = LumenArc shares or its 2034 corporate bond, purpose = describes the instrument, including bond coupon and maturity

        [
        {
            "security_id": 1,
            "issuer_id": 1,
            "name": "LumenArc Systems Ordinary Shares",
            "instrument_type": "equity",
            "currency": "USD",
            "maturity_date": null,
            "coupon_pct": null,
            "credit_rating": null
        },
        {
            "security_id": 100,
            "issuer_id": 1,
            "name": "LumenArc Systems 4.25% 2034",
            "instrument_type": "corporate_bond",
            "currency": "GBP",
            "maturity_date": "2034-06-30",
            "coupon_pct": 4.25,
            "credit_rating": "A-"
        }
        ]

    - Holding
        Fund 1 invests 8% in LumenArc shares
        purpose = records the fund’s position and weight

- Mandates = client's investment rules and restrictions (what's allowed and what's not, and limits on how their funds can be invested and allocated).

Mandate compliance must often be assessed across whole portfolio, not simply one investment at a time.

    E.g.,
    - No tobacco investments for a cancer charity
    - No weapons companies
    - Max exposure to xy company
    - Esg requirements
    - Restrictions on xy sector

### Documents:
- Fund factsheets
- Fund manager commentary
- Client mandates
- ESG policy
- Sustainability policy
- Fee methodology
- Compliance breach procedure
- Regulatory suitability guidance

Docs will be stored in Chroma using Voyage embeddings so that users can search them and ask grounded questions.

#### Doc may look like:

Two main docs: Funds, Holdings, Portfolio, Portfolio_fund, Mandate, Madate_rule

Fund:

- fund_id
- name
- strategy
- management_fee
- risk_rating
- esg_score
- benchmark
- management_style

{
  "fund_id": 1,
  "name": "Global Equity Fund",
  "strategy": "Global large-cap equities",
  "management_fee": 0.75,
  "risk_rating": 5,
  "esg_score": 78,
  "benchmark": "Global Equity Index",
  "management_style": "active"
}

    Funds has to many relationship with Holdings:

    This branching into HOLDINGS for that fund:
    - holding_id
    - fund_id
    - company_name
    - sector
    - weight
    - esg_score

     E.g.,Microsoft           8%
        Apple                 6%
        Shell                 3%
        Other companies      83%

    [
    {
        "holding_id": 1,
        "fund_id": 1,
        "company_name": "Microsoft",
        "sector": "Technology",
        "weight": 8.0
    },
    {
        "holding_id": 2,
        "fund_id": 1,
        "company_name": "Apple",
        "sector": "Technology",
        "weight": 6.0
    },
    {
        "holding_id": 3,
        "fund_id": 1,
        "company_name": "Shell",
        "sector": "Energy",
        "weight": 3.0
    }
    ]

Portfolio:
- portfolio_id
- name
- client_name

{
  "portfolio_id": 1,
  "name": "Charity Growth Portfolio",
  "client_name": "Example Charity"
}

    Portfolio has one to many relationship with Portfolio funds

    Portfolio fund
    - portfolio_fund_id
    - portfolio_id
    - fund_id
    - weight

    [
    {
        "portfolio_id": 1,
        "fund_id": 1,
        "weight": 50.0
    },
    {
        "portfolio_id": 1,
        "fund_id": 2,
        "weight": 50.0
    }
    ]

Mandate:
- mandate_id
- name
- client_name

{
  "mandate_id": 1,
  "name": "Charity Responsible Investment Mandate",
  "client_name": "Example Charity"
}

    Mandate will have one to many relationship with Mandate rules

    Mandate Rules
    - rule_id
    - mandate_id       ← links to Mandate
    - rule_type
    - target
    - operator
    - limit

    [
    {
        "rule_type": "company_exposure",
        "target": "Microsoft",
        "operator": "<=",
        "limit": 5.0
    },
    {
        "rule_type": "sector_exclusion",
        "target": "Tobacco",
        "operator": "=",
        "limit": 0.0
    },
    {
        "rule_type": "sector_exposure",
        "target": "Technology",
        "operator": "<=",
        "limit": 25.0
    }
    ]

Mandate rules could just look like this: 
"rule_type "         "target"     "operator"  "limit"
company_exposure     Microsoft    <=          5
sector_exposure      Technology   <=          25
sector_exclusion     Tobacco      =           0
minimum_esg_score    FUND         >=          70

### Mandate screening tool:
Agent will have a tool that it can use to check a portfolio against a client's mandate.

E.g.,
` screen_portfolio_against_mandate(portfolio_id, mandate_id)`

The tool should be able to loosely do these - can add or take away during project:
- Look at the funds in the portfolio
- Look at the holdings inside these funds
- Calculate client's overall exposure to companies and sectors
- Compare above exposures with client's mandate rules
- Flag any breaches or issues that need reviewing.

The calculations will set in python than letting LLM decide.

### Extra tool:
- something to look through the funds to see how many holdings they have and then flag the rule breaches of the potential investments for them.

    So the system will calculate client's real exposure to companies through the funds they own.

    E.g.,
    Client portfolio has: 50% in fund A, 50% in fund B

    Fund A has 8% invested in Microsoft and Fund B has 6% inbvested in Microsoft.

    Therefore, the client's total Microsoft exposure = (50% * 8%) + (50% * 6%) = 7%

    7% can then be compared with client's mandate.

During compliance calculation the model will look through Portfolio --> Portfolio Fund --> Fund --> Holdings where it will calculate exposures --> Manate Rule --> Output: Pass/breach/review with references of why from which doc.

### Fuzzy matching
- Name searching: 
    Users and the agent will be able to find funds and mandates even if the name is slightly misspelled.
- Company searching: 
    Different versions of the same company name will be grouped together - recognised as the same company.
        - important when calculating exposure
        - if not system could incorrectly treat them as different companies and miss a mandate breach --> not good
- Min score threshold will be used 
    - if match score is too low then the system will not match the names --> not the same company
    - if more than one company looks like they're a possible match, then the system will return the possible matches for review instad of guessing if they're a match or not.

### LLM features to include:
Model used - Claude because anthropic api key

- Client firnedly fund summary
    - Claude will generate simple explanation of fund
    - summary for the fund could include:
        - investment strategy
        - performance
        - risks
        - fees
        - important changes made
    - may include normal summary endpoints and also a streaming version, where streaming version will allow user to see response appear as it's generated.

- Structured fund assessment
    - Claude will return structured assessment validated using Pydantic.
    - Potential fields in return:
        - strengths
        - risks
        - fee observations
            - what system notices about fund's fees, e.g., fund x has higher fees than fun y or management fee = 1.2%
        - ESG observations
            - what system notices about fund's environmental, social, and governance characteristics. E.g., fund A has low ESG score or Fund A has exposure to companies restricted by client's ESG policy.
        - mandate issues

Structures texts helps user read better than free text. 

- Grounded Q&A with citations
    - Users will be able to ask questions about the documents --> indexed.
    - System will be able to:
        - search Chromadb
        - find most relevant documents
        - check whether results = above relevance threshold
        - send relevant information to claude
        - return an answer with document citations for reference

If not document = relevant enough then the system will refuse to answer and wnt call Claude.

- Agent using search and screening
    - Agent will have at least 2 tools to use:
        1. Knowledge search
        2. Portfolio mandate screening

    Agent will then be able to decide which tools it needs depending on the user's query.

### Validations:
- No answer below the relevance floor --> no LLM call in that case
    - if not result = above set relevance threshold, then the system will not call LLM. Instead will explain that there's not enough relevant info to answer query without guessing.

- Never give suitability advice
    - system will not make final investment suitability decisions for a client.
    - systenm can explain information and identify possible issues, but important decisions will remain with the portfolio manager, client advisor, etc. 

- Breached = always flagged to compliance
    - if deterministic screening tool finds a mandate rule = breached, then the breach will ALWAYS be flagged up
    - system will not allow LLM to override calculated risk

- Out-of-date factsheets = flagged
    - fund factsheets will contain dates
    - if factsheet = older than allowed age then system will mark it as old/out of date
    - this method will stop users from relying on old information without realising

### UI:
- Ask, search only, streaming summary --> diff pages? maybes
- Fund comparisons??
    - users may be able to select two or more funds to compare information. E.g., stretgy, fees, risk rating, etc.
- Mandate compliance screen??
    - users can choose a portfolio and a client mandate then the system can screen the portfolio of those id's and show:
        - passed rules
        - breached rules
        - exposure calculations
        - items requiring human review

### Tests to see if it's working overall:
- LLM Summary
    - check that summary endpoint works while mocking claude call
- Refusal
    - check that agent uses the tools correctly and handles tool errors
- Iteration limits
    - check agent stops when it reaches max number of tool-use iterations and doesn't keep looping through
- Screening Maths
    - check that portfolio exposures and mandate limits = calculated correctly
- Fuzzy Matching
    - exact company names
    - slightly diff company names
    - misspelled names
    - matches below threshold
    - ambiguous matching - e.g., more than one pair match --> should allow users to decide instead of guessing if same.