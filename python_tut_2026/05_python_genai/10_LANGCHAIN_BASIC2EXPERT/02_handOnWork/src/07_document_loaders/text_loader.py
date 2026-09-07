from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import _bootstrap  # noqa: F401  re-launches under myenv/ if python3 is the wrong one

from langchain_community.document_loaders import TextLoader
from utils.helpers import print_seperator , print_title

 
def main():
    print_title("Text Loader")
    file_path = PROJECT_ROOT /  "data"/ "input" /"sample.txt"

    loader = TextLoader(file_path)
    documents = loader.load()

    print(f"Total documents loaded: {len(documents)}")
    print_seperator()

    document = documents[0]

    print(f"Document Metadata: {document.metadata}")
    print_seperator()

    print(f"Document Content: {document.page_content}")

if __name__ == "__main__":
      main()

# ======================================================================
#  Concept Summary
 
#  TextLoader reads a single plain-text file into one Document.

#  It is the simplest loader and the baseline for the rest: every loader returns
#  the same Document shape - page_content plus a metadata dict - so whatever
#  comes next in the pipeline does not care where the text came from.

# ======================================================================