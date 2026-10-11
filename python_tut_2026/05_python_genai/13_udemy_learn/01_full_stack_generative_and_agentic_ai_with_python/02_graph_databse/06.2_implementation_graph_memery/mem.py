"""Memory agent with BOTH vector (Qdrant) and graph (Neo4j) memory.

Run with THIS folder's venv, not the repo-root one:
    .venv/bin/python mem.py        (deps pinned in requirements.txt)

Why: mem0ai 2.0.0+ deleted graph support entirely - the "graph_store" block
below is silently ignored there and Neo4j never receives a single node.
This folder pins mem0ai==1.0.11, the last release where graph memory works.
"""
import json
import os

from dotenv import load_dotenv
from mem0 import Memory
from neo4j import GraphDatabase
from openai import OpenAI

load_dotenv()

# Flip this one variable to switch the chat LLM for EVERYTHING below -
# mem0's extraction LLM and the chat call both follow it. Can also be set
# per run without editing the file:  MEM0_PROVIDER=groq .venv/bin/python mem.py
PROVIDER = os.getenv("MEM0_PROVIDER", "gemini")  # "gemini", "openai" or "groq"

if PROVIDER == "gemini":
    API_KEY = os.getenv("GOOGLE_API_KEY")
    # gemini-2.0-flash was retired by Google (API now 404s with "no longer
    # available, use gemini-3.8-flash"). Override via GEMINI_CHAT_MODEL in .env.
    CHAT_MODEL = os.getenv("GEMINI_CHAT_MODEL", "gemini-3.8-flash")
    EMBED_PROVIDER, EMBED_KEY = "gemini", API_KEY
    EMBED_MODEL = "models/gemini-embedding-001"  # mem0's own default Gemini embedder
    EMBED_DIMS = 768                           # mem0's Gemini embedder outputs 768-d vectors
    # Google publishes an OpenAI-compatible endpoint, so the SAME OpenAI
    # client class and .chat.completions.create() call below works against
    # Gemini too - no second code path or response shape needed.
    client = OpenAI(
        api_key=API_KEY,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    )
elif PROVIDER == "groq":
    # Groq: fast open models on a free tier, an OpenAI-compatible endpoint,
    # and mem0 ships a native "groq" LLM provider with tool-calling (which
    # the graph extraction needs). Groq hosts NO embedding models though, so
    # embeddings stay on Gemini - those calls never failed, only chat did.
    API_KEY = os.getenv("GROQ_API_KEY")
    CHAT_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    EMBED_PROVIDER, EMBED_KEY = "gemini", os.getenv("GOOGLE_API_KEY")
    EMBED_MODEL = "models/gemini-embedding-001"
    EMBED_DIMS = 768
    client = OpenAI(api_key=API_KEY, base_url="https://api.groq.com/openai/v1")
else:
    API_KEY = os.getenv("OPENAI_API_KEY")
    CHAT_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    EMBED_PROVIDER, EMBED_KEY = "openai", API_KEY
    EMBED_MODEL = "text-embedding-3-small"
    EMBED_DIMS = 1536                          # text-embedding-3-small outputs 1536-d vectors
    client = OpenAI(api_key=API_KEY)


def neo4j_default_database() -> str:
    """Ask the server which database it serves by default.

    mem0 hands our connection to langchain's Neo4jGraph, which assumes the
    database is called "neo4j" unless told otherwise. Newer Aura instances
    name it after the instance id instead (e.g. "a26c4b8b"), and the first
    write then dies with Neo.ClientError.Database.DatabaseNotFound.
    """
    with GraphDatabase.driver(
        os.getenv("NEO_CONNECTION_URI"),
        auth=(os.getenv("NEO_USERNAME"), os.getenv("NEO_PASSWORD")),
    ) as driver, driver.session() as session:
        return session.run("CALL db.info() YIELD name RETURN name").single()["name"]


# Set NEO_DATABASE in .env to skip the lookup.
NEO_DATABASE = os.getenv("NEO_DATABASE") or neo4j_default_database()

config = {
    "version": "v1.1",
    # mem0 logs every add/update/delete to a SQLite file. The default
    # ~/.mem0/history.db is shared with the repo-root venv's mem0 2.x, whose
    # table schema differs - keep 1.x's log in its own file so neither
    # version trips over the other's columns.
    "history_db_path": os.path.expanduser("~/.mem0/history_mem0_v1.db"),
    # "embedder", not "embeder" - mem0 reads this key by that exact name;
    # the old typo meant your embedder settings were silently ignored.
    "embedder": {
        "provider": EMBED_PROVIDER,
        "model": EMBED_MODEL,
        "config": {
            "api_key": EMBED_KEY,
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
    "graph_store": {
        "provider": "neo4j",
        "config": {
            "url": os.getenv("NEO_CONNECTION_URI"),
            "username": os.getenv("NEO_USERNAME"),
            "password": os.getenv("NEO_PASSWORD"),
            "database": NEO_DATABASE,  # see neo4j_default_database() above
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
            # switching back and forth never collides. Keyed by the EMBEDDER,
            # not the chat LLM: groq + Gemini embeddings shares mem0_gemini
            # because the stored vectors are identical either way.
            "collection_name": f"mem0_{EMBED_PROVIDER}",
            # mem0 creates the Qdrant collection with this size and DEFAULTS TO
            # 1536 when it's omitted. Gemini embeds to 768, so leaving it out
            # produced "Vector dimension error: expected dim: 1536, got 768"
            # on the very first search. Always pin it to the embedder's size.
            "embedding_model_dims": EMBED_DIMS,
        },
    },
}

mem_client = Memory.from_config(config)

while True:
    user_query = input("> ")

    # mem0 1.x takes the scope as a kwarg. Passing it inside filters= raises
    # "At least one of 'user_id', 'agent_id', or 'run_id' must be provided."
    search_memory = mem_client.search(user_query, user_id="user_1")
    print(search_memory)

    memories = [
        f"ID: {mem.get('id')}\nMemory: {mem.get('memory')}"
        for mem in search_memory["results"]
    ]

    print("Found Memories:", memories)

    # Only present while graph_store is active: the entity -> relationship ->
    # entity triples mem0 pulled out of Neo4j for this query. This is the
    # part a pure vector store can never give you.
    relations = search_memory.get("relations", [])
    print("Found Relations:", relations)

    SYSTEM_PROMPT = f"""
    Here is the context about the user:
    {json.dumps(memories)}

    Known relationships between entities (source -> relationship -> destination):
    {json.dumps(relations)}
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

    print(mem_client.get_all(user_id="user_1"))
