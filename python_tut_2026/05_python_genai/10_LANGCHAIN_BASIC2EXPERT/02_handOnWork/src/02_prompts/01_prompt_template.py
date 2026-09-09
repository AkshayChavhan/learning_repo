from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import _bootstrap  # noqa: F401  re-launches under myenv/ if python3 is the wrong one

from langchain_core.prompts import PromptTemplate
from llm_client import get_llm
from utils.helpers import print_seperator, print_title

def main():
    print_title("PromptTemplate")
    llm = get_llm()

    prompt_template = PromptTemplate(
        template = """
        You are an expert {profession}.
        Explain the concept of {topic} in simple words.
        Keep the explaination under {word_limit} words.
        """,
        input_variables = ["profession","topic","word_limit"],
    )

    prompt = prompt_template.invoke(
        {
            "profession":"AI Engineer",
            "topic":"Vector Database",
            "word_limit":100
        }
    )

    print("Formatted Prompt:\n")
    print(prompt.text)

    print_seperator()
    response = llm.invoke(prompt)

    print("LLM Response:\n")
    print(response.text)

if __name__ == "__main__":
    main()

# ======================================================================
#  Concept Summary
 
#  PromptTemplate turns a prompt into a reusable function: write it once with
#  {placeholders}, then .invoke() with different values.

#  The braces belong to LangChain, NOT to Python - never prefix the template
#  with f. An f-string is interpolated at import time and raises NameError for
#  the variables it cannot see. Use PromptTemplate for plain-text completion and
#  ChatPromptTemplate when you need message roles.

# ======================================================================