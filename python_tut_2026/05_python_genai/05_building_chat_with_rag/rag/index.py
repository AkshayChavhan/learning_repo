"""Indexing for RAG: load a PDF, split it, embed it, store it in Qdrant.

Setup, once:

    python3 -m venv venv
    source venv/bin/activate
    pip install -qU langchain-community pypdf langchain-openai langchain-qdrant

Pin what you installed, so the setup is repeatable:

    pip freeze > requirements.txt       # run this INSIDE the venv
    pip install -r requirements.txt     # rebuild it later

Run `freeze` inside the venv. Outside it, you capture every package on the
machine - dbus-python, python-apt and all.

Start the vector database:

    docker compose -f docker-composer.yml up -d

    Note the filename: docker-composer.yml, with an r. Docker does not look
    for that name on its own, so the -f flag is required here. (The
    langgraph folder's file is named docker-compose.yml and needs no flag.)

Put your key in .env next to this file:

    OPENAI_API_KEY=sk-...

    Or export it - an exported value takes precedence over the .env.
    Generate every .env in this repo at once with ../../../../scripts/setup_env.sh

Run it:

    python3 index.py
"""

import os

from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore

# Read .env into environment variables, so the key can live in a file next to
# this script instead of being exported by hand in every new shell. An export
# still wins if you set one - load_dotenv does not overwrite what is already
# in the environment.
load_dotenv()

HERE = os.path.dirname(os.path.abspath(__file__))
SAMPLE_PDF = os.path.join(HERE, "sample.pdf")

CHUNK_SIZE = 1000       # characters in a chunk
CHUNK_OVERLAP = 200     # characters repeated from the end of the previous chunk

EMBEDDING_MODEL = "text-embedding-3-small"   # 1536 numbers per chunk

QDRANT_URL = "http://localhost:6333"
COLLECTION = "rag_sample"


def read_pdf(path=SAMPLE_PDF):
    """Read a PDF and return one Document per page.

    Each Document has .page_content (the text) and .metadata
    (the source path and a 0-based page number).
    """
    loader = PyPDFLoader(path)
    return loader.load()


def split_documents(documents, chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP):
    """Split Documents into smaller, overlapping chunks.

    A page is too big to embed usefully - you want to retrieve the paragraph
    that answers the question, not the whole page around it.

    "Recursive" means it tries separators in order and only moves to the next
    when a piece is still too big:

        "\\n\\n"  paragraphs   <- try hardest to split here
        "\\n"    lines
        " "     words
        ""      raw characters, last resort

    So chunks break at natural boundaries instead of mid-word. The overlap
    repeats the tail of each chunk at the head of the next, so a sentence
    sitting on a boundary is still readable in at least one of them.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    return splitter.split_documents(documents)


def get_embeddings(model=EMBEDDING_MODEL):
    """Create the OpenAI embedding model.

    An embedding turns text into a list of numbers (a vector) that captures
    its meaning. Two chunks about the same thing end up close together, even
    when they share no words - which is how retrieval finds "refund policy"
    from a question phrased "can I get my money back".

    text-embedding-3-small returns 1536 numbers per chunk.

    Needs OPENAI_API_KEY in the environment:

        export OPENAI_API_KEY="sk-..."
    """
    return OpenAIEmbeddings(model=model)


def store_in_qdrant(chunks, embeddings, url=QDRANT_URL, collection=COLLECTION):
    """Embed the chunks and write them into Qdrant.

    Each chunk becomes one point in the collection: the vector, plus the
    text and metadata kept alongside it as payload. The collection is
    created on first run.

    Careful: running this twice inserts the chunks twice. Qdrant does not
    deduplicate. Pass force_recreate=True to wipe and start clean.
    """
    return QdrantVectorStore.from_documents(
        documents=chunks,
        embedding=embeddings,
        url=url,
        collection_name=collection,
    )


if __name__ == "__main__":
    pages = read_pdf()
    chunks = split_documents(pages)

    print(f"loaded {len(pages)} pages from {os.path.basename(SAMPLE_PDF)}")
    print(f"split into {len(chunks)} chunks "
          f"(size {CHUNK_SIZE}, overlap {CHUNK_OVERLAP})")

    sizes = [len(c.page_content) for c in chunks]
    print(f"chunk sizes: smallest {min(sizes)}, largest {max(sizes)}, "
          f"average {sum(sizes) // len(sizes)}")

    if not os.getenv("OPENAI_API_KEY"):
        print("\nset OPENAI_API_KEY to embed and store these chunks")
        raise SystemExit

    store = store_in_qdrant(chunks, get_embeddings())
    print(f"\nstored {len(chunks)} chunks in Qdrant collection {COLLECTION!r}")
    print(f"  browse them at {QDRANT_URL}/dashboard")

    question = "What problem does RAG solve?"
    print(f"\nsearch: {question!r}")
    for i, hit in enumerate(store.similarity_search(question, k=2), 1):
        text = " ".join(hit.page_content.split())
        print(f"  {i}. page {hit.metadata['page']} - {text[:90]}...")
