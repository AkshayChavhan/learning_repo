from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from pydantic import BaseModel, Field
from langchain_core.tools import StructuredTool

from utils.helpers import print_seperator, print_title


class  CalculatorInput(BaseModel):
    """
    Input schema for the calculator tool.
    """

    a: float = Field(description="First Number.")
    b: float = Field(description="Second Number.")
    operation: str = Field(description="Mathematical operation: add, substract, multplipy or divide.")

def calculate(a: float , b: float, operation: str) -> float:
    """ Performs a mathematical operation on two numbers """
    if operation == "add":
        return a+b
    if operation == "substract":
        return a-b
    if operation == "multiply":
        return a*b
    if operation == "divide":
        if b == 0 :
            return ValueError("Cannot divided by zero.")
        return a/b
    raise ValueError("Invalid operation. Choose: Add , Substract , multiply or divide.")

def main() -> None:
    print_title("Structured Tool")

    calculator_tool = StructuredTool.from_function(
        func = calculate,
        name = "calculator",
        description="Performs a mathematical operation on two numbers",
        args_schema = CalculatorInput
    )

    print(f"Tool name: {calculator_tool.name}")
    print_seperator()
    print(f"Tool Description: {calculator_tool.description}")
    print_seperator()
    print(f"Input Schema: {calculator_tool.args_schema.model_json_schema()}")    
    print_seperator()

    result = calculator_tool.invoke(
        {
            "a": 20,
            "b": 5,
            "operation": "multiply"
        }
    )

    print(f"Calculation Result: \n {result}")


if __name__ == "__main__":
    main()

# ======================================================================
#  Concept Summary
 
#  StructuredTool.from_function() is the explicit form of what @tool did in
#  02, with one addition that matters: args_schema. Handing it a Pydantic
#  model gives every argument a real description and a validated type - and
#  those per-field descriptions DO reach the model, unlike the Args: block in
#  02, which arrived as plain text.

#  The schema is not decoration; it is enforced. invoke({"a": "twenty", ...})
#  is a ValidationError before calculate() ever runs, so the function can
#  trust its inputs. The schema is also the contract a model fills in when it
#  calls the tool (04) - so how precisely you describe a field is how
#  accurately the model will use it.

#  Two lessons this file shows by getting them wrong. Line 34 RETURNS a
#  ValueError instead of raising it, so divide-by-zero hands the model an
#  exception object as a normal result - always raise. And operation is a free
#  str: typing it Literal["add", "subtract", "multiply", "divide"] turns the
#  prose list (with its "multplipy" typo) into a real enum the model cannot
#  misspell.

# ======================================================================
