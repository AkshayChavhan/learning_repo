from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Project imports go BELOW the sys.path block - above it, `llm_client` is not
# importable yet and the script dies with ModuleNotFoundError.
from langchain_core.tools import tool

from llm_client import get_llm
from utils.helpers import print_seperator, print_title


@tool
def multiply(a: int, b: int) -> int:
    """
    Multiply two numbers.
    """
    return a * b


@tool
def add(a: int, b: int) -> int:
    """
    Add two numbers.
    """
    return a + b


def main() -> None:
    """Demonstrates binding tools to an LLM."""
    print_title("Tool Binding")
    llm = get_llm()
    tools = [multiply, add]
    llm_with_tools = llm.bind_tools(tools)

    query = "What is 25 multiplied by 4"
    print(f"User's Query : {query}")
    print_seperator()

    result = llm_with_tools.invoke(query)

    # When the model decides to call a tool, .text is usually EMPTY - the
    # answer is in .tool_calls, not in the prose. That is expected, not a bug.
    print(f"Model's response : {result.text or '(no text - the model chose a tool instead)'}")
    print_seperator()

    if result.tool_calls:
        print("Tool calls :\n")

        # `tool_call` (singular) is the loop variable - each one is a dict
        # with name / args / id. Naming the loop variable `tool_calls` while
        # indexing `tool_call` was a TypeError waiting on the first iteration.
        for tool_call in result.tool_calls:
            print(f"Tool: {tool_call['name']}")
            print(f"Arguments: {tool_call['args']}")
            print(f"Call ID: {tool_call['id']}")
            print_seperator()
    else:
        print("No tool call was required by the model.")


if __name__ == "__main__":
    main()

# ======================================================================
#  Concept Summary
 
#  bind_tools() hands the model the schema of every tool - name, description,
#  typed arguments - so that instead of answering in prose it may answer with
#  a TOOL CALL. Nothing about the tools changed; the model was told they exist.

#  What comes back is an AIMessage whose .text is empty and whose .tool_calls
#  holds dicts of name / args / id - here {"name": "multiply", "args": {"a":
#  25, "b": 4}}. The model filled those args from the schema alone, which is
#  why the descriptions and types in 02 and 03 were never cosmetic.

#  Nothing was EXECUTED. The model decided; multiply(25, 4) never ran and the
#  model never saw 100. Running the call, wrapping the result in a ToolMessage
#  carrying the same id, and invoking the model again is the agent loop - the
#  next step, deliberately not taken here. Tool calling is also a provider
#  feature: a model that lacks it ignores bind_tools and answers in prose.

# ======================================================================
