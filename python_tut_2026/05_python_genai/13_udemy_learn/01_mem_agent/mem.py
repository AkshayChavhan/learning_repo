import json
import os

from dotenv import load_dotenv
from mem0 import Memory
from openai import OpenAI

load_dotenv()

# Flip this one variable to switch providers for EVERYTHING below -
# the mem0 LLM/embedder and the chat call all follow it.
PROVIDER = "gemini"  # "gemini" or "openai"

if PROVIDER == "gemini":
    API_KEY = os.getenv("GOOGLE_API_KEY")
    CHAT_MODEL = "gemini-2.0-flash"            # mem0's own default Gemini model
    EMBED_MODEL = "models/gemini-embedding-001"  # mem0's own default Gemini embedder
    # Google publishes an OpenAI-compatible endpoint, so the SAME OpenAI
    # client class and .chat.completions.create() call below works against
    # Gemini too - no second code path or response shape needed.
    client = OpenAI(
        api_key=API_KEY,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    )
else:
    API_KEY = os.getenv("OPENAI_API_KEY")
    CHAT_MODEL = "gpt-4o-mini"
    EMBED_MODEL = "text-embedding-3-small"
    client = OpenAI(api_key=API_KEY)

config = {
    "version": "v1.1",
    # "embedder", not "embeder" - mem0 reads this key by that exact name;
    # the old typo meant your embedder settings were silently ignored.
    "embedder": {
        "provider": PROVIDER,
        "model": EMBED_MODEL,
        "config": {
            "api_key": API_KEY,
            "model": EMBED_MODEL,
        },
    },
    "llm": {
        "provider": PROVIDER,
        "model": CHAT_MODEL,
        "config": {
            "api_key": API_KEY,
            "model": CHAT_MODEL,
        },
    },
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "host": "localhost",
            "port": 6333,
            # "url": "http://localhost:6333",
            "api_key": os.getenv("QDRANT_API_KEY"),
            # A collection's vector size is fixed when it's created. OpenAI
            # and Gemini embed to different dimensions, so sharing one
            # collection across providers breaks with a Qdrant 400 the
            # moment you switch ("Vector dimension error: expected dim: X,
            # got Y"). One collection PER provider sidesteps that entirely -
            # each gets created fresh, sized for its own embedder, and
            # switching PROVIDER back and forth never collides.
            "collection_name": f"mem0_{PROVIDER}",
        },
    },
}

mem_client = Memory.from_config(config)

while True:
    user_query = input("> ")

    search_memory = mem_client.search(user_query, filters={"user_id": "user_1"})
    print(search_memory)

    memories = [
        f"ID: {mem.get('id')}\nMemory: {mem.get('memory')}"
        for mem in search_memory["results"]
    ]

    print("Found Memories:", memories)

    SYSTEM_PROMPT = f"""
    Here is the context about the user:
    {json.dumps(memories)}
    """

    response = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_query},
        ],
    )

    print("AI :-> ", response.choices[0].message.content)

    mem_client.add(
        user_id="user_1",
        messages=[
            {"role": "user", "content": user_query},
            {"role": "assistant", "content": response.choices[0].message.content},
        ],
    )

    print("Memory added successfully")

    print(mem_client.get_all(filters={"user_id": "user_1"}))
