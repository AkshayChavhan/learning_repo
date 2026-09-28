from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import _bootstrap  # noqa: F401  re-launches under myenv/ if python3 is the wrong one

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import CommaSeparatedListOutputParser

from llm_client import get_llm
from utils.helpers import print_seperator, print_title


def main():
    print_title("CSV Output Parser")
    llm = get_llm()
    parser = CommaSeparatedListOutputParser()

    prompt = PromptTemplate(
        template= """
        List the top 10 programming skills needed in GenAi Developement career.

        {format_instructions}
        """,
        input_variables=[],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    prompt_value = prompt.invoke({})

    # The object itself, before .text unwraps it. prompt.invoke() returns a
    # PromptValue, not a string - the same input a chat model expects. .text
    # is just one view of it; .to_messages() is the other, and it is what the
    # model actually receives.
    print("Prompt Value Object: \n")
    print(f"  type     : {type(prompt_value).__name__}")
    print(f"  repr     : {prompt_value!r}")
    print(f"  messages : {prompt_value.to_messages()}")
    print_seperator()

    print("Formatted Prompt \n")
    print(prompt_value.text)

    print_seperator()
    """CSV Output Parser."""

    print_title("CSV Output Parser Output")

    # llm.invoke() returns an AIMessage whose .text is one comma-separated
    # LINE. CommaSeparatedListOutputParser splits it into a real Python list.
    # Format instructions only tell the model what shape to emit - something
    # still has to parse the reply.
    response = llm.invoke(prompt_value)

    print("Raw LLM Response: \n")
    print(response.text)

    print_seperator()

    skills = parser.invoke(response)

    # The parsed value itself, before any formatting. This parser hands back a
    # PLAIN PYTHON LIST - not a LangChain object, not a model instance. So it
    # has no attributes to explore: len(), indexing and slicing are all there
    # is. 03_pydantic_parser.py is where a parser returns a real object with
    # named fields you can reach with a dot.
    print("Parsed Object: \n")
    print(f"  type   : {type(skills).__name__}")
    print(f"  value  : {skills}")
    print(f"  length : {len(skills)}")
    print(f"  first  : {skills[0]!r}")
    print_seperator()

    print("Parsed Output: \n")
    print("Rank , Language")

    for index, skill in enumerate(skills, start=1):
        print(f"{index} : {skill}")

if __name__ == "__main__":
    main()

# ======================================================================
#  Concept Summary
 
#  CommaSeparatedListOutputParser splits a comma-separated reply into a real
#  Python list.

#  The smallest useful parser, and the clearest illustration that format
#  instructions and parsing are separate steps: the model returns ONE LINE of
#  text, and something still has to split it. Fragile by nature - an item
#  containing a comma cannot survive the round trip.

# ======================================================================