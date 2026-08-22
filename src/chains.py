from langchain_openai import ChatOpenAI
from src.config import OPENAI_API_KEY
from src.prompts import CHAT_PROMPT_TEMPLATE, NARRATIVE_CHAT_TEMPLATE
from src.utils import parse_json_safely

def get_llm():
    return ChatOpenAI(
        model_name="gpt-4o-mini",
        temperature=0.2,
        openai_api_key=OPENAI_API_KEY
    )

def run_financial_chain(inputs: dict) -> dict:
    llm = get_llm()
    chain = CHAT_PROMPT_TEMPLATE | llm
    response = chain.invoke(inputs)
    return parse_json_safely(response.content)

def stream_recommendations(inputs: dict):
    llm = get_llm()
    messages = NARRATIVE_CHAT_TEMPLATE.format_messages(**inputs)
    for chunk in llm.stream(messages):
        if chunk.content:
            yield chunk.content