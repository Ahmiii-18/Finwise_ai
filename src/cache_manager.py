"""
src/cache_manager.py
--------------------
Manages dynamic switching between InMemoryCache and SQLiteCache.
"""
try:
    from langchain_core.globals import set_llm_cache
except ImportError:
    from langchain.globals import set_llm_cache

from langchain_community.cache import InMemoryCache, SQLiteCache

def configure_cache(cache_type: str) -> str:
    """Configures global LangChain LLM cache."""
    if cache_type == "InMemoryCache":
        set_llm_cache(InMemoryCache())
        return "InMemoryCache Active (Fastest, volatile RAM)."
    elif cache_type == "SQLiteCache":
        set_llm_cache(SQLiteCache(database_path="finwise_cache.db"))
        return "SQLiteCache Active (Persistent disk database)."
    else:
        set_llm_cache(None)
        return "Caching Disabled."