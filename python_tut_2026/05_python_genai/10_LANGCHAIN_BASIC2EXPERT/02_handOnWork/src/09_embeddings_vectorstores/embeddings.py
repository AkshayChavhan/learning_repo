from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import _bootstrap  # noqa: F401  re-launches under myenv/ if python3 is the wrong one

from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings

from utils.helpers import print_seperator , print_title

load_dotenv()

def main():
    print_title("Text Embeddings")
    embeddings = OpenAIEmbeddings(model= "text-embedding-3-small")
    text = "LangChain makes it easy to build applications powered by LLM"
    vector = embeddings.embed_query(text)

    print(f"Input Text: {text}")
    print_seperator()

    print(f"First 10 vector values: {vector[:10]}")


if __name__ == "__main__":
    main()

