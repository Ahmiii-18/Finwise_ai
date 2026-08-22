"""
src/chains.py
-------------
LLM connection, chain builders using LCEL, System/Human/AI message demonstrations, and streaming.
"""
import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from src.prompts import FINANCIAL_CHAT_PROMPT, NARRATIVE_CHAT_TEMPLATE

def build_llm(model_name: str = "gpt-4o-mini", temperature: float = 0.2, streaming: bool = False) -> ChatOpenAI:
    """Instantiate ChatOpenAI provider."""
    return ChatOpenAI(
        model=model_name,
        temperature=temperature,
        streaming=streaming,
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )

def build_financial_chain(llm):
    """
    Builds reusable chain using LCEL syntax (prompt | llm) 
    replacing legacy LLMChain.
    """
    return FINANCIAL_CHAT_PROMPT | llm

def run_message_demo(llm, prompt_text: str) -> str:
    """Demonstrates SystemMessage, HumanMessage, and AIMessage interaction."""
    messages = [
        SystemMessage(content="You are FinWise AI, an educational assistant."),
        HumanMessage(content=prompt_text)
    ]
    ai_response = llm.invoke(messages)
    return ai_response.content if hasattr(ai_response, 'content') else str(ai_response)

def stream_recommendations(llm, inputs: dict):
    """Yields recommendation chunks for real-time typing effect via st.write_stream."""
    messages = NARRATIVE_CHAT_TEMPLATE.format_messages(**inputs)
    for chunk in llm.stream(messages):
        if chunk.content:
            yield chunk.content