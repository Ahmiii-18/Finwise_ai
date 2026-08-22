import streamlit as st
import json
from src.config import EXPENSE_CATEGORIES, FINANCIAL_GOALS, CURRENCIES
from src.financial_calculator import calculate_financial_metrics
from src.cache_manager import setup_cache
from src.chains import run_financial_chain, stream_recommendations

# -----------------------------------------------------------------------
# PAGE CONFIGURATION
# -----------------------------------------------------------------------
st.set_page_config(
    page_title="FinWise AI | Personal Wealth & Budget Engine",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------
# MODERN CUSTOM STYLES (CSS)
# -----------------------------------------------------------------------
CUSTOM_CSS = """
<style>
    :root {
        --fw-bg: #faf9f6;
        --fw-bg-soft: #f2f0ea;
        --fw-text: #1e293b;
        --fw-text-muted: #64748b;
        --fw-border: rgba(30, 41, 59, 0.15);
        --fw-accent: #059669;
        --fw-accent-hover: #047857;
    }

    .stApp { background-color: var(--fw-bg); color: var(--fw-text); font-family: 'Inter', sans-serif; }
    .stApp, .stApp p, .stApp span, .stApp li, .stApp label, .stApp div, .stApp h1, .stApp h2, .stApp h3 { color: var(--fw-text); }

    /* Sidebar Customization */
    section[data-testid="stSidebar"] { background: var(--fw-bg-soft); border-right: 1px solid var(--fw-border); }
    section[data-testid="stSidebar"] * { color: var(--fw-text); }

    div[data-testid="stWidgetLabel"] p, div[data-testid="stWidgetLabel"] label {
        color: var(--fw-text) !important;
        font-weight: 600 !important;
    }

    /* Input Fields & Textareas */
    div[data-baseweb="input"] input,
    div[data-baseweb="textarea"] textarea,
    textarea, input[type="text"], input[type="number"] {
        color: var(--fw-text) !important;
        background-color: #ffffff !important;
        border: 1px solid var(--fw-border) !important;
        border-radius: 8px !important;
        transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out !important;
    }

    /* Focus States */
    div[data-baseweb="input"]:focus-within,
    div[data-baseweb="textarea"]:focus-within,
    div[data-baseweb="select"]:focus-within,
    textarea:focus, 
    input[type="text"]:focus,
    input[type="number"]:focus {
        border-color: #059669 !important;
        box-shadow: 0 0 0 3px rgba(5, 150, 105, 0.25) !important;
        outline: none !important;
    }

    /* Select Dropdowns */
    div[data-baseweb="select"] > div {
        background-color: #ffffff !important;
        border-color: var(--fw-border) !important;
        border-radius: 8px !important;
    }
    div[data-baseweb="select"] * { color: var(--fw-text) !important; }

    /* Header Banner */
    .modern-header {
        background: linear-gradient(135deg, #064e3b 0%, #047857 100%);
        border-radius: 18px;
        padding: clamp(1.2rem, 3vw, 2.2rem);
        margin-bottom: 1.8rem;
        display: flex;
        align-items: center;
        gap: 1.5rem;
        flex-wrap: wrap;
        box-shadow: 0 4px 20px rgba(6, 78, 59, 0.15);
    }
    .modern-header * { color: #ffffff !important; }

    .header-logo {
        width: 64px; height: 64px;
        background: rgba(255, 255, 255, 0.12);
        padding: 0.5rem;
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        display: flex; align-items: center; justify-content: center;
    }

    /* Glass Cards */
    .glass-card {
        background: #ffffff;
        border: 1px solid var(--fw-border);
        border-radius: 14px;
        padding: 1.3rem;
        margin-bottom: 1.2rem;
        box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
    }

    /* Metric Cards Grid */
    .metric-card-box {
        background: #ffffff;
        border: 1px solid var(--fw-border);
        border-radius: 12px;
        padding: 1rem 1.2rem;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04);
    }
    .metric-title { font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.05em; color: var(--fw-text-muted); font-weight: 700; }
    .metric-value { font-size: 1.5rem; font-weight: 800; color: var(--fw-text); margin-top: 0.2rem; }

    /* Form Buttons */
    .stButton > button, div[data-testid="stFormSubmitButton"] > button {
        background: #059669 !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.65rem 1.4rem !important;
        width: 100% !important;
        transition: background 0.2s ease !important;
    }
    .stButton > button:hover, div[data-testid="stFormSubmitButton"] > button:hover {
        background: #047857 !important;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

def get_logo_svg(size=40):
    return f'''<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="#34d399" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M2 17L12 22L22 17" stroke="#34d399" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M2 12L12 17L22 12" stroke="#34d399" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'''

# -----------------------------------------------------------------------
# SIDEBAR
# -----------------------------------------------------------------------
with st.sidebar:
    st.markdown(
        f'<div style="display:flex; align-items:center; gap:0.7rem; margin-bottom:0.2rem;">'
        f'{get_logo_svg(36)}'
        f'<div style="font-size:1.3rem; font-weight:800; color:#059669;">FinWise AI</div>'
        f'</div>',
        unsafe_allow_html=True
    )
    st.caption("Financial Advisory Engine v2.0")

    st.divider()
    st.markdown("### ⚙️ Engine Parameters")
    cache_type = st.radio("Caching Mechanism", ["InMemoryCache", "SQLiteCache"], index=0)
    setup_cache(cache_type)
    
    if st.button("🔄 Reset Session State"):
        st.session_state.clear()
        st.rerun()

    st.divider()
    st.markdown('<div style="font-size: 0.78rem; color: #64748b;">⚠️ <b>EDUCATIONAL DISCLAIMER:</b> Prototype for informational use only. Not certified financial advice.</div>', unsafe_allow_html=True)

# -----------------------------------------------------------------------
# HEADER BANNER
# -----------------------------------------------------------------------
st.markdown(f"""
    <div class="modern-header">
        <div class="header-logo">{get_logo_svg(48)}</div>
        <div>
            <h1 style="margin:0; font-size:2rem; font-weight:800;">FinWise AI Budget & Wealth Engine</h1>
            <p style="margin:0.3rem 0 0 0; opacity:0.9;">Algorithmic cash-flow tracking, debt reduction strategies, and financial planning.</p>
        </div>
    </div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------
# INTAKE FORM
# -----------------------------------------------------------------------
with st.form("financial_form"):
    st.markdown("#### 💰 Income & Primary Reserves")
    col1, col2, col3 = st.columns(3)
    with col1:
        monthly_income = st.number_input("Monthly Income", min_value=0.0, value=5000.0, step=100.0)
    with col2:
        current_savings = st.number_input("Current Savings", min_value=0.0, value=15000.0, step=500.0)
    with col3:
        currency = st.selectbox("Currency Unit", CURRENCIES)

    st.markdown("#### 📊 Itemized Monthly Expenses")
    exp_cols = st.columns(3)
    expenses = {}
    for idx, category in enumerate(EXPENSE_CATEGORIES):
        with exp_cols[idx % 3]:
            expenses[category] = st.number_input(
                f"{category.replace('_', ' ').title()}", 
                min_value=0.0, 
                value=200.0 if category != "housing" else 1500.0, 
                step=50.0
            )

    st.markdown("#### 🎯 Strategic Priority Focus")
    financial_goal = st.selectbox("Financial Focus Area", FINANCIAL_GOALS)
    
    submitted = st.form_submit_button("🚀 Run Wealth & Advisory Synthesis")

# -----------------------------------------------------------------------
# COMPUTATION & DASHBOARD DISPLAY
# -----------------------------------------------------------------------
if submitted:
    # 1. Deterministic Python Calculations
    metrics = calculate_financial_metrics(monthly_income, expenses, current_savings)
    curr_sym = currency.split()[1]

    st.divider()
    
    # 2. Financial Metrics Cards Grid
    st.markdown("### 📈 Deterministic Cash-Flow Analytics")
    m1, m2, m3, m4, m5 = st.columns(5)
    
    with m1:
        st.markdown(f'''<div class="metric-card-box"><div class="metric-title">Total Expenses</div><div class="metric-value">{curr_sym} {metrics["total_expenses"]:,.2f}</div></div>''', unsafe_allow_html=True)
    with m2:
        st.markdown(f'''<div class="metric-card-box"><div class="metric-title">Remaining Cash</div><div class="metric-value">{curr_sym} {metrics["remaining_income"]:,.2f}</div></div>''', unsafe_allow_html=True)
    with m3:
        st.markdown(f'''<div class="metric-card-box"><div class="metric-title">Savings Ratio</div><div class="metric-value">{metrics["savings_ratio"]:.1f}%</div></div>''', unsafe_allow_html=True)
    with m4:
        st.markdown(f'''<div class="metric-card-box"><div class="metric-title">Expense Ratio</div><div class="metric-value">{metrics["expense_ratio"]:.1f}%</div></div>''', unsafe_allow_html=True)
    with m5:
        st.markdown(f'''<div class="metric-card-box"><div class="metric-title">Rule Score</div><div class="metric-value">{metrics["preliminary_score"]}/100</div></div>''', unsafe_allow_html=True)

    # 3. Execute LangChain Chain
    chain_inputs = {
        "monthly_income": monthly_income,
        "total_expenses": metrics["total_expenses"],
        "remaining_income": metrics["remaining_income"],
        "savings": current_savings,
        "savings_ratio": metrics["savings_ratio"],
        "expense_ratio": metrics["expense_ratio"],
        "financial_goal": financial_goal,
        "expense_breakdown": json.dumps(expenses)
    }

    with st.spinner("AI Synthesis in progress..."):
        ai_result = run_financial_chain(chain_inputs)

    st.divider()
    st.markdown("### 🤖 LangChain AI Wealth Insights")

    # Health & Risk Indicators Card
    c_score, c_risk = st.columns(2)
    score = ai_result.get("financial_health_score", 50)
    risk_lvl = ai_result.get("risk_level", "UNKNOWN").upper()

    with c_score:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown(f"**AI Health Score:** `{score}/100`")
        st.progress(score / 100)
        st.markdown('</div>', unsafe_allow_html=True)

    with c_risk:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("**Risk Level Assessment:**")
        if risk_lvl == "LOW":
            st.success(f"🟢 {risk_lvl} RISK")
        elif risk_lvl in ["MEDIUM", "MODERATE"]:
            st.warning(f"🟡 {risk_lvl} RISK")
        else:
            st.error(f"🔴 {risk_lvl} RISK")
        st.markdown('</div>', unsafe_allow_html=True)

    # Tabs Section
    t_summary, t_analysis, t_plan = st.tabs(["📋 Executive Summary", "🔍 Category Analysis", "🎯 Strategic Action Plan"])

    with t_summary:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### Financial Assessment")
        st.write(ai_result.get("financial_summary", ""))
        st.markdown("#### High-Priority Focus Areas")
        for priority in ai_result.get("top_priorities", []):
            st.write(f"• {priority}")
        st.markdown('</div>', unsafe_allow_html=True)

    with t_analysis:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### Categorical Spend Evaluation")
        for item in ai_result.get("spending_analysis", []):
            with st.expander(f"📁 {item.get('category', 'Category').replace('_', ' ').title()}"):
                st.write(f"**Observation:** {item.get('observation', '')}")
                st.write(f"**Recommendation:** {item.get('recommendation', '')}")
        st.markdown('</div>', unsafe_allow_html=True)

    with t_plan:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        col_plan_a, col_plan_b = st.columns(2)
        with col_plan_a:
            st.markdown("#### Budget & Savings Recommendations")
            for rec in ai_result.get("budget_recommendations", []):
                st.write(f"• {rec}")
            for strat in ai_result.get("savings_strategy", []):
                st.write(f"• {strat}")
        with col_plan_b:
            st.markdown("#### Next Month Action Items")
            for idx, act in enumerate(ai_result.get("next_month_action_plan", []), 1):
                st.write(f"**{idx}.** {act}")
        st.markdown('</div>', unsafe_allow_html=True)

    # Streamed Live Narrative Response
    st.divider()
    st.markdown("### 🎙️ Real-Time Financial Advisory Narrative")
    st.markdown('<div class="glass-card" style="border-left: 5px solid #059669;">', unsafe_allow_html=True)
    st.write_stream(stream_recommendations(chain_inputs))
    st.markdown('</div>', unsafe_allow_html=True)