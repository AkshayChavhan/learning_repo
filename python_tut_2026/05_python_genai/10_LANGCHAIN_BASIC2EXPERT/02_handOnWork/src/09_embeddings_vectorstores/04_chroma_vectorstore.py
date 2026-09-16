from pathlib import Path
import shutil
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import _bootstrap  # noqa: F401  re-launches under myenv/ if python3 is the wrong one

# Third-party imports go BELOW _bootstrap. Above it they run before the re-exec
# fires, so the wrong interpreter dies on the import instead of being switched.
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

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
    print_title("Chroma Vector Store")

    # Load and split the document
    file_path = PROJECT_ROOT / "data" / "input" / "sample.txt"
    loader = TextLoader(file_path=file_path , encoding="utf-8")
    documents = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size= 200 , chunk_overlap = 50)
    chunks = splitter.split_documents(documents)
    print(f"Chunk Created: {len(chunks)}")
    print_seperator()

    # Setup embedding model & Database Path
    embeddings = GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL)

    # --- OPENAI ALTERNATIVE (commented) -------------------------------------
    # Swap the two lines to switch providers - nothing else changes, because both
    # classes implement the same Embeddings interface. Dimensions differ though
    # (Gemini 3072, OpenAI 1536), so an index built with one must be REBUILT,
    # never reused, with the other.
    #
    # embeddings = OpenAIEmbeddings(model=OPENAI_EMBEDDING_MODEL)
    # ------------------------------------------------------------------------

    chroma_db_path = PROJECT_ROOT  / "data" / "chroma_db"

    # Wipe any previous index. Vectors from a different embedding model are not
    # comparable - reusing the directory after switching models gives silently
    # meaningless similarity scores rather than an error.
    if chroma_db_path.exists():
        shutil.rmtree(chroma_db_path)

    # Initialize & polulate vector store in one step
    print("Adding documents to Chroma ...")
    vector_store = Chroma.from_documents(
        documents = chunks ,
        embedding = embeddings,
        collection_name = "langchain_demo",
        persist_directory = str(chroma_db_path)
    )

    # Verify document count - count() with parentheses, or this prints the
    # bound method rather than the number.
    print(f"Document count in collection: {vector_store._collection.count()}")
    print_seperator()

    # Run similarity search
    query = "What is Generative AI ?"
    print(f"Query: {query}")
    print("Running similarity search...")

    results = vector_store.similarity_search(query = query , k=2)
    print(f"Retrieval {len(results)} document(s). \n")
    print_seperator()
    for idx , doc in enumerate(results , start=1):
        print(f"Result {idx}: \n {doc.page_content} \n")
        print_seperator()


if __name__ == "__main__":
    main()

# ======================================================================
#  Concept Summary
 
#  Chroma is a vector database that stores embeddings and finds the nearest ones
#  to a query. from_documents() embeds and indexes in a single call.

#  Passing persist_directory writes the index to disk so it survives the
#  process, which is the difference from an in-memory store - and the reason
#  this script wipes the directory first. An index is only valid for the
#  embedding model that built it; reusing one after switching models produces
#  meaningless scores rather than an error.

# ======================================================================
