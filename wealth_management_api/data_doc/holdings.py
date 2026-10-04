from typing import Any

# Within-fund weights are percentages of total NAV, including cash; each fund totals 100%.

HOLDINGS: list[dict[str, Any]] = [
    {'holding_id': 26, 'fund_id': 2, 'company_name': 'Everfield Renewables', 'sector': 'Utilities', 'weight': 30, 'esg_score': 92, 'as_of_date': '2026-09-30'},
    {'holding_id': 27, 'fund_id': 2, 'company_name': 'Greenhaven Water', 'sector': 'Utilities', 'weight': 15, 'esg_score': 90, 'as_of_date': '2026-09-30'},
    {'holding_id': 35, 'fund_id': 2, 'company_name': 'Fairhaven Finance', 'sector': 'Financials', 'weight': 27, 'esg_score': 84, 'as_of_date': '2026-09-30'},
    {'holding_id': 38, 'fund_id': 2, 'company_name': 'Alderwell Health', 'sector': 'Healthcare', 'weight': 25, 'esg_score': 89, 'as_of_date': '2026-09-30'},
    {'holding_id': 48, 'fund_id': 2, 'company_name': 'LumenArc Systems', 'sector': 'Technology', 'weight': 3, 'esg_score': 88, 'as_of_date': '2026-09-30'},
    {'holding_id': 51, 'fund_id': 3, 'company_name': 'LotusGate Internet', 'sector': 'Technology', 'weight': 25, 'esg_score': 64, 'as_of_date': '2026-09-30'},
    {'holding_id': 52, 'fund_id': 3, 'company_name': 'JadeRiver Commerce', 'sector': 'Consumer Discretionary', 'weight': 25, 'esg_score': 59, 'as_of_date': '2026-09-30'},
    {'holding_id': 53, 'fund_id': 3, 'company_name': 'Sundara Bank', 'sector': 'Financials', 'weight': 25, 'esg_score': 67, 'as_of_date': '2026-09-30'},
    {'holding_id': 54, 'fund_id': 3, 'company_name': 'Pacifica Chips', 'sector': 'Technology', 'weight': 20.5, 'esg_score': 72, 'as_of_date': '2026-09-30'},
    {'holding_id': 76, 'fund_id': 4, 'company_name': 'Northhaven Bank', 'sector': 'Financials', 'weight': 30, 'esg_score': 73, 'as_of_date': '2026-09-30'},
    {'holding_id': 80, 'fund_id': 4, 'company_name': 'Alderwell Health', 'sector': 'Healthcare', 'weight': 30, 'esg_score': 89, 'as_of_date': '2026-09-30'},
    {'holding_id': 81, 'fund_id': 4, 'company_name': 'Greenhaven Water', 'sector': 'Utilities', 'weight': 30, 'esg_score': 90, 'as_of_date': '2026-09-30'},
    {'holding_id': 94, 'fund_id': 4, 'company_name': 'Redleaf Tobacco', 'sector': 'Tobacco', 'weight': 6, 'esg_score': 22, 'as_of_date': '2026-09-30'},
    {'holding_id': 95, 'fund_id': 4, 'company_name': 'Ironvale Defence', 'sector': 'Weapons', 'weight': 4, 'esg_score': 35, 'as_of_date': '2026-09-30'},
    {'holding_id': 101, 'fund_id': 5, 'company_name': 'LumenArc Systems', 'sector': 'Technology', 'weight': 30, 'esg_score': 88, 'as_of_date': '2026-09-30'},
    {'holding_id': 104, 'fund_id': 5, 'company_name': 'Meridian Cloudworks', 'sector': 'Technology', 'weight': 25, 'esg_score': 84, 'as_of_date': '2026-09-30'},
    {'holding_id': 105, 'fund_id': 5, 'company_name': 'Deepwell Analytics', 'sector': 'Technology', 'weight': 20, 'esg_score': 80, 'as_of_date': '2026-09-30'},
    {'holding_id': 121, 'fund_id': 5, 'company_name': 'Clearstream Payments', 'sector': 'Financials', 'weight': 10, 'esg_score': 82, 'as_of_date': '2026-09-30'},
    {'holding_id': 124, 'fund_id': 5, 'company_name': 'Pacifica Chips', 'sector': 'Technology', 'weight': 15, 'esg_score': 72, 'as_of_date': '2026-09-30'},
    {'holding_id': 126, 'fund_id': 6, 'company_name': 'Northhaven Bank', 'sector': 'Financials', 'weight': 30, 'esg_score': 73, 'as_of_date': '2026-09-30'},
    {'holding_id': 130, 'fund_id': 6, 'company_name': 'Greenhaven Water', 'sector': 'Utilities', 'weight': 25, 'esg_score': 90, 'as_of_date': '2026-09-30'},
    {'holding_id': 131, 'fund_id': 6, 'company_name': 'Alderwell Health', 'sector': 'Healthcare', 'weight': 22, 'esg_score': 89, 'as_of_date': '2026-09-30'},
    {'holding_id': 140, 'fund_id': 6, 'company_name': 'Everfield Renewables', 'sector': 'Utilities', 'weight': 20, 'esg_score': 92, 'as_of_date': '2026-09-30'},
    {'holding_id': 141, 'fund_id': 6, 'company_name': 'LumenArc Systems', 'sector': 'Technology', 'weight': 3, 'esg_score': 88, 'as_of_date': '2026-09-30'},
    {'holding_id': 151, 'fund_id': 3, 'company_name': 'GBP Cash Reserve', 'sector': 'Cash', 'weight': 4.5, 'esg_score': None, 'as_of_date': '2026-09-30'},
]