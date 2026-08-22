from langchain_community.cache import InMemoryCache, SQLiteCache
from langchain_core.globals import set_llm_cache

def setup_cache(cache_type: str):
    if cache_type == "InMemoryCache":
        set_llm_cache(InMemoryCache())
    elif cache_type == "SQLiteCache":
        set_llm_cache(SQLiteCache(database_path="finwise_cache.db"))