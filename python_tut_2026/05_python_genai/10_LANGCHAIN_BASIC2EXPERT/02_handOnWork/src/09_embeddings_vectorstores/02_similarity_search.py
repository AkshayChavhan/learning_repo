from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import _bootstrap  # noqa: F401  re-launches under myenv/ if python3 is the wrong one

from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# --- OPENAI ALTERNATIVE (commented) -----------------------------------------
# from langchain_openai import OpenAIEmbeddings
# ----------------------------------------------------------------------------

from utils.helpers import print_seperator , print_title

load_dotenv()

# See embeddings.py - text-embedding-004 is 404 on this account.
EMBEDDING_MODEL = "models/gemini-embedding-001"

# --- OPENAI ALTERNATIVE (commented) -----------------------------------------
# OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"
# ----------------------------------------------------------------------------

# Documents written by hand instead of loaded + split. Loading a file is the
# previous topic; here the point is only the search, so a short list keeps the
# right answer obvious - you can see which document SHOULD win before running.
DOCUMENTS = [
    Document(
        page_content="Python is a high-level programming language known for readable syntax.",
        metadata={"topic": "programming"},
    ),
    Document(
        page_content="Machine learning lets systems improve from data instead of hand-written rules.",
        metadata={"topic": "ai"},
    ),
    Document(
        page_content="A vector store saves embeddings and finds the nearest ones to a query.",
        metadata={"topic": "ai"},
    ),
    Document(
        page_content="Espresso is brewed by forcing hot water through finely ground coffee.",
        metadata={"topic": "coffee"},
    ),
]


def main():
    print_title("Similarity Search")

    embeddings = GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL)

    # --- OPENAI ALTERNATIVE (commented) -------------------------------------
    # Swap the two lines to switch providers - nothing else changes, because both
    # classes implement the same Embeddings interface. Dimensions differ though
    # (Gemini 3072, OpenAI 1536), so an index built with one must be REBUILT,
    # never reused, with the other.
    #
    # embeddings = OpenAIEmbeddings(model=OPENAI_EMBEDDING_MODEL)
    # ------------------------------------------------------------------------

    vector_store = FAISS.from_documents(documents=DOCUMENTS, embedding=embeddings)
    print(f"Documents indexed: {len(DOCUMENTS)}")
    print_seperator()

    # The query shares no keyword with the document that should win - no
    # "vector", no "embedding". Keyword search would return nothing; similarity
    # search matches on meaning, which is the whole point.
    query = "How do I store and look up text by meaning?"
    print(f"Query: {query}")
    print_seperator()

    # similarity_search returns the k nearest documents, best first.
    results = vector_store.similarity_search(query, k=2)
    for index, doc in enumerate(results, start=1):
        print(f"Result {index} [{doc.metadata['topic']}]")
        print(doc.page_content)
        print()
    print_seperator()

    # Same search, but with the raw distance attached. Worth seeing at least
    # once: it tells you HOW close a match is, so you can drop weak hits.
    print("With scores (FAISS returns L2 distance - LOWER is closer):")
    print()
    scored = vector_store.similarity_search_with_score(query, k=2)
    for index, (doc, score) in enumerate(scored, start=1):
        print(f"Result {index} | distance {score:.4f}")
        print(doc.page_content)
        print()
    print_seperator()


if __name__ == "__main__":
    main()


# ======================================================================
#  Concept Summary
 
#  similarity_search(query, k) embeds the query with the SAME model used to
#  index the documents, then returns the k documents whose vectors sit closest
#  to it - ranked best first.

#  It matches meaning, not words: a query with zero overlapping keywords still
#  finds the right document.

#  similarity_search_with_score returns (document, score) pairs. The number is
#  store-specific - FAISS gives L2 distance where LOWER is better, while Chroma
#  and others may return a similarity where HIGHER is better. Check which one
#  you have before filtering on a threshold, or you will keep the worst matches.

#  k has no "correct" answer and no safety net: the store always returns k
#  documents if it holds that many, however irrelevant they are. Relevance is
#  judged by the score, never by being in the result list.

# ======================================================================
