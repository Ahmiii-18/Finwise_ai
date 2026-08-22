import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

EXPENSE_CATEGORIES = [
    "housing",
    "food",
    "transportation",
    "utilities",
    "education",
    "healthcare",
    "entertainment",
    "loan_debt",
    "other"
]

FINANCIAL_GOALS = [
    "Save Money",
    "Build Emergency Fund",
    "Pay Off Debt",
    "Vacation",
    "Start a Business",
    "Improve Budgeting"
]

CURRENCIES = ["USD ($)", "EUR (€)", "GBP (£)", "PKR (Rs)"]