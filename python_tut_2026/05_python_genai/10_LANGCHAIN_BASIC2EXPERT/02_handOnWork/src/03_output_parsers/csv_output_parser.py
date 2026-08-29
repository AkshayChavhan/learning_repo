from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

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

    print("Parsed Output: \n")
    print("Rank , Language")

    for index, skill in enumerate(skills, start=1):
        print(f"{index} : {skill}")

if __name__ == "__main__":
    main()