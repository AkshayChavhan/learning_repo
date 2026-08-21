"""Ask questions about the PDF that index.py stored in Qdrant.

Setup, once:

    python3 -m venv venv
    source venv/bin/activate
    pip install -qU langchain-community pypdf langchain-openai langchain-qdrant

Pin what you installed, so the setup is repeatable:

    pip freeze > requirements.txt       # run this INSIDE the venv
    pip install -r requirements.txt     # rebuild it later

Run `freeze` inside the venv. Outside it, you capture every package on the
machine - dbus-python, python-apt and all.

Start the vector database and set your key:

    docker compose -f docker-composer.yml up -d
    export OPENAI_API_KEY="sk-..."

Run it:

    python3 index.py                                 # once, to fill the collection
    python3 02_chat.py "what problem does RAG solve?"

Retrieve the closest chunks, put them in a system prompt, let the model
answer from them.
"""

import os
import sys

from langchain_openai import ChatOpenAI
from langchain_qdrant import QdrantVectorStore

from index import COLLECTION, QDRANT_URL, get_embeddings

TOP_K = 4
CHAT_MODEL = "gpt-4o-mini"

# The system prompt is where RAG is won or lost. Without the "only" rule the
# model happily blends the document with what it half-remembers from training,
# and you cannot tell which sentence came from where.
SYSTEM_PROMPT = """You answer questions about one specific document.

Rules:
- Use ONLY the context below. Treat it as everything you know.
- If the context does not answer the question, say exactly:
  "That is not in the document." Do not fall back on general knowledge.
- Cite the page for every fact, like [page 3].
- Be brief. Two or three sentences unless more is genuinely needed.

Context:
{context}"""


def get_store(url=QDRANT_URL, collection=COLLECTION):
    """Connect to the collection index.py already filled.

    This only reads. It does not re-embed the PDF or re-upload anything,
    so it is cheap and instant - unlike index.py, which pays OpenAI to
    embed every chunk.

    Raises if the collection does not exist yet. Run index.py first.
    """
    return QdrantVectorStore.from_existing_collection(
        collection_name=collection,
        embedding=get_embeddings(),
        url=url,
    )


def search(question, k=TOP_K, store=None):
    """Return the k chunks closest in meaning to the question.

    The question is embedded with the same model the chunks were, then
    Qdrant finds the nearest vectors. Matching is by meaning, not keywords -
    "can I get my money back" finds a chunk about the refund policy even
    with no word in common.

    Pass an existing `store` to avoid reconnecting on every question.
    """
    store = store or get_store()
    return store.similarity_search(question, k=k)


def build_context(chunks):
    """Join retrieved chunks into one block of text, labelled by page.

    This is the "Augment" in Retrieval Augmented Generation - the text you
    drop into the system prompt so the model answers from your document
    instead of from whatever it memorised during training.
    """
    parts = []
    for chunk in chunks:
        text = " ".join(chunk.page_content.split())
        parts.append(f"[page {chunk.metadata.get('page')}]\n{text}")
    return "\n\n".join(parts)


def build_messages(question, chunks):
    """Build the two messages sent to the model.

    system -> the rules plus the retrieved context
    user   -> the question, on its own

    Keeping the context in the system message and the question in the user
    message is what stops the model treating your document as a request.
    Text inside the context is data to be read, never instructions to follow.
    """
    return [
        {"role": "system", "content": SYSTEM_PROMPT.format(context=build_context(chunks))},
        {"role": "user", "content": question},
    ]


def answer(question, chunks, model=CHAT_MODEL):
    """Ask the model the question, given the chunks already retrieved.

    temperature=0 so the same question gives the same answer - you want a
    document lookup here, not creative writing.
    """
    llm = ChatOpenAI(model=model, temperature=0)
    return llm.invoke(build_messages(question, chunks)).content


if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        print("set OPENAI_API_KEY first - the question has to be embedded too")
        raise SystemExit(1)

    question = " ".join(sys.argv[1:]) or "What problem does RAG solve?"
    print(f"question: {question}\n")

    chunks = search(question)

    print(f"retrieved {len(chunks)} chunks from pages "
          f"{[c.metadata.get('page') for c in chunks]}\n")

    print("--- answer ---")
    print(answer(question, chunks))
