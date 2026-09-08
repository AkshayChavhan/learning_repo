from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import _bootstrap  # noqa: F401  re-launches under myenv/ if python3 is the wrong one

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

# ======================================================================
#  Concept Summary
 
#  The entry point for every LangChain app: build a chat model, call .invoke()
#  with a prompt, read the reply.

#  Read response.text, not response.content. .text is a langchain_core property
#  that returns a plain string for every provider, while .content can be a list
#  of content blocks (Gemini does this) and breaks string operations.
#  response.type tells you the message role - "ai" for a model reply.

# ======================================================================