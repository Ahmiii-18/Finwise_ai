from langchain_core.prompts import PromptTemplate, ChatPromptTemplate

SYSTEM_MESSAGE_TEXT = """You are FinWise AI, an expert educational financial advisory assistant. 
Your goal is to evaluate user cash flows, assess risk levels, and output structured JSON recommendations.
CRITICAL SAFETY & COMPLIANCE:
- You are providing EDUCATIONAL guidance only, not licensed financial or investment advice.
- Return output strictly as valid JSON adhering to the target schema."""

# Double curly braces {{ }} escape literal JSON brackets from LangChain variable parsing
JSON_SCHEMA_INSTRUCTIONS = """
{{
  "financial_summary": "Brief summary paragraph",
  "financial_health_score": 75,
  "spending_analysis": [
    {{"category": "category_name", "observation": "obs text", "recommendation": "rec text"}}
  ],
  "risk_level": "LOW | MEDIUM | HIGH",
  "top_priorities": ["priority 1", "priority 2"],
  "budget_recommendations": ["rec 1", "rec 2"],
  "savings_strategy": ["strategy 1"],
  "next_month_action_plan": ["step 1", "step 2"]
}}
"""

PROMPT_TEMPLATE_TEXT = """
Financial Data Analysis Request:
- Monthly Income: {monthly_income}
- Total Expenses: {total_expenses}
- Remaining Income: {remaining_income}
- Current Savings: {savings}
- Savings Ratio: {savings_ratio}%
- Expense Ratio: {expense_ratio}%
- Financial Goal: {financial_goal}
- Itemized Expenses: {expense_breakdown}

Analyze these details and supply JSON strictly following this schema:
""" + JSON_SCHEMA_INSTRUCTIONS

FINANCIAL_PROMPT_TEMPLATE = PromptTemplate(
    template=PROMPT_TEMPLATE_TEXT,
    input_variables=[
        "monthly_income", "total_expenses", "remaining_income",
        "savings", "savings_ratio", "expense_ratio",
        "financial_goal", "expense_breakdown"
    ]
)

CHAT_PROMPT_TEMPLATE = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_MESSAGE_TEXT),
    ("human", PROMPT_TEMPLATE_TEXT)
])

NARRATIVE_CHAT_TEMPLATE = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_MESSAGE_TEXT),
    ("human", "Provide an encouraging, step-by-step written coaching narrative based on goal '{financial_goal}', monthly income {monthly_income}, leftover balance {remaining_income}, and risk level assessment.")
])