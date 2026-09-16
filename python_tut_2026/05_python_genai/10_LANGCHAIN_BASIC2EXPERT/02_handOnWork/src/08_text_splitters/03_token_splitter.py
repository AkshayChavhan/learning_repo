from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import _bootstrap  # noqa: F401  re-launches under myenv/ if python3 is the wrong one

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import TokenTextSplitter

from utils.helpers import print_seperator , print_title

def main():
    print_title("Token Text Splitter")
    file_path = PROJECT_ROOT / "data" / "input" / "sample.txt"

    loader = TextLoader(file_path)
    documents = loader.load()

    print(f"Original Documents: {len(documents)}")
    print_seperator()

    splitter = TokenTextSplitter(
        chunk_size = 50,
        chunk_overlap = 10
    )
    chunks = splitter.split_documents(documents)
    print(f"Chunks created: {len(chunks)}")
    print_seperator()

    for index, chunk in enumerate(chunks, start=1):
        print(f"Chunk  -> {index}")
        print(f"Characters: {len(chunk.page_content)}")
        print()
        print(chunk.page_content)
        print_seperator()

if __name__ == "__main__":
    main()

# ======================================================================
#  Concept Summary
 
#  TokenTextSplitter creates chunks based on token count instead of character count.

#  Since LLMs have token-based context windows, token-aware chunking
#  often provides more consistent chunk sizes for RAG applications.
#  It is especially useful when working with models that have strict token limits

# ======================================================================