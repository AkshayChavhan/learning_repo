from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import _bootstrap  # noqa: F401  re-launches under myenv/ if python3 is the wrong one

from langchain_text_splitters import MarkdownHeaderTextSplitter

from utils.helpers import print_seperator , print_title

def main():
    print_title("Markdown Header Text Splitter")
    file_path = PROJECT_ROOT / "data" / "input" / "langchain_notes.md"

    with open(file_path , "r"  , encoding="utf-8") as file:
        markdown_text = file.read()
    # headerS_to_split_on - plural. The singular spelling is not an optional
    # kwarg it can ignore, it is the one REQUIRED positional argument, so
    # getting it wrong raises TypeError before anything runs.
    spliter = MarkdownHeaderTextSplitter(
        headers_to_split_on =[
              ("#","Header 1" ),
              ("##","Header 2" ),
              ("###","Header 3" ),
        ]
    )
    
    documents = spliter.split_text(markdown_text)

    print(f"Chunk created : {len(documents)}")
    print_seperator()

    for index, doc in enumerate(documents, start=1):
        print(f"Chunk  -> {index}")
        print(f"\nMetadata : \n  {doc.metadata}")
        print(f"Characters: {len(doc.page_content)}")
        print_seperator()

if __name__ == "__main__":
    main()