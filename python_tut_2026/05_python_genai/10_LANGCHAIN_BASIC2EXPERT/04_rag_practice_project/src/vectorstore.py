from operator import index
import os
import shutil
from pathlib import Path

from langchain_community.document_loaders.generic import DEFAULT
from langchain_core import vectorstores

from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStoreRetriever

from src.embeddings import get_embedding_model
from src.loaders import load_documents , split_documents


load_dotenv()

DEFAULT_VECTORSTORE_DIR = Path("data/vectorstore")
DEFAULT_DOCUMENTS_DIR = Path("data/documents")
INDEX_NAME = "index"

def vectorstore_exists(persistent_directory: str | Path = DEFAULT_VECTORSTORE_DIR) -> bool:
    folder  =  Path(persistent_directory)

    return (folder / f"{INDEX_NAME}.faiss").exists() and (folder / f"{INDEX_NAME}.pkl").exists()

def build_vectorstore(
    documents_dir: str | Path = DEFAULT_DOCUMENTS_DIR,
    persist_directory: str | Path = DEFAULT_VECTORSTORE_DIR,
    chunk_size : int | None = None,
    chunk_overlap : int | None = None,
) -> tuple[FAISS , int , int]:
    selected_chunk_size = chunk_size or int(os.getenv("CHUNK_SIZE", 1000))
    selected_chunk_overlap = chunk_overlap or int(os.getenv("CHUNK_OVERLAP", 1000))

    # 1. load raw documents from disk
    documents = load_documents(str(documents_dir))
    num_files = len({doc.metadata.get("filename") for doc in documents})

    #  2. Split into chunks before embeddings
    chunks = split_documents(
         documents,
         chunk_size = selected_chunk_size , 
         chunk_overlap = selected_chunk_overlap,
    )

    try:
        # 3. Create embeddings and store them in FAISS
        embeddings = get_embedding_model()
        vectorstore = FAISS.from_documents(chunks,embeddings)
    except Exception as e:
        raise RuntimeError(
            "Failed to create embeddings or build the FAISS index"
        ) from e

    persist_path = Path(persist_directory)
    persist_path.mkdir(parents = True  , exist_ok = True)
    vectorstore.save_local(str(persist_path), index_name = INDEX_NAME)

    return vectorstore , num_files  , len(chunks)

def load_vectorstore(
    persist_directorty : str | Path = DEFAULT_VECTORSTORE_DIR,
    ) -> FAISS :
    if not vectorstore_exists(persist_directorty):
        raise FileNotFoundError("No knowledge base found. Please build the knoledge base  first.")

    try:
        embeddings   = get_embedding_model()

        vectorstores = FAISS.load_local(
            str(persist_directorty),
            embeddings ,
            index_name = INDEX_NAME,
            allow_dangerous_deserialization=True
        )
    
    except FileNotFoundError:
        raise
    
    except Exception as e:
        raise RuntimeError(
            "Failed to load the FAISS knowledge base."
            "Try rebuilding the knowledge base."
        ) from e
    
    return vectorstores

def rebuild_vectorstore(
    documents_dir :str | Path = DEFAULT_DOCUMENTS_DIR,
    persist_directory: str| Path = DEFAULT_VECTORSTORE_DIR,
):
    clear_vectorstore(persist_directory)
    return build_vectorstore(documents_dir , persist_directory)

def clear_vectorstore(persist_directory: str| Path = DEFAULT_VECTORSTORE_DIR):
    folder = Path(persist_directory)
    if folder.exists():
        shutil.rmtree(folder)
    folder.mkdir(parents = True , exist_ok=True)

def get_retriever(
    vectorstore: FAISS,
    k: int | None = None,
):
    top_k = k or int(os.getenv("TOP_K" , "4"))
    return vectorstore .as_retriever(search_kwargs = { "k" : top_k})

def  get_chunk_count(persist_directory: str| Path = DEFAULT_VECTORSTORE_DIR) -> int :
    if not vectorstore_exists(persist_directory):
        return 0
    
    try:
        vectorstore = load_vectorstore(persist_directory)
        return int(vectorstore.index.ntotal)
    except Exception:
        return 0
    
def format_docs(docs: list[Document]) -> str:
    if not docs:
        return "No relevant context  was retrieved."

    parts = []

    for i,  doc in enumerate(docs, start =1):
        filename = doc.metadata.get("filename") or doc.metadata.get("source", "unknown")
        page = doc.metadata.get("page")
        location = f"{filename}"
        if page is not None:
            location = f"{filename} ( page {page})"
        parts.append(f"[Source {i}: {location}] \n {doc.page_content}")

    return "\n\n".join(parts)
