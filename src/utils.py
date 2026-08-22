import json

def parse_json_safely(raw_response: str) -> dict:
    try:
        clean_response = raw_response.strip()
        if clean_response.startswith("```json"):
            clean_response = clean_response[7:]
        if clean_response.endswith("```"):
            clean_response = clean_response[:-3]
        return json.loads(clean_response.strip())
    except Exception:
        return {
            "financial_summary": raw_response,
            "financial_health_score": 50,
            "spending_analysis": [],
            "risk_level": "UNKNOWN",
            "top_priorities": ["Review manual budget metrics"],
            "budget_recommendations": [],
            "savings_strategy": [],
            "next_month_action_plan": []
        }