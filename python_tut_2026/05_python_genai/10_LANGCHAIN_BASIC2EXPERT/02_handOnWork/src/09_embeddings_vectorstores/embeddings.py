from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import _bootstrap  # noqa: F401  re-launches under myenv/ if python3 is the wrong one

from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from utils.helpers import print_seperator , print_title

load_dotenv()

# Gemini rather than OpenAI: the OpenAI account returns
#   429 ... 'code': 'credit_balance_exhausted'
# Note the model id. text-embedding-004, which most tutorials name, is 404 on
# this account - only gemini-embedding-001 / -2 / -2-preview are available.
# Ask the API what it will serve you:
#   curl "https://generativelanguage.googleapis.com/v1beta/models?key=$GOOGLE_API_KEY"
EMBEDDING_MODEL = "models/gemini-embedding-001"

def main():
    print_title("Text Embeddings")
    embeddings = GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL)
    text = "LangChain makes it easy to build applications powered by LLM"
    vector = embeddings.embed_query(text)

    print(f"Input Text: {text}")
    print_seperator()

    print(f"First 10 vector values: {vector[:10]}")


if __name__ == "__main__":
    main()

# ======================================================================
#  Concept Summary
 
#  An embedding turns text into a list of numbers positioned so that texts with
#  similar MEANING sit close together in vector space.

#  That is what makes semantic search possible: closeness is computed between
#  vectors, not words, so a query can match a passage sharing none of its terms.
#  The model choice is not cosmetic - it fixes the dimension count (Gemini's
#  gemini-embedding-001 gives 3072, OpenAI's text-embedding-3-small 1536) and
#  vectors from different models are not comparable.

# ======================================================================