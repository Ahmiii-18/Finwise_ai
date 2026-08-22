def calculate_financial_metrics(monthly_income: float, expenses: dict, current_savings: float) -> dict:
    total_expenses = sum(expenses.values())
    remaining_income = monthly_income - total_expenses
    
    # Guard against divide-by-zero
    if monthly_income > 0:
        savings_ratio = (current_savings / monthly_income) * 100
        expense_ratio = (total_expenses / monthly_income) * 100
    else:
        savings_ratio = 0.0
        expense_ratio = 0.0

    # Preliminary Weighted 0-100 Heuristic Score
    # 1. Savings Ratio Weight (30%)
    savings_score = min(100.0, (savings_ratio / 20.0) * 100) * 0.30
    
    # 2. Expense Ratio Weight (40%) - lower expense ratio gives higher score
    if expense_ratio <= 50:
        expense_score = 100.0
    elif expense_ratio >= 100:
        expense_score = 0.0
    else:
        expense_score = (100 - expense_ratio) * 2.0
    expense_score *= 0.40

    # 3. Leftover Cash Flow Weight (20%)
    leftover_score = (100.0 if remaining_income > 0 else 0.0) * 0.20

    # 4. Debt Burden Weight (10%)
    debt_exp = expenses.get("loan_debt", 0.0)
    debt_ratio = (debt_exp / monthly_income * 100) if monthly_income > 0 else 0.0
    debt_score = max(0.0, (100.0 - debt_ratio * 2)) * 0.10

    preliminary_score = int(round(savings_score + expense_score + leftover_score + debt_score))
    preliminary_score = max(0, min(100, preliminary_score))

    return {
        "total_expenses": total_expenses,
        "remaining_income": remaining_income,
        "savings_ratio": savings_ratio,
        "expense_ratio": expense_ratio,
        "preliminary_score": preliminary_score
    }