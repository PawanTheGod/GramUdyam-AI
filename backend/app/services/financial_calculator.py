"""
GramUdyam AI – Financial Calculator
=====================================

Implements actual EMI, break-even, ROI, and DSCR calculations.
"""

import math
from typing import Dict


def calculate_emi(principal: float, annual_rate: float, months: int) -> float:
    """
    Standard EMI formula:
    EMI = P × r × (1+r)^n / ((1+r)^n - 1)
    where r = monthly interest rate, n = number of months
    """
    if principal <= 0 or months <= 0:
        return 0.0
    if annual_rate <= 0:
        return principal / months

    r = annual_rate / (12 * 100)  # monthly interest rate
    power = math.pow(1 + r, months)
    emi = principal * r * power / (power - 1)
    return round(emi, 2)


def calculate_break_even(
    total_investment: float,
    monthly_profit: float,
    emi: float = 0,
) -> int:
    """Months until cumulative profit covers the investment."""
    if monthly_profit <= 0:
        return 999  # never breaks even
    net_monthly = monthly_profit - emi
    if net_monthly <= 0:
        return 999
    months = math.ceil(total_investment / net_monthly)
    return min(months, 999)


def calculate_roi(annual_profit: float, total_investment: float) -> float:
    """Return on Investment as percentage."""
    if total_investment <= 0:
        return 0.0
    return round((annual_profit / total_investment) * 100, 1)


def calculate_dscr(monthly_income: float, monthly_debt_service: float) -> float:
    """
    Debt Service Coverage Ratio.
    DSCR > 1.25 is generally considered healthy.
    """
    if monthly_debt_service <= 0:
        return 99.0  # no debt
    return round(monthly_income / monthly_debt_service, 2)


def generate_financial_plan(
    project_cost: float,
    user_contribution: float,
    expected_monthly_revenue: float,
    monthly_operating_cost: float,
    interest_rate: float = 8.5,
    repayment_months: int = 60,
    working_capital_months: int = 3,
) -> Dict:
    """
    Generate a complete financial plan for a business opportunity.

    Args:
        project_cost: Total project / setup cost
        user_contribution: Capital the farmer can invest
        expected_monthly_revenue: Expected monthly revenue
        monthly_operating_cost: Monthly operating expenses
        interest_rate: Annual interest rate (%)
        repayment_months: Loan tenure in months
        working_capital_months: How many months of working capital to budget
    """
    # Calculate working capital
    working_capital = monthly_operating_cost * working_capital_months
    total_cost = project_cost + working_capital

    # Fixed cost = project cost (setup, equipment, etc.)
    fixed_cost = project_cost

    # Determine loan amount
    actual_contribution = min(user_contribution, total_cost)
    loan_amount = max(total_cost - actual_contribution, 0)

    # Calculate EMI
    emi = calculate_emi(loan_amount, interest_rate, repayment_months)

    # Monthly P&L
    monthly_profit = expected_monthly_revenue - monthly_operating_cost
    net_monthly_after_emi = monthly_profit - emi

    # Break-even
    break_even = calculate_break_even(total_cost, monthly_profit, emi)

    # Annual income (after EMI)
    annual_income = net_monthly_after_emi * 12

    # ROI
    roi = calculate_roi(annual_income, total_cost)

    # DSCR
    dscr = calculate_dscr(monthly_profit, emi) if emi > 0 else 99.0

    return {
        "project_cost": round(project_cost, 2),
        "fixed_cost": round(fixed_cost, 2),
        "working_capital": round(working_capital, 2),
        "user_contribution": round(actual_contribution, 2),
        "loan_amount": round(loan_amount, 2),
        "interest_rate": interest_rate,
        "emi": emi,
        "repayment_months": repayment_months,
        "expected_monthly_revenue": round(expected_monthly_revenue, 2),
        "monthly_expenses": round(monthly_operating_cost, 2),
        "monthly_profit": round(net_monthly_after_emi, 2),
        "break_even_months": break_even,
        "annual_income": round(annual_income, 2),
        "roi_percentage": roi,
        "dscr": dscr,
    }
