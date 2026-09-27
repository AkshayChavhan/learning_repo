from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from langchain_core.tools import Tool

from utils.helpers import print_seperator, print_title


def get_mcu_weather( city: str) -> str:
    """
    Returns a simple weather report for a city.
    """

    if  city.lower() == "wakanda":
        return f"The weather in {city} is sunny with a temperature of 28 degree c."
    elif city.lower() == "sokovia":
        return f"The weather in {city} is cold with a temperature of 4 degree c."
    else:
        return f" The weather in {city} is pleasant with a temperature of 20 degree c." 

def main() -> None:
    """
    Demostrate creatiuon and invoking a basic langchain tool.
    """
    print_title("Basic Tool")
    weather_tool = Tool(
        name = "get_mcu_weather",
        func = get_mcu_weather,
        description = "Get the current weather information for a city."
    )

    print(f"Tool name: {weather_tool.name}")

    print_seperator()
    print(f"Tool description: {weather_tool.description}")
    print_seperator()

    city = "Wakanda"

    print(f"Input {city}")
    print_seperator()

    result = weather_tool.invoke(city)
    print(f"Tool Result: \n{result}")

if __name__ == "__main__":
    main()

# ======================================================================
#  Concept Summary
 
#  Tool() wraps an ordinary Python function so LangChain - and later a model -
#  can call it by name. Three parts: name (what it is called by), func (what
#  actually runs) and description (how a model decides WHEN to use it).

#  Nothing here involves an LLM. weather_tool.invoke("Wakanda") is you calling
#  the function through the Tool interface - a Tool is a Runnable like a prompt
#  or a retriever, which is what lets a model be handed it in 04_tool_binding.
#  The description is written for the model, not for people: it is the only
#  thing the model reads to choose this tool over another.

#  This legacy Tool class takes ONE string input, so func must accept a single
#  str. Anything with several typed arguments needs StructuredTool (03). The
#  MCU cities are a stand-in: a tool can wrap any callable - an API, a database
#  query, a calculation - as long as it returns something the model can read.

# ======================================================================
