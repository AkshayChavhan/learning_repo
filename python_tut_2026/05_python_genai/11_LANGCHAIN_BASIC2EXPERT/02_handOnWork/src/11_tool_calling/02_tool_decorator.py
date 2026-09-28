from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from langchain_core.tools import tool

from utils.helpers import print_seperator, print_title

@tool
def calculate_discount(price: float , discount: float) -> float:
    """
    Calculate the final price  after applying a discount .

    Args:
        price: Original  price of the product.
        discount: Discount percentage.
    """
    return price - ( price * discount / 100)

def main() -> None :
    """
    Demostrates creating a langchain tool using a decorator.
    """
    print_title("Tool Decorator")

    print(f"Tool Name: {calculate_discount.name}")
    print_seperator()
    print(f"Tool Description : {calculate_discount.description}")
    print_seperator()

    print(f"Tool Input Schema : {calculate_discount.args_schema.schema()}")
    print_seperator()

    price = 1000
    discount = 20
    print(f"Price : {price}/- | Discount : {discount}")

    print_seperator()
    result =calculate_discount.invoke(
        {
            "price": price,
            "discount": discount
        }
    )
    print(f"Final Price: {result}")

if __name__ == "__main__":
    main()

# ======================================================================
#  Concept Summary
 
#  @tool turns a plain function into a tool with no boilerplate. Everything
#  Tool() needed you to type in 01 is now read off the function itself: the
#  name from the function name, the description from the docstring, and the
#  input schema from the type hints. Get those three right and the tool is
#  right.

#  It builds a StructuredTool, not the legacy Tool, so the two typed arguments
#  are a real schema and you call it with a dict: invoke({"price": 1000,
#  "discount": 20}) -> 800.0. A bare string is a ValidationError. That schema is
#  exactly what a model will be shown in 04 to decide how to fill the call.

#  The docstring IS the description, so write it for the model. The Args:
#  block reaches the model only as text - per-argument descriptions do not
#  become field descriptions unless you use @tool(parse_docstring=True). And
#  .schema() on args_schema is the Pydantic v1 name and warns on v2; the
#  current call is .model_json_schema().

# ======================================================================
