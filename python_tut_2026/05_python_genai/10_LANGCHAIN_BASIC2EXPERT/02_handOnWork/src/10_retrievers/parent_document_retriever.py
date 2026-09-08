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
# Both live in langchain_classic, NOT langchain.retrievers - that path does not
# exist in LangChain 1.x and raises ModuleNotFoundError.
from langchain_classic.retrievers import ParentDocumentRetriever
from langchain_classic.storage import InMemoryStore

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
    print_title("Parent Document Retriever")

    loader = TextLoader(PROJECT_ROOT / "data" / "input" / "sample.txt", encoding="utf-8")
    documents = loader.load()

    parent_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1000,
        chunk_overlap = 100,
    )
    child_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 200,
        chunk_overlap = 50,
    )

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

    # FAISS needs at least one vector to size its index, but this retriever
    # must be given an EMPTY store - it writes both children and parents itself
    # via add_documents(). So: seed with one throwaway vector, then delete it.
    vector_store = FAISS.from_texts(
        texts = ["dummy"],
        embedding = embeddings,
    )
    vector_store.delete(list(vector_store.index_to_docstore_id.values()))

    store = InMemoryStore()

    retriever = ParentDocumentRetriever(
        vectorstore = vector_store,
        docstore= store,
        child_splitter= child_splitter,
        parent_splitter = parent_splitter,
    )
    retriever.add_documents(documents)

    query = "What are LLM models ?"
    print(f"Query: {query}")
    print_seperator()

    results = retriever.invoke(query)
    
    print(f"Retrieved Parent Documents: {len(results)}")
    print_seperator()

    for idx, doc in enumerate(results, start=1):
        print(f"Parent Document {idx} \n")
        print(doc.page_content)
        print_seperator()


if __name__ == "__main__":
    main()

# ======================================================================
#  Concept Summary
 
#  ParentDocumentRetriever indexes SMALL chunks for matching but returns the
#  LARGE parent they came from. Two splitters, two stores: children go to the
#  vector store, parents to a separate docstore, linked by id.

#  It resolves the chunk-size tension. Small chunks embed precisely - a short
#  passage about one thing gives a clean vector - but are too fragmentary to
#  answer from. Large chunks carry context but embed vaguely, because averaging
#  many topics into one vector matches everything and nothing. This gets both:
#  match small, return large.

#  Construct it with an EMPTY vector store and call add_documents() on the
#  RETRIEVER, not from_documents() on the store - it has to write children and
#  parents to two places and link them. Note the docstore here is InMemoryStore,
#  so the parents vanish when the process exits; persisting them needs a real
#  store even if the vectors are on disk.

# ======================================================================
