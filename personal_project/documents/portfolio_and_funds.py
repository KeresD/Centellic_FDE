from typing import Any

PORTFOLIOS: list[dict[str, Any]] = [
    {'portfolio_id': 1, 'name': 'Haven Cancer Support Growth Portfolio', 'client_name': 'Haven Cancer Support Trust', 'mandate_id': 1, 'valuation_gbp': 2000000, 'as_of_date': '2026-09-30', 'synthetic': True},
    {'portfolio_id': 2, 'name': 'Willow Community Responsible Portfolio', 'client_name': 'Willow Community Foundation', 'mandate_id': 2, 'valuation_gbp': 1250000, 'as_of_date': '2026-09-30', 'synthetic': True},
    {'portfolio_id': 3, 'name': 'Hartwell Long-Term Growth Portfolio', 'client_name': 'Sofia Hartwell', 'mandate_id': 3, 'valuation_gbp': 350000, 'as_of_date': '2026-09-30', 'synthetic': True},
    {'portfolio_id': 4, 'name': 'Marlow Retirement Income Portfolio', 'client_name': 'Evan Marlow', 'mandate_id': 4, 'valuation_gbp': 600000, 'as_of_date': '2026-09-30', 'synthetic': True},
    {'portfolio_id': 5, 'name': 'Ashcombe Research Allocation Portfolio', 'client_name': 'Ashcombe Research Endowment', 'mandate_id': 5, 'valuation_gbp': 3000000, 'as_of_date': '2026-09-30', 'synthetic': True},
]

PORTFOLIO_FUNDS: list[dict[str, Any]] = [
    {'portfolio_fund_id': 1, 'portfolio_id': 1, 'fund_id': 1, 'weight': 50, 'as_of_date': '2026-09-30', 'synthetic': True},
    {'portfolio_fund_id': 2, 'portfolio_id': 1, 'fund_id': 2, 'weight': 30, 'as_of_date': '2026-09-30', 'synthetic': True},
    {'portfolio_fund_id': 3, 'portfolio_id': 1, 'fund_id': 6, 'weight': 20, 'as_of_date': '2026-09-30', 'synthetic': True},
    {'portfolio_fund_id': 4, 'portfolio_id': 2, 'fund_id': 2, 'weight': 70, 'as_of_date': '2026-09-30', 'synthetic': True},
    {'portfolio_fund_id': 5, 'portfolio_id': 2, 'fund_id': 6, 'weight': 30, 'as_of_date': '2026-09-30', 'synthetic': True},
    {'portfolio_fund_id': 6, 'portfolio_id': 3, 'fund_id': 5, 'weight': 60, 'as_of_date': '2026-09-30', 'synthetic': True},
    {'portfolio_fund_id': 7, 'portfolio_id': 3, 'fund_id': 1, 'weight': 40, 'as_of_date': '2026-09-30', 'synthetic': True},
    {'portfolio_fund_id': 8, 'portfolio_id': 4, 'fund_id': 4, 'weight': 40, 'as_of_date': '2026-09-30', 'synthetic': True},
    {'portfolio_fund_id': 9, 'portfolio_id': 4, 'fund_id': 6, 'weight': 60, 'as_of_date': '2026-09-30', 'synthetic': True},
    {'portfolio_fund_id': 10, 'portfolio_id': 5, 'fund_id': 3, 'weight': 20, 'as_of_date': '2026-09-30', 'synthetic': True},
    {'portfolio_fund_id': 11, 'portfolio_id': 5, 'fund_id': 2, 'weight': 40, 'as_of_date': '2026-09-30', 'synthetic': True},
    {'portfolio_fund_id': 12, 'portfolio_id': 5, 'fund_id': 6, 'weight': 40, 'as_of_date': '2026-09-30', 'synthetic': True},
]