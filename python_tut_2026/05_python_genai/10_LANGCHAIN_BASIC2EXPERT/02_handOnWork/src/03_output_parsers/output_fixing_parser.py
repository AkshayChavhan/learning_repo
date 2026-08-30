from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import _bootstrap  # noqa: F401  re-launches under myenv/ if python3 is the wrong one

from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser
from langchain_classic.output_parsers import OutputFixingParser  #pip install langchain-classic

from llm_client import get_llm
from utils.helpers import print_seperator, print_title

class Employee(BaseModel):
    name: str = Field(description="Employee's full name")
    department: str = Field(description="Department name")
    experience: int = Field(description="Years of Experience")
    skills: list[str] = Field(description="List of Technical Skills")


def main():
    print_title("Output fixing Parser")
    llm = get_llm()
    parser = PydanticOutputParser(pydantic_object=Employee)

    fixing_parser = OutputFixingParser.from_llm(
        parser = parser,
        llm = llm
    )

    malformed_output = """
    {
        "name": "Rahul Sharma",
        "department": "AI",
        "experience" : "5 years",
        "skills" : "Python, SQL , Langchain"
    }
    """

    print("Malformed LLM output: \n")
    print(malformed_output)

    print_seperator()

    parsed_response = fixing_parser.invoke(malformed_output)


    print("Fixed & Parsed Output: \n")
    print(parsed_response)
    print_seperator()

    print("Accessing Invidual Fields:\n")

    print(f"Name      : {parsed_response.name}")
    print(f"Department: {parsed_response.department}")
    print(f"Experience: {parsed_response.experience}")
    print(f"Skills    : {parsed_response.skills}")

if __name__ == "__main__":
    main()