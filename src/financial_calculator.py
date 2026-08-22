"""
src/financial_calculator.py
---------------------------
Deterministic Python financial calculations and preliminary rule-based scoring (No AI).
"""

def calculate_financials(monthly_income: float, expenses: dict, current_savings: float) -> dict:
    """Computes total expenses, remaining income, savings ratio, and expense ratio."""
    total_expenses = sum(expenses.values())
    remaining_income = monthly_income - total_expenses

    if monthly_income <= 0:
        savings_ratio = 0.0
        expense_ratio = 0.0
    else:
        savings_ratio = (current_savings / monthly_income) * 100
        expense_ratio = (total_expenses / monthly_income) * 100

    return {
        "monthly_income": round(monthly_income, 2),
        "total_expenses": round(total_expenses, 2),
        "remaining_income": round(remaining_income, 2),
        "savings_ratio": round(savings_ratio, 2),
        "expense_ratio": round(expense_ratio, 2),
        "current_savings": round(current_savings, 2),
    }

def calculate_preliminary_score(financials: dict, debt_expense: float) -> int:
    """Calculates a rule-based preliminary score (0-100) based on weighted heuristics."""
    income = financials["monthly_income"]
    if income <= 0:
        return 0

    score = 100.0

    # 1. Expense ratio penalty
    expense_ratio = financials["expense_ratio"]
    if expense_ratio > 100:
        score -= 40
    elif expense_ratio > 80:
        score -= 25
    elif expense_ratio > 60:
        score -= 10

    # 2. Savings ratio reward / penalty
    savings_ratio = financials["savings_ratio"]
    if savings_ratio >= 20:
        score += 10
    elif savings_ratio < 5:
        score -= 15

    # 3. Leftover income penalty
    if financials["remaining_income"] < 0:
        score -= 20

    # 4. Debt burden penalty
    debt_ratio = (debt_expense / income) * 100
    if debt_ratio > 40:
        score -= 20
    elif debt_ratio > 20:
        score -= 10

    return max(0, min(100, int(score)))