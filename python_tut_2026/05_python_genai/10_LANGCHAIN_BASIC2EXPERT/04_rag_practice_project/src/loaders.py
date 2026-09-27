from pathlib import Path

from langchain_community.document_loaders import Docx2txtLoader, PyPDFLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

SUPPORTED_EXTENSIONS = { ".pdf" , ".docx"}

def load_documents(folder_path:str) -> list[Document]:
    folder = Path(folder_path)
    if not folder.exists():
        raise FileNotFoundError(f"Document folder not found : {folder_path}")

    files = [
        path 
        for path in sorted(folder.iterdir())
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS
    ]

    if not files:
        raise ValueError("No supported documents found. Please upload PDF or DOCX files.")

    documents: list[Document] = []

    for file_path in files:
        loaded = _load_single_document(file_path)
        documents.extend(loaded)

    documents = [doc for doc in documents if doc.page_content and doc.page_content.strip()]

    if not documents:
        raise ValueError("Documents were found but they appear to be empty or unreadable.")

    return documents

def _load_single_document( file_path : str) -> list[Document]:
    suffix = file_path.suffix.lower()

    try:
        if suffix == ".pdf":
            loader = PyPDFLoader(str(file_path))
            docs = loader.load()
        elif suffix == ".docx":
            loader = Docx2txtLoader(str(file_path))
            docs = loader.load()
        else:
            raise ValueError(f"Unsupported file type: {file_path.name}")
            
    except ValueError:
        raise
    except Exception as e:
        raise ValueError(f"Could not read '{file_path.name}'") from e
        
    for doc in docs:
        doc.metadata["source"] = file_path.name
        doc.metadata["filename"] = file_path.name
            
        if "page" in doc.metadata  and doc.metadata["page"] is not None:
            try:
                doc.metadata["page"] = int(doc.metadata["page"]) + 1
            except (TypeError , ValueError):
                doc.metadata["page"]  = None
        else:
            doc.metadata["page"] = None
    return docs

def split_documents(documents: list[Document] , chunk_size : int = 1000 ,  chunk_overlap:int = 150 ,):
    if not documents:
        raise ValueError("No documents to split")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = chunk_size ,
        chunk_overlap = chunk_overlap,
        length_function = len,
        separators = [ "\n\n" , "\n" , " " , ""]
    )

    chunks = text_splitter.split_documents(documents)

    if not chunks:
        raise ValueError("Document splitting produced no chunks.")

    return chunks
         
def count_source_files(folder_path) -> int:
    folder = Path(folder_path)
    if not folder.exists():
        return 0
            
    return sum(
        1
        for path in folder.iterdir()
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS
    )
