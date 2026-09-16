from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import _bootstrap  # noqa: F401  re-launches under myenv/ if python3 is the wrong one

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

from llm_client import get_llm
from utils.helpers import print_seperator, print_title


def main():
    print_title("JSON Output Parser")
    llm = get_llm()
    parser = JsonOutputParser()

    prompt = PromptTemplate(
        template= """
        Extract the following product information.
        -Product Name
        -RAM
        -Storage
        -Display Size
        -Price
        {format_instructions}

        Product Descrtiption:
        {product}
        """,
        input_variables=["product"],
        partial_variables={
            "format_instructions": parser.get_format_instructions()
        },
    )

    prompt_value = prompt.invoke(
        {
            "product": (
                "The Apple Macbook Air M4 comes with 16GB RAM,"
                "512GB SSD Storage, a 13.6-inch Liquid Retina display,"
                "and is priced at $1,199."
            )
        }
    )

    # The object itself, before .text unwraps it. prompt.invoke() returns a
    # PromptValue, not a string - the same input a chat model expects. .text
    # is just one view of it; .to_messages() is the other, and it is what the
    # model actually receives.
    print("Prompt Value Object: \n")
    print(f"  type     : {type(prompt_value).__name__}")
    print(f"  messages : {prompt_value.to_messages()}")
    print_seperator()

    print("Formatted Prompt \n")
    print(prompt_value.text)

    print_seperator()
    """JSON OUTPUT Parser."""

    print_title("JSON OUTPUT Parser Output")

    # llm.invoke() returns an AIMessage whose .text is still a JSON STRING.
    # JsonOutputParser is what turns that text into a real dict you can index.
    # Format instructions only tell the model what shape to emit - something
    # still has to parse the reply.
    response = llm.invoke(prompt_value)

    print("Raw LLM Response: \n")
    print(response.text)

    print_seperator()

    parsed_response = parser.invoke(response)

    # The parsed value itself. JsonOutputParser hands back a PLAIN PYTHON DICT
    # - one step up from 01's list, because keys carry meaning. Still no
    # schema though: the keys are whatever the model chose to emit, and
    # nothing validates the types. 03_pydantic_parser.py adds both.
    print("Parsed Object: \n")
    print(f"  type   : {type(parsed_response).__name__}")
    print(f"  keys   : {list(parsed_response)}")
    print(f"  value  : {parsed_response}")
    print_seperator()

    print("Parsed JSON: \n")
    print(parsed_response)

    print_seperator()

    print("Accessing Invidual Fields:\n")

    for key, value in parsed_response.items():
        print(f"{key} : {value}")

if __name__ == "__main__":
    main()

# ======================================================================
#  Concept Summary
 
#  JsonOutputParser turns the reply into a plain Python dict.

#  Lighter than the Pydantic parser: no schema, no validation, no type checking
#  - you get whatever keys the model chose to emit. Use it for exploration or
#  genuinely dynamic shapes, and Pydantic when the fields are known and wrong
#  ones should be caught.

# ======================================================================