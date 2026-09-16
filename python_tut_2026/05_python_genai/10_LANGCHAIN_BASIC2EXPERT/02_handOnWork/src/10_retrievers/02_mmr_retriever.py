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

# See 09_embeddings_vectorstores/embeddings.py - text-embedding-004 is 404 on
# this account, so only gemini-embedding-001 / -2 / -2-preview are served.
EMBEDDING_MODEL = "models/gemini-embedding-001"

# --- OPENAI ALTERNATIVE (commented) -----------------------------------------
# OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"
# ----------------------------------------------------------------------------


def main():
    print_title("MMR RETRIEVER")

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
    # Swap the two lines to switch providers - nothing else changes, because both
    # classes implement the same Embeddings interface. Dimensions differ though
    # (Gemini 3072, OpenAI 1536), so an index built with one must be REBUILT,
    # never reused, with the other.
    #
    # embeddings = OpenAIEmbeddings(model=OPENAI_EMBEDDING_MODEL)
    # ------------------------------------------------------------------------

    vector_store = FAISS.from_documents(
        documents = chunks,
        embedding = embeddings,
    )

    # search_type="mmr" is the whole difference from vector_retriever.py.
    #   fetch_k  how many candidates to pull by pure similarity first
    #   k        how many of those to actually return, chosen for diversity
    # fetch_k MUST be larger than k, or there is nothing to choose between and
    # MMR degrades to plain similarity search.
    retriever = vector_store.as_retriever(
        search_type="mmr",
        search_kwargs= {
            "k": 2 ,
            "fetch_k":4
        }
    )

    query = "Explain artificial intelligence."
    print(f"Query: \n{query}")
    print_seperator()

    documents = retriever.invoke(query)

    for idx, doc in enumerate(documents, start=1):
        print(f"Retrieval Document {idx} \n")
        print(doc.page_content)
        print_seperator()


if __name__ == "__main__":
    main()

# ======================================================================
#  Concept Summary
 
#  MMR (Maximal Marginal Relevance) trades a little relevance for diversity:
#  it fetches fetch_k candidates by similarity, then picks k that are close to
#  the query but far from EACH OTHER.

#  Plain similarity search has a failure mode this fixes. The top k results are
#  often near-duplicates - the same fact phrased three ways - because they are
#  all closest to the query for the same reason. That wastes the context window
#  and can leave out the one chunk holding the rest of the answer.

#  fetch_k must exceed k or there is nothing to select between. lambda_mult
#  (default 0.5) sets the balance: 1.0 is pure relevance, so MMR collapses back
#  to similarity search, and 0.0 is maximum diversity, which will happily
#  return something barely related to the query.

# ======================================================================
