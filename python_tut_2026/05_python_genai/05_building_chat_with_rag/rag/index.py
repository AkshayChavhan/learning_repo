"""Steps 1 and 2 of RAG: load a PDF, then split it into chunks.

    pip install -qU langchain-community pypdf
    python3 index.py
"""

import os

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

HERE = os.path.dirname(os.path.abspath(__file__))
SAMPLE_PDF = os.path.join(HERE, "sample.pdf")

CHUNK_SIZE = 1000       # characters in a chunk
CHUNK_OVERLAP = 200     # characters repeated from the end of the previous chunk


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


if __name__ == "__main__":
    pages = read_pdf()
    chunks = split_documents(pages)

    print(f"loaded {len(pages)} pages from {os.path.basename(SAMPLE_PDF)}")
    print(f"split into {len(chunks)} chunks "
          f"(size {CHUNK_SIZE}, overlap {CHUNK_OVERLAP})\n")

    sizes = [len(c.page_content) for c in chunks]
    print(f"chunk sizes: smallest {min(sizes)}, largest {max(sizes)}, "
          f"average {sum(sizes) // len(sizes)}")
    print(f"metadata:    {chunks[0].metadata}\n")

    print("--- first chunk ---")
    print(chunks[0].page_content[:300])
