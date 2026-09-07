from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import _bootstrap  # noqa: F401  re-launches under myenv/ if python3 is the wrong one

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter

from utils.helpers import print_seperator , print_title

def main():
    print_title("Character Text Splitter")
    file_path = PROJECT_ROOT / "data" / "input" / "sample.txt"

    loader = TextLoader(file_path)
    documents = loader.load()

    print(f"Original Documents: {len(documents)}")
    print_seperator()

    splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size = 200,
        chunk_overlap = 50
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