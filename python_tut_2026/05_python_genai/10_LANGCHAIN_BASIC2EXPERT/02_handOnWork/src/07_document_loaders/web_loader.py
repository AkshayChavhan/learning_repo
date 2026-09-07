from pathlib import Path
import os
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import _bootstrap  # noqa: F401  re-launches under myenv/ if python3 is the wrong one

# WebBaseLoader reads USER_AGENT at IMPORT time, so this has to be set before
# the import below or it warns "USER_AGENT environment variable not set".
# Identifying your scraper is basic web etiquette - some sites block or
# rate-limit the default python-requests agent.
os.environ.setdefault("USER_AGENT", "langchain-tutorial/1.0 (learning-repo)")

from langchain_community.document_loaders import WebBaseLoader
from utils.helpers import print_seperator , print_title

def main():
    print_title("Web Loader")

    # /docs/introduction is a 404. WebBaseLoader does NOT raise on an error
    # status - it hands back a Document with an empty page_content, so a
    # dead link looks exactly like a successful load until you check.
    loader = WebBaseLoader(web_path=("https://docs.langchain.com/oss/python/langchain/overview",))
    documents = loader.load()

    if not documents or not documents[0].page_content.strip():
        raise SystemExit("Loaded 0 characters - check the URL is reachable.")

    print(f"Total documents loaded: {len(documents)}")
    print_seperator()

    document = documents[0]

    print(f"Document Metadata: {document.metadata}")
    print_seperator()

    print(f"Document Content (First 1000 Characters only):\n {document.page_content[:1000]}")




if __name__ == "__main__":
    main()