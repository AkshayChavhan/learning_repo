from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import _bootstrap  # noqa: F401  re-launches under myenv/ if python3 is the wrong one

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence

from llm_client import get_llm
from utils.helpers import print_title


def main():
    print_title("Runnable Sequence")
    llm = get_llm()
    sequence = PromptTemplate.from_template("What is the capital of {country}?")
    chain = sequence | llm | StrOutputParser()
    print(chain.invoke({"country": "France"}))
    print("--------------------------------")

if __name__ == "__main__":
    main()

# ======================================================================
#  Concept Summary
 
#  RunnableSequence chains steps so each one's output feeds the next. The pipe
#  operator builds one: prompt | model | parser.

#  Everything in LangChain implements the Runnable interface, which is what
#  makes the pipe work at all and gives the whole chain .invoke, .batch and
#  .stream for free. Read it left to right - format, generate, parse.

# ======================================================================