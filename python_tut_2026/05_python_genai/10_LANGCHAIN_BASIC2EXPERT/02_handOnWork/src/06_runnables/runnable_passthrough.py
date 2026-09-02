from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import _bootstrap  # noqa: F401  re-launches under myenv/ if python3 is the wrong one

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough , RunnableParallel

from llm_client import get_llm
from utils.helpers import print_title


def main():
    print_title("Runnable Passthrough")
    llm = get_llm()

    prompt = PromptTemplate.from_template("Explain in two sentences: {query}")
    answer_chain = prompt | llm | StrOutputParser()

    # Shape 1 - passthrough as a PLACEHOLDER.
    #
    # `RunnablePassthrough() | llm` does not work: passthrough hands the model
    # whatever it was given, untouched, and a chat model needs a PromptValue, a
    # str, or a list of messages - never a bare dict. Hence:
    #     ValueError: Invalid input type <class 'dict'>
    #
    # Put it inside a dict instead and it becomes "drop the raw input in here",
    # so the chain can be invoked with a plain string.
    chain = {"query": RunnablePassthrough()} | answer_chain
    print(chain.invoke("What is AI?"))
    print("--------------------------------")

    # Shape 2 - .assign() KEEPS the original keys and adds computed ones.
    #
    # This is the reason passthrough exists. Without it, `prompt | llm` returns
    # only the answer and the question is gone. assign() carries the input
    # forward alongside the new value - exactly what RAG needs when the question
    # has to survive next to the retrieved documents.
    chain_with_input = RunnablePassthrough.assign(answer=answer_chain)
    result = chain_with_input.invoke({"query": "What is AI?"})
    print(f"keys kept: {list(result)}")
    print(f"question : {result['query']}")
    print(f"answer   : {result['answer']}")
    print("--------------------------------")

if __name__ == "__main__":
    main()

# add some notes here
# RunnablePassthrough forwards its input unchanged.
# Use it as a dict value to feed the raw input into a prompt variable,
# or RunnablePassthrough.assign(...) to add keys while keeping the originals.
