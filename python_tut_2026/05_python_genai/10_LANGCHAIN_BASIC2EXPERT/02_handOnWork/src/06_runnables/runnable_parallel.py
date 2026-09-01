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
    print_title("Runnable Parallel")
    llm = get_llm()

    summary_chain =(
        PromptTemplate.from_template("Summarize the following topic: {topic}")
        | llm 
        | StrOutputParser()
    )

    advantages_chain =(
        PromptTemplate.from_template("What are the advantages of {topic}?")
        | llm 
        | StrOutputParser()
    )

    applications_chain =(
        PromptTemplate.from_template("What are the applications of {topic}?")
        | llm 
        | StrOutputParser()
    )

    parallel_chain = RunnableParallel(
        summary=summary_chain, 
        advantages=advantages_chain, 
        applications=applications_chain
    )
    topic = "AI"
    result = parallel_chain.invoke({"topic": topic})
    print(result)
    print("--------------------------------")
    print(result["summary"])
    print("--------------------------------")
    print(result["advantages"])
    print("--------------------------------")
    print(result["applications"])
    print("--------------------------------")



if __name__ == "__main__":
    main()

# add some notes here
# RunnableParallel is a chain that runs a sequence of runnables in parallel.
# It is a chain that runs a sequence of runnables in parallel.

