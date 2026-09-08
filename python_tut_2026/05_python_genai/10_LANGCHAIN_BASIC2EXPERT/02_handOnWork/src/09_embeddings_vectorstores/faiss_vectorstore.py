from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import _bootstrap  # noqa: F401  re-launches under myenv/ if python3 is the wrong one

from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader

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

def main():
    print_title("FAISS Vector Store")
    file_path = PROJECT_ROOT / "data" / "input" / "sample.txt"
    loader = TextLoader(file_path)
    documents= loader.load()
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 200,
        chunk_overlap = 50
    )
    chunks = splitter.split_documents(documents)
    embeddings = GoogleGenerativeAIEmbeddings(model = EMBEDDING_MODEL)

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
    print(f"Documents indexed: { len(chunks)}")
    print_seperator()

    query = "What is Machine Learning?"

    result = vector_store.similarity_search(
        query, k = 2
    )

    print(f"Query: {query}")
    print_seperator()

    for index , doc in enumerate(result , start=1):
        print(f"Results --> {index} \n")
        print(doc.page_content)
        print_seperator()



if __name__ == "__main__":
    main()

# ======================================================================
#  Concept Summary
 
#  FAISS is an in-memory similarity-search library from Meta. Same from_documents
#  interface as Chroma, so the surrounding code is identical.

#  The difference is persistence: FAISS holds the index in RAM and disappears
#  when the process exits unless you call save_local() / load_local(), whereas
#  Chroma persists to a directory. FAISS is the faster choice for a large index
#  that fits in memory; Chroma is easier when you want durability and metadata
#  filtering for free.

# ======================================================================
