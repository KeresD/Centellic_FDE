from typing import Any

# Use activity_tags for tobacco/weapons tests. Cash ESG is not applicable; unused reference issuers are omitted.

ISSUERS: list[dict[str, Any]] = [
    {'issuer_id': 1, 'name': 'LumenArc Systems', 'sector': 'Technology', 'country': 'United States', 'esg_score': 88, 'activity_tags': [], 'esg_score_status': 'approved'},
    {'issuer_id': 4, 'name': 'Northhaven Bank', 'sector': 'Financials', 'country': 'United Kingdom', 'esg_score': 73, 'activity_tags': [], 'esg_score_status': 'approved'},
    {'issuer_id': 5, 'name': 'Alderwell Health', 'sector': 'Healthcare', 'country': 'United Kingdom', 'esg_score': 89, 'activity_tags': [], 'esg_score_status': 'approved'},
    {'issuer_id': 9, 'name': 'Meridian Cloudworks', 'sector': 'Technology', 'country': 'United States', 'esg_score': 84, 'activity_tags': [], 'esg_score_status': 'approved'},
    {'issuer_id': 12, 'name': 'Redleaf Tobacco', 'sector': 'Tobacco', 'country': 'United Kingdom', 'esg_score': 22, 'activity_tags': ['tobacco'], 'esg_score_status': 'approved'},
    {'issuer_id': 13, 'name': 'Ironvale Defence', 'sector': 'Weapons', 'country': 'United States', 'esg_score': 35, 'activity_tags': ['weapons'], 'esg_score_status': 'approved'},
    {'issuer_id': 19, 'name': 'Everfield Renewables', 'sector': 'Utilities', 'country': 'Denmark', 'esg_score': 92, 'activity_tags': [], 'esg_score_status': 'approved'},
    {'issuer_id': 20, 'name': 'Greenhaven Water', 'sector': 'Utilities', 'country': 'United Kingdom', 'esg_score': 90, 'activity_tags': [], 'esg_score_status': 'approved'},
    {'issuer_id': 24, 'name': 'Clearstream Payments', 'sector': 'Financials', 'country': 'United States', 'esg_score': 82, 'activity_tags': [], 'esg_score_status': 'approved'},
    {'issuer_id': 33, 'name': 'Fairhaven Finance', 'sector': 'Financials', 'country': 'United Kingdom', 'esg_score': 84, 'activity_tags': [], 'esg_score_status': 'approved'},
    {'issuer_id': 36, 'name': 'LotusGate Internet', 'sector': 'Technology', 'country': 'India', 'esg_score': 64, 'activity_tags': [], 'esg_score_status': 'approved'},
    {'issuer_id': 37, 'name': 'JadeRiver Commerce', 'sector': 'Consumer Discretionary', 'country': 'China', 'esg_score': 59, 'activity_tags': [], 'esg_score_status': 'approved'},
    {'issuer_id': 38, 'name': 'Sundara Bank', 'sector': 'Financials', 'country': 'India', 'esg_score': 67, 'activity_tags': [], 'esg_score_status': 'approved'},
    {'issuer_id': 39, 'name': 'Pacifica Chips', 'sector': 'Technology', 'country': 'Taiwan', 'esg_score': 72, 'activity_tags': [], 'esg_score_status': 'approved'},
    {'issuer_id': 69, 'name': 'Deepwell Analytics', 'sector': 'Technology', 'country': 'United States', 'esg_score': 80, 'activity_tags': [], 'esg_score_status': 'approved'},
    {'issuer_id': 90, 'name': 'GBP Cash Reserve', 'sector': 'Cash', 'country': 'United Kingdom', 'esg_score': None, 'activity_tags': [], 'esg_score_status': 'not_applicable'},
]