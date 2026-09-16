from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import _bootstrap  # noqa: F401  re-launches under myenv/ if python3 is the wrong one

# Third-party imports go BELOW _bootstrap. Above it they run before the re-exec
# fires, so the wrong interpreter dies on the import instead of being switched.
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

# --- OPENAI ALTERNATIVE (commented) -----------------------------------------
# from langchain_openai import OpenAIEmbeddings
# ----------------------------------------------------------------------------

from utils.helpers import print_seperator , print_title

load_dotenv()

# Gemini is the ACTIVE provider: the OpenAI account returns
#   429 ... 'code': 'credit_balance_exhausted'
# text-embedding-004, which most tutorials name, is 404 on this account - only
# gemini-embedding-001 / -2 / -2-preview are served.
EMBEDDING_MODEL = "models/gemini-embedding-001"

# --- OPENAI ALTERNATIVE (commented) -----------------------------------------
# OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"
# ----------------------------------------------------------------------------


def main():
    print_title("Vector store retrieval")

    # TextLoader, not TextSplitter - loading and splitting are separate steps,
    # and a splitter has no .load().
    loader = TextLoader(PROJECT_ROOT / "data" / "input" / "sample.txt", encoding="utf-8")
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 200,
        chunk_overlap = 50,
    )
    chunks = splitter.split_documents(documents)
    print(f"Chunks indexed: {len(chunks)}")
    print_seperator()

    # ACTIVE: Gemini
    embeddings = GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL)

    # --- OPENAI ALTERNATIVE (commented) -------------------------------------
    # Swap the two lines to switch providers - nothing else in this file
    # changes, because both classes implement the same Embeddings interface.
    # Note the dimensions differ (Gemini 3072, OpenAI 1536), so any index built
    # with one model must be rebuilt, never reused, with the other.
    #
    # embeddings = OpenAIEmbeddings(model=OPENAI_EMBEDDING_MODEL)
    # ------------------------------------------------------------------------

    vector_store = FAISS.from_documents(
        documents = chunks,
        embedding = embeddings,
    )

    # as_retriever() wraps the store in the standard Retriever interface.
    # search_kwargs is a DICT - {"k": 2}, with a colon. {"k"=2} is a SyntaxError.
    retriever = vector_store.as_retriever(search_kwargs={"k": 2})

    query = "What are large language model ?"
    print(f"Query: {query}")
    print_seperator()

    # Retrievers use .invoke(), like every other Runnable. The older
    # .get_relevant_documents() still works but is deprecated.
    documents = retriever.invoke(query)

    for idx, doc in enumerate(documents, start=1):
        print(f"Retrieval Document {idx} \n")
        print(doc.page_content)
        print_seperator()

if __name__ == "__main__":
    main()

# ======================================================================
#  Concept Summary
 
#  as_retriever() wraps a vector store in the standard Retriever interface, so
#  it becomes a Runnable that takes a query string and returns Documents.

#  The difference from calling similarity_search() directly is composability,
#  not capability. A retriever is a chain component: it pipes into a prompt,
#  swaps for a different retrieval strategy (MMR, multi-query, compression)
#  without touching the surrounding code, and gives you .invoke/.batch/.stream.
#  That interface is what the rest of this module builds on.

#  search_kwargs={"k": 2} controls how many documents come back. There is no
#  relevance floor - the store returns k documents whenever it holds that many,
#  however poor the match, so judge relevance by score and never by presence in
#  the result list.

# ======================================================================
