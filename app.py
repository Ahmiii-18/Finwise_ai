"""
app.py
------
Streamlit Financial Dashboard for FinWise AI.
"""
import streamlit as st
import matplotlib.pyplot as plt
from src.config import APP_TITLE, APP_SUBTITLE, DISCLAIMER_TEXT, FINANCIAL_GOALS, CURRENCIES, EXPENSE_CATEGORIES
from src.financial_calculator import calculate_financials, calculate_preliminary_score
from src.chains import build_llm, build_financial_chain, stream_recommendations
from src.cache_manager import configure_cache
from src.utils import parse_llm_json

st.set_page_config(page_title=APP_TITLE, page_icon="💰", layout="wide")

# Custom Styling
st.markdown("""
<style>
    .stApp header { background-color: transparent; }
    .header-card {
        background-color: #0e2a47;
        padding: 1.8rem;
        border-radius: 10px;
        color: #ffffff !important;
        margin-bottom: 1.5rem;
    }
    .header-card h1, .header-card p { color: #ffffff !important; }
    .disclaimer-box {
        background-color: #3b1111;
        color: #ffcdd2;
        padding: 0.8rem;
        border-radius: 6px;
        font-size: 0.85rem;
        border: 1px solid #e53935;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Header Banner
st.markdown(f"""
<div class="header-card">
    <h1>💰 {APP_TITLE}</h1>
    <p>{APP_SUBTITLE}</p>
</div>
""", unsafe_allow_html=True)

# Disclaimer
st.markdown(f'<div class="disclaimer-box">⚠️ <b>{DISCLAIMER_TEXT}</b></div>', unsafe_allow_html=True)

# Sidebar Configuration
st.sidebar.title("🛠️ Settings & Config")
model_name = st.sidebar.selectbox("OpenAI Model", ["gpt-4o-mini", "gpt-4o"], index=0)
cache_option = st.sidebar.radio("Cache Mode", ["InMemoryCache", "SQLiteCache", "Disabled"], index=0)

cache_msg = configure_cache(cache_option)
st.sidebar.info(cache_msg)

if st.sidebar.button("Reset Session State"):
    st.session_state.clear()
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown("### Educational Notice\nFinWise AI is a prototype built for educational evaluation.")

# Main Form
with st.form("financial_form"):
    st.subheader("1. Financial Profile Inputs")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        currency = st.selectbox("Currency", CURRENCIES, index=0)
        monthly_income = st.number_input("Monthly Income", min_value=0.0, value=5000.0, step=100.0)
    with col2:
        current_savings = st.number_input("Current Savings", min_value=0.0, value=1000.0, step=100.0)
    with col3:
        financial_goal = st.selectbox("Financial Goal", FINANCIAL_GOALS, index=0)

    st.subheader("2. Monthly Expense Categories")
    exp_cols = st.columns(3)
    expenses = {}
    
    default_vals = [1200.0, 500.0, 300.0, 200.0, 100.0, 150.0, 200.0, 400.0, 150.0]
    for idx, category in enumerate(EXPENSE_CATEGORIES):
        with exp_cols[idx % 3]:
            expenses[category] = st.number_input(
                category.replace('_', ' ').title(),
                min_value=0.0,
                value=default_vals[idx],
                step=50.0
            )

    submit_btn = st.form_submit_button("Analyse Financials", type="primary")

if submit_btn:
    # 1. Deterministic Python Calculations
    calc_results = calculate_financials(monthly_income, expenses, current_savings)
    preliminary_score = calculate_preliminary_score(calc_results, expenses.get("loan_debt", 0.0))

    st.markdown("---")
    st.header("📊 Financial Overview & Analysis")

    # Metrics Display
    curr_symbol = currency.split()[0]
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Monthly Income", f"{curr_symbol} {calc_results['monthly_income']:,.2f}")
    m2.metric("Total Expenses", f"{curr_symbol} {calc_results['total_expenses']:,.2f}")
    m3.metric("Remaining Balance", f"{curr_symbol} {calc_results['remaining_income']:,.2f}")
    m4.metric("Savings Ratio", f"{calc_results['savings_ratio']}%")

    # Score comparison
    sc1, sc2 = st.columns(2)
    with sc1:
        st.subheader("Deterministic Preliminary Score")
        st.progress(preliminary_score / 100)
        st.write(f"**Score:** {preliminary_score} / 100")

    # 2. LLM Execution via LCEL Chain
    with st.spinner("Connecting to LangChain LLM for AI Analysis..."):
        llm = build_llm(model_name=model_name, temperature=0.2)
        chain = build_financial_chain(llm)

        chain_inputs = {
            "currency": curr_symbol,
            "monthly_income": calc_results["monthly_income"],
            "total_expenses": calc_results["total_expenses"],
            "remaining_income": calc_results["remaining_income"],
            "savings": calc_results["current_savings"],
            "savings_ratio": calc_results["savings_ratio"],
            "expense_ratio": calc_results["expense_ratio"],
            "financial_goal": financial_goal,
            "expense_breakdown": str(expenses)
        }

        try:
            raw_response = chain.invoke(chain_inputs).content
            ai_data = parse_llm_json(raw_response)

            with sc2:
                st.subheader("AI Health Score")
                ai_score = ai_data.get("financial_health_score", 50)
                st.progress(ai_score / 100)
                st.write(f"**Score:** {ai_score} / 100 | **Risk Level:** {ai_data.get('risk_level', 'UNKNOWN')}")

            # Tabs for Detailed AI Insights
            tab1, tab2, tab3, tab4 = st.tabs(["📋 Summary & Analysis", "🎯 Priorities & Plan", "📊 Expense Chart", "📝 Streamed Narrative"])

            with tab1:
                st.write("### Financial Summary")
                st.info(ai_data.get("financial_summary", "N/A"))
                
                st.write("### Itemized Spending Analysis")
                for item in ai_data.get("spending_analysis", []):
                    with st.expander(f"Category: {item.get('category')}"):
                        st.write(f"**Observation:** {item.get('observation')}")
                        st.write(f"**Recommendation:** {item.get('recommendation')}")

            with tab2:
                st.write("### Top Priorities")
                for p in ai_data.get("top_priorities", []):
                    st.write(f"- {p}")

                st.write("### Next Month Action Plan")
                for a in ai_data.get("next_month_action_plan", []):
                    st.write(f"1. {a}")

            with tab3:
                st.write("### Expense Breakdown Visualization")
                fig, ax = plt.subplots()
                non_zero_expenses = {k.replace('_', ' ').title(): v for k, v in expenses.items() if v > 0}
                if non_zero_expenses:
                    ax.pie(non_zero_expenses.values(), labels=non_zero_expenses.keys(), autopct='%1.1f%%', startangle=90)
                    ax.axis('equal')
                    st.pyplot(fig)
                else:
                    st.write("No expenses to display.")

            with tab4:
                st.write("### Live Streamed Recommendations")
                stream_llm = build_llm(model_name=model_name, temperature=0.5, streaming=True)
                stream_input = {
                    "financial_summary": ai_data.get("financial_summary", ""),
                    "financial_goal": financial_goal,
                    "risk_level": ai_data.get("risk_level", "MEDIUM")
                }
                st.write_stream(stream_recommendations(stream_llm, stream_input))

        except Exception as e:
            st.error(f"Error processing AI assessment: {str(e)}")