from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import _bootstrap  # noqa: F401  re-launches under myenv/ if python3 is the wrong one

from llm_client import get_llm
from utils.helpers import print_seperator, print_title

def main():

    print_title("Google Gemini Chat Model")

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
    print("Gemini RESPONSE: \n")
    print(response.text)
    print("-" * 80)

    print("-" * 80)
    print("AI RESPONSE TYPE: \n")
    print(response.type)
    print("-" * 80)

if(__name__ == "__main__"):
    main()

# ======================================================================
#  Concept Summary
 
#  Same code as the OpenAI script with a different provider behind get_llm().

#  That is the point of LangChain's common interface: only the class, the key
#  and the model id change, and everything downstream - prompts, chains,
#  parsers - is untouched. Gemini is where .content returns content blocks
#  rather than a string, so .text matters most here.

# ======================================================================