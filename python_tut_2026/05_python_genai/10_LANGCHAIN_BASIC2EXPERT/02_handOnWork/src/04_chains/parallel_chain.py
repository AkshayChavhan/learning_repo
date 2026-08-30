from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import _bootstrap  # noqa: F401  re-launches under myenv/ if python3 is the wrong one

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel
from llm_client import get_llm
from utils.helpers import print_seperator, print_title

def main():
    print_title("Parallel Chain")
    llm = get_llm()

    summary_prompt = PromptTemplate.from_template(
        "Write a short summary about {topic}"
    )

    advantages_prompt = PromptTemplate.from_template(
        "Write a short summary about {topic}"
    )

    applications_prompt = PromptTemplate.from_template(
        "Write a short summary about {topic}"
    )

    parallel_chain = RunnableParallel(
        summary = summary_prompt | llm | StrOutputParser(),
        advantages = advantages_prompt | llm | StrOutputParser(),
        applications = applications_prompt | llm | StrOutputParser(),
    )

    topic = "Retrieval Augumented Generation (RAG)"

    print(f"Topic: \n {topic}")
    print_seperator()

    result = parallel_chain.invoke({"topic": topic})

    print("Summary:\n")
    print(result["summary"])
    print_seperator()

    print("Advantages:\n")
    print(result["advantages"])
    print_seperator()

    print("Applications:\n")
    print(result["applications"])
    print_seperator()



if __name__ == "__main__":
    main()