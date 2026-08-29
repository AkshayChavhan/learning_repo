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
    print_title("Partial-Prompt-Template")
    llm = get_llm()

    prompt_template = PromptTemplate(
        template = """
        You are an expert {domain} trainer.

        Explain the concept of {topic}.

        Keep the explaination under {word_limit} words.
        """,
        input_variables = ["domain", "topic" ,"word_limit"]
    )

    partial_prompt = prompt_template.partial(domain="Generative AI")
    prompt = partial_prompt.invoke(
        {
            "topic":"Vector Embeddings",
            "word_limit": 200
        }
    )

    print("Formatted messages:\n")
    print(prompt.text)

    print_seperator()
     
    response = llm.invoke(prompt)

    print("LLM Responses:\n")
    print(response.text)

if __name__ == "__main__":
    main()