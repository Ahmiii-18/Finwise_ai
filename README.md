# 💰 FinWise AI - Smart Personal Budget & Financial Analysis Assistant

# Streamlit Demo : [finwiseai-ai.streamlit.app](https://finwiseai-ai.streamlit.app/)

**FinWise AI** is an AI-powered personal financial assistant prototype built with **LangChain (LCEL)** and **Streamlit**. It combines deterministic Python-based financial calculations with OpenAI's LLM capabilities to deliver personalized, structured financial insights and streaming budgeting advice.

---

## ⚠️ Educational Use Only

This application is an educational prototype built for assignment evaluation. It does not provide guaranteed investment advice, execute financial transactions, or replace a certified financial planner.

---

## ⚙️ Architecture: Deterministic Python vs. AI Reasoning

To ensure maximum accuracy and reliability, the architecture clearly separates rule-based logic from generative AI:

1. **Deterministic Python Engine (`financial_calculator.py`)**:
   - Handles exact mathematical calculations (Total Expenses, Remaining Balance, Savings Ratio, Expense Ratio).
   - Computes a rule-based preliminary financial health score (0–100) using static heuristics.
   - Prevents AI hallucination on exact numbers and guards against divide-by-zero errors[cite: 12].

2. **LangChain Generative Engine (`chains.py` & `prompts.py`)**[cite: 12]:
   - Receives calculated metrics and itemized expenses dynamically[cite: 12].
   - Evaluates risk factors, categorical spending habits, and priority focus areas[cite: 12].
   - Returns structured JSON data for interactive dashboards and streams natural language coaching recommendations in real time[cite: 12].

---

## 🚀 Quickstart & Installation Guide

### 1. Repository Setup

git clone [https://github.com/your-username/finwise_ai.git](https://github.com/your-username/finwise_ai.git)
cd finwise_ai
Some new line of text
