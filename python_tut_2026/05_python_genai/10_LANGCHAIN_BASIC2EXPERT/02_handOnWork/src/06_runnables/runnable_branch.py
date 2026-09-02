from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import _bootstrap  # noqa: F401  re-launches under myenv/ if python3 is the wrong one

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableBranch

from llm_client import get_llm
from utils.helpers import print_seperator, print_title


def main():
    print_title("Runnable Branch")
    llm = get_llm()

    # The prompts declare {query}, which is also the key the branch is invoked
    # with. They have to match - {topic} here would raise KeyError at invoke time.
    technical_chain = PromptTemplate.from_template("Explain the technical details of: {query}") | llm | StrOutputParser()
    non_technical_chain = PromptTemplate.from_template("Explain in simple, non-technical terms: {query}") | llm | StrOutputParser()

    # "non-technical" CONTAINS "technical" as a substring, so a plain
    # `"technical" in query` is True for BOTH queries and everything routes to
    # the technical chain - silently, with no error. Rule out the negative case
    # first. A word-boundary regex would be the sturdier fix.
    def is_technical(x):
        query = x["query"].lower()
        if "non-technical" in query:
            return False
        return any(keyword in query for keyword in ["technical", "engineer", "developer"])

    # RunnableBranch takes (condition, runnable) PAIRS, then one bare default
    # runnable at the end. The condition returns a bool, not a label - a lone
    # lambda returning "technical"/"non-technical" is not a branch at all, and
    # raises ValueError: RunnableBranch requires at least two branches.
    branch = RunnableBranch(
        (is_technical, technical_chain),
        non_technical_chain,
    )

    result = branch.invoke({"query": "What is the technical details of AI?"})
    print(f"Result: {result}")
    print("--------------------------------")
    result = branch.invoke({"query": "What is the non-technical details of AI?"})
    print(f"Result: {result}")
    print("--------------------------------")

if __name__ == "__main__":
    main()
