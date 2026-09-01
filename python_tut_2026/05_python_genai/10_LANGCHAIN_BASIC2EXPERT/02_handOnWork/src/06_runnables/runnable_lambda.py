from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import _bootstrap  # noqa: F401  re-launches under myenv/ if python3 is the wrong one

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda

from llm_client import get_llm
from utils.helpers import print_seperator, print_title


def to_uppercase(text: str) -> str:
    return text.upper()

def count_words(text: str) -> int:
    return f"Total words: {len(text.split())}"

def main():
    print_title("Runnable Lambda")
    to_uppercase_lambda = RunnableLambda(to_uppercase)
    count_words_lambda = RunnableLambda(count_words)

    text = "hello world"
    print(f"Original text: {text}")
    
    llm = get_llm()
    result = to_uppercase_lambda.invoke(text)
    print(f"Uppercase text: {result}")
    print("--------------------------------")
    result = count_words_lambda.invoke(text)
    print(f"Total words: {result}")
    print("--------------------------------")

if __name__ == "__main__":
    main()