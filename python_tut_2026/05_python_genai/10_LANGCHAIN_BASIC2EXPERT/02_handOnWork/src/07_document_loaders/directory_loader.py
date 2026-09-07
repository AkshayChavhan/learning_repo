from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import _bootstrap  # noqa: F401  re-launches under myenv/ if python3 is the wrong one

from langchain_community.document_loaders import (
    DirectoryLoader,
    TextLoader
)

from utils.helpers import print_seperator , print_title

def main():
    print_title("Directory Loader")
    directory = PROJECT_ROOT / "data" / "input"
    loader = DirectoryLoader(
        path = directory,
        glob = "**/*.txt",
        loader_cls = TextLoader
    )
    
    documents = loader.load()

    print(f"Total FILES Loaded: {len(documents)}")

    print_seperator()

    for index, document in enumerate( documents , start=1):
        # `document`, not `documents` - the latter is the list, which has no
        # .metadata, so this raised AttributeError on the first iteration.
        print(f"Document {index}")
        print(f"Source: {Path(document.metadata['source']).name}")
        print(f"Characters: {len(document.page_content)}")
        print()
        print(document.page_content[:200])
        print_seperator()

if __name__ == "__main__":
    main()