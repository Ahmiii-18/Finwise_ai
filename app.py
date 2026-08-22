"""
app.py
------
FinWise AI - Modern Personal Financial Advisory & Portfolio Engine.

Features:
- Real inline-SVG brand logo (header + sidebar)
- High-contrast responsive adaptive theme
- Focus ring highlighting on all input boxes & text areas
- Financial Health Intake & Cash Flow Analytics
- Multi-Metric Advisory (Budgeting, Debt, Savings, Investment Rationale)
- Target-Based Financial Refinement Protocol
- Real-Time Token Streaming Advice Engine
- Fully responsive layout across mobile, tablet, and desktop
"""

import json
import os
import time
import streamlit as st

# -----------------------------------------------------------------------
# CONFIG & STYLES
# -----------------------------------------------------------------------
st.set_page_config(
    page_title="FinWise AI | Personal Wealth & Budget Assistant",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded"
)

CUSTOM_CSS = """
<style>
    :root {
        --fw-bg: #faf9f6;
        --fw-bg-soft: #f2f0ea;
        --fw-text: #1e293b;
        --fw-text-muted: #64748b;
        --fw-border: rgba(30, 41, 59, 0.18);
        --fw-accent: #059669;
    }

    .stApp { background-color: var(--fw-bg); color: var(--fw-text); font-family: 'Inter', sans-serif; }
    .stApp, .stApp p, .stApp span, .stApp li, .stApp label, .stApp div, .stApp h1, .stApp h2, .stApp h3 { color: var(--fw-text); }

    section[data-testid="stSidebar"] { background: var(--fw-bg-soft); border-right: 1px solid var(--fw-border); }
    section[data-testid="stSidebar"] * { color: var(--fw-text); }

    div[data-testid="stWidgetLabel"] p, div[data-testid="stWidgetLabel"] label {
        color: var(--fw-text) !important;
        font-weight: 600 !important;
    }

    /* Base Styling for Inputs */
    div[data-baseweb="input"] input,
    div[data-baseweb="textarea"] textarea,
    textarea, input[type="text"], input[type="number"] {
        color: var(--fw-text) !important;
        background-color: #ffffff !important;
        border: 1px solid var(--fw-border) !important;
        border-radius: 8px !important;
        transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out !important;
    }

    /* FOCUS STATES FOR ALL INPUT BOXES */
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

    /* Select Customization */
    div[data-baseweb="select"] > div {
        background-color: #ffffff !important;
        border-color: var(--fw-border) !important;
        border-radius: 8px !important;
    }
    div[data-baseweb="select"] * { color: var(--fw-text) !important; }

    /* Modern Header */
    .modern-header {
        background: linear-gradient(135deg, #064e3b 0%, #047857 100%);
        border-radius: 18px;
        padding: clamp(1.2rem, 3vw, 2.2rem);
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 1.5rem;
        flex-wrap: wrap;
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

    .glass-card {
        background: #ffffff;
        border: 1px solid var(--fw-border);
        border-radius: 14px;
        padding: 1.2rem;
        margin-bottom: 1rem;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.05);
    }

    .stButton > button, div[data-testid="stFormSubmitButton"] > button {
        background: #059669 !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.6rem 1.3rem !important;
        width: 100% !important;
    }
    .stButton > button:hover, div[data-testid="stFormSubmitButton"] > button:hover {
        background: #047857 !important;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

def logo_svg(size=40):
    return f"""
    <svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="#34d399" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        <path d="M2 17L12 22L22 17" stroke="#34d399" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        <path d="M2 12L12 17L22 12" stroke="#34d399" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
    """

# -----------------------------------------------------------------------
# SIDEBAR
# -----------------------------------------------------------------------
with st.sidebar:
    st.markdown(f"""
        <div style="display:flex; align-items:center; gap:0.7rem; margin-bottom:0.2rem;">
            {logo_svg(36)}
            <div style="font-size:1.3rem; font-weight:800; color:#059669;">FinWise AI</div>
        </div>
    """, unsafe_allow_html=True)
    st.caption("Financial Advisory Engine v2.0")

    st.divider()
    st.markdown("### ⚙️ Engine Parameters")
    risk_profile = st.selectbox("Risk Tolerance", ["Conservative", "Moderate", "Growth", "Aggressive"], index=1)
    currency = st.selectbox("Currency", ["USD ($)", "EUR (€)", "GBP (£)", "PKR (Rs)"], index=0)
    st.divider()
    st.markdown('<div style="font-size: 0.78rem; color: #64748b;">Financial advice generated by FinWise AI is for educational reference only.</div>', unsafe_allow_html=True)

# -----------------------------------------------------------------------
# HEADER BANNER
# -----------------------------------------------------------------------
st.markdown(f"""
    <div class="modern-header">
        <div class="header-logo">{logo_svg(48)}</div>
        <div>
            <h1 style="margin:0; font-size:2rem; font-weight:800;">FinWise AI Budget & Wealth Engine</h1>
            <p style="margin:0.3rem 0 0 0; opacity:0.9;">Algorithmic cash-flow tracking, debt reduction strategies, and financial planning.</p>
        </div>
    </div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------
# INTAKE FORM
# -----------------------------------------------------------------------
with st.form("financial_intake_form"):
    st.markdown("#### 💰 Income & Essential Cash Flow")
    c1, c2, c3 = st.columns(3)
    with c1:
        monthly_income = st.number_input("Monthly Income", min_value=0.0, value=5000.0, step=100.0)
    with c2:
        fixed_expenses = st.number_input("Fixed Expenses (Rent, Utilities)", min_value=0.0, value=2000.0, step=50.0)
    with c3:
        variable_expenses = st.number_input("Variable Expenses (Food, Leisure)", min_value=0.0, value=1200.0, step=50.0)

    st.markdown("#### 🏦 Assets & Liabilities")
    col_a1, col_a2 = st.columns(2)
    with col_a1:
        total_savings = st.number_input("Total Savings & Investments", min_value=0.0, value=15000.0, step=500.0)
    with col_a2:
        total_debt = st.number_input("Total High-Interest Debt", min_value=0.0, value=3000.0, step=250.0)

    st.markdown("#### 🎯 Financial Goals & Priorities")
    goals = st.text_area(
        "Narrative Goals & Notes",
        placeholder="e.g. Save $10,000 for emergency fund, pay off credit cards within 12 months, start investing in index funds.",
        height=100
    )

    submitted = st.form_submit_button("🚀 Run Wealth & Advisory Synthesis")

# -----------------------------------------------------------------------
# COMPUTATION & RESULTS DASHBOARD
# -----------------------------------------------------------------------
if submitted:
    net_savings = monthly_income - (fixed_expenses + variable_expenses)
    savings_rate = (net_savings / monthly_income * 100) if monthly_income > 0 else 0.0

    st.divider()
    
    # Financial Metrics Cards
    st.markdown(f"""
        <div class="glass-card" style="border-left: 6px solid #059669;">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem;">
                <div>
                    <span style="font-size: 0.85rem; color: #64748b; text-transform: uppercase;">Net Monthly Surplus</span>
                    <h2 style="margin: 0; color: #059669; font-size: 1.8rem;">{currency.split()[1]} {net_savings:,.2f} / mo</h2>
                </div>
                <div>
                    <span style="font-size: 0.85rem; color: #64748b; text-transform: uppercase;">Savings Rate</span>
                    <h2 style="margin: 0; color: #1e293b; font-size: 1.8rem;">{savings_rate:.1f}%</h2>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    tab_summary, tab_strategy, tab_insights = st.tabs([
        "📊 Cash Flow Overview",
        "💡 Strategic Plan",
        "🎯 Optimization Recommendations"
    ])

    with tab_summary:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### Cash Flow Breakdown")
        st.write(f"• **Monthly Income:** {currency.split()[1]} {monthly_income:,.2f}")
        st.write(f"• **Total Expenses:** {currency.split()[1]} {(fixed_expenses + variable_expenses):,.2f}")
        st.write(f"• **Net Savings:** {currency.split()[1]} {net_savings:,.2f}")
        st.write(f"• **Total Assets:** {currency.split()[1]} {total_savings:,.2f}")
        st.write(f"• **High-Interest Debt:** {currency.split()[1]} {total_debt:,.2f}")
        st.markdown('</div>', unsafe_allow_html=True)

    with tab_strategy:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### Recommended Action Plan")
        if total_debt > 0:
            st.markdown("1. **Debt Avalanche Strategy:** Direct discretionary cash flow to clear high-interest liabilities first.")
        else:
            st.markdown("1. **Debt Free Status:** Maintain zero high-interest liabilities.")
        st.markdown(f"2. **Emergency Fund Target:** Maintain at least 3-6 months of fixed costs ({currency.split()[1]} {fixed_expenses * 3:,.2f} - {currency.split()[1]} {fixed_expenses * 6:,.2f}).")
        st.markdown(f"3. **Investment Allocation:** Deploy remaining surplus according to your **{risk_profile}** profile.")
        st.markdown('</div>', unsafe_allow_html=True)

    with tab_insights:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### Narrative Analysis")
        st.write(f"Targeting stated objectives: *'{goals if goals.strip() else 'General Wealth Building'}'*")
        st.info("FinWise AI engine completed the cash flow assessment.")
        st.markdown('</div>', unsafe_allow_html=True)