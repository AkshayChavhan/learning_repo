from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from langchain_ollama import ChatOllama
from utils.helpers import print_seperator, print_title


def main():
    print_title("Local LLM using Ollama")

    llm = ChatOllama(
        model="llama3.2",
        temperature = 0.7
    )

    prompt = """ 
    Explain 3 advantages of running LLs locally in exactly three concise bullet points
    """


    print("-" * 80)
    print("USER PROMPT: \n")
    print(prompt.strip())
    print("-" * 80)

    print("\nGenerating response ... \n")
    response = llm.invoke(prompt)

    print("-" * 80)
    print("Local Ollama RESPONSE: \n")
    print(response.content)
    print("-" * 80)

    print("-" * 80)
    print("Local Ollama RESPONSE TYPE: \n")
    print(response.type)
    print("-" * 80)

if(__name__ == "__main__"):
    main()