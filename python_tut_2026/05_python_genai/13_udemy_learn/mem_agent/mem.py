from mem0 import Memory
import os

OPEN_AI_API_KEY = os.getenv("OPENAI_API_KEY")
config = {
    "version": "v1.1",
    "embeder":{
        "provider": "openai",
        "model": "text-embedding-3-small",
        "config": {
            "api_key": os.getenv("OPENAI_API_KEY"),
            "model": "text-embedding-3-small",
        }
    },
    "llm":{
        "provider": "openai",
        "model": "gpt-4o-mini",
        "config": {
            "api_key": os.getenv("OPENAI_API_KEY"),
            "model": "gpt-4o-mini",
        }
    },
    "vector_store":{
        "provider": "qdrant",
        "config": {
            "host": "localhost",
            "port": 6333,
            # "url": "http://localhost:6333",
            "api_key": os.getenv("QDRANT_API_KEY"),
        }
    }
}

mem_client = Memory.from_config(config)