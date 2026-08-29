from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import _bootstrap  # noqa: F401  re-launches under myenv/ if python3 is the wrong one

from llm_client import get_llm
from utils.helpers import print_seperator, print_title

def main():

    print_title("Anthropic Chat Model")

    llm = get_llm()
    prompt = """
    Explain what LangChain is in exactly three concise bullet points.
    """

    print("-" * 80)
    print("USER PROMPT: \n")
    print(prompt.strip())
    print("-" * 80)

    print("\nGenerating response ... \n")
    response = llm.invoke(prompt)

    print("-" * 80)
    print("Anthropic RESPONSE: \n")
    print(response.text)
    print("-" * 80)

    print("-" * 80)
    print("Anthropic RESPONSE TYPE: \n")
    print(response.type)
    print("-" * 80)

if(__name__ == "__main__"):
    main()