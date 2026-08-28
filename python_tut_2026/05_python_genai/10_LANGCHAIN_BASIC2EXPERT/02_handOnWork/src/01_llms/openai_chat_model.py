from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from llm_client import get_llm

def chat_with_model() -> None:

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
    print("AI RESPONSE: \n")
    print(response.text)
    print("-" * 80)

    print("-" * 80)
    print("AI RESPONSE TYPE: \n")
    print(response.type)
    print("-" * 80)

if(__name__ == "__main__"):
    chat_with_model()