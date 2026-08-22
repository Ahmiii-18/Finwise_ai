"""
src/config.py
-------------
Application settings, financial goal options, currency selections, and default values.
"""
import os
from dotenv import load_dotenv

load_dotenv()

APP_TITLE = "FinWise AI"
APP_SUBTITLE = "AI-Powered Personal Financial Analysis & Smart Budget Assistant"

DISCLAIMER_TEXT = (
    "EDUCATIONAL USE ONLY: This prototype provides educational financial analysis. "
    "It does not provide guaranteed investment advice, execute transactions, or replace a qualified financial professional."
)

FINANCIAL_GOALS = [
    "Save Money",
    "Build Emergency Fund",
    "Pay Off Debt",
    "Vacation / Major Purchase",
    "Start a Business",
    "Improve Budgeting Habits",
]

CURRENCIES = ["USD ($)", "EUR (€)", "GBP (£)", "INR (₹)", "CAD ($)", "AUD ($)"]

EXPENSE_CATEGORIES = [
    "housing",
    "food",
    "transportation",
    "utilities",
    "education",
    "healthcare",
    "entertainment",
    "loan_debt",
    "other",
]