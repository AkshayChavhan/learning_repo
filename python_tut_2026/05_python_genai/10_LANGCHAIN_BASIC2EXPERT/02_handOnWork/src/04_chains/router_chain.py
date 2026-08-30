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

def main():
    print_title("Router Chain")
    llm = get_llm()

    science_chain = (PromptTemplate.from_template("Explain the following science concept:\n\n{query}")
    | llm
    | StrOutputParser())

    coding_chain = (PromptTemplate.from_template("Answer the following programming question:\n\n{query}")
    | llm
    | StrOutputParser())

    general_chain = (PromptTemplate.from_template("Answer the following question:\n\n{query}")
    | llm
    | StrOutputParser())

    def route(info):
        query = info["query"].lower()

        if "physics" in query or "science" in query:
            print("Routing to: Science Chain\n")
            return science_chain
        
        elif "python" in query or "llm" in query or "rag" in query or "code" in query:
            print("Routing to: Coding Chain\n")
            return coding_chain
        
        else:
            print("Routing to: General Chain\n")
            return general_chain

    chain = RunnableLambda(route)

    query = "Give me top 3 best practices for python beginner"

    print(f"Query: {query}\n")

    response = chain.invoke({"query": query})
    print(f"Response: {response}")

if __name__ == "__main__":
    main()