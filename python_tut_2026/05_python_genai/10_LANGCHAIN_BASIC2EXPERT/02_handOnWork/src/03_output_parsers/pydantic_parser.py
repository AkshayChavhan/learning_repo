from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import _bootstrap  # noqa: F401  re-launches under myenv/ if python3 is the wrong one

from pydantic import BaseModel, Field
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

from llm_client import get_llm
from utils.helpers import print_seperator, print_title


class Employee(BaseModel):
    name: str = Field(description="Employee's full name")
    department: str = Field(description="Department name")
    experience: int = Field(description="Years of Experience")
    skills: list[str] = Field(description="List of Technical Skills")

def main():
    print_title("Pydantic Output Parcer")
    llm = get_llm()
    parser = PydanticOutputParser(pydantic_object=Employee)

    prompt = PromptTemplate(
        template="""
        Extract the employee information.
        {format_instructions}
        Text:
        {employee_details}
        """,
        input_variables=["employee_details"],
        partial_variables={
            "format_instructions": parser.get_format_instructions()
        }, 
    )
    print(prompt)

    prompt_value = prompt.invoke(
        {
            "employee_details": (
                "Rahul Sharma works as a Data Scientist in the AI team."
                "He has 5 Years of Experience and is skilled in Python,"
                "Machine Learning ,SQL and LangChain."
            )
        }
    )

    print("Formatted Prompt \n")
    print(prompt_value.text)
    print_seperator()
    """Demostrates Pydantic Parser."""

    print_title("Pydantic Parser Output")

    # llm.invoke() alone returns an AIMessage whose .text is still a JSON
    # STRING - it has no .department / .experience / .skills. The parser is
    # what turns that text into a real Employee instance, so it has to run on
    # the reply, not just supply the format instructions above.
    llm_message = llm.invoke(prompt_value)
    parsed_response = parser.invoke(llm_message)

    print("Parsed Pydantic Object: \n")
    print(parsed_response)
    print(f"type: {type(parsed_response).__name__}")

    print_seperator()

    print("Accessing Invidual Fields:\n")

    print(f"Name      : {parsed_response.name}")
    print(f"Department: {parsed_response.department}")
    print(f"Experience: {parsed_response.experience}")
    print(f"Skills    : {parsed_response.skills}")



if __name__ == "__main__":
    main()