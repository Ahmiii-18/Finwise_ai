"""
src/utils.py
------------
Safe JSON parsing and error-handling utilities.
"""
import json
import re

def parse_llm_json(raw_response: str) -> dict:
    """Safely extracts and parses JSON content from raw LLM string outputs."""
    clean_str = raw_response.strip()
    
    # Strip Markdown codeblock ticks if present
    if clean_str.startswith("```"):
        clean_str = re.sub(r"^```[a-zA-Z]*\n?", "", clean_str)
        clean_str = re.sub(r"\n?```$", "", clean_str)

    try:
        return json.loads(clean_str)
    except json.JSONDecodeError:
        # Fallback regex extraction for nested objects
        match = re.search(r"\{.*\}", clean_str, re.DOTALL)
        if match:
            return json.loads(match.group(0))
        raise ValueError("Failed to parse valid JSON from LLM response.")