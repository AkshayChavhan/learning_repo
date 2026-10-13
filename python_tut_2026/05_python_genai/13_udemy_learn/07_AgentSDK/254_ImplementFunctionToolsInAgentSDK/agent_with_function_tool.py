"""Function tools - your own Python function as a tool.

Three steps:  (1) from agents import function_tool
              (2) @function_tool on a normal, typed function WITH a docstring
              (3) tools=[get_weather]   <- the function itself, no parentheses

Run:
    python agent_with_function_tool.py                        # "What is the weather in Patiala?"
    python agent_with_function_tool.py "weather in Mumbai?"   # your own question
    python agent_with_function_tool.py --show-schema          # what the decorator built from the function
    python agent_with_function_tool.py --no-tool              # same question, no tool -> "go check an app"
"""
import json
import os
import sys

import requests
from dotenv import load_dotenv
from agents import Agent, Runner, WebSearchTool, function_tool

load_dotenv()


@function_tool                                     # (1)+(2) makes it a tool
def get_weather(city: str) -> str:
    """Fetch the current weather for the given city.

    Args:
        city: The city name to fetch the weather for.
    """
    # Everything above this line is READ BY THE LLM: name, first docstring line (description),
    # Args (parameter descriptions), type hints (parameter types). Everything below is yours.
    print(f"   [tool] get_weather(city={city!r}) <- your Python is running")
    url = f"https://wttr.in/{city}?format=%C+%t"
    response = requests.get(url, timeout=10)
    if response.status_code == 200:
        return f"The weather in {city} is {response.text.strip()}."
    return "Something went wrong"


USE_TOOL = "--no-tool" not in sys.argv
QUESTION = " ".join(a for a in sys.argv[1:] if not a.startswith("--")) or "What is the weather in Patiala?"
INSTRUCTIONS = "You greet the user and answer using emojis, in a funny way."


def build_agent() -> Agent:
    if os.getenv("LLM_PROVIDER", "openai") != "groq":
        # ---- the lecture's code: hosted tool + function tool in ONE list ----------
        return Agent(
            name="Hello World Agent",
            instructions=INSTRUCTIONS,
            tools=[WebSearchTool(), get_weather] if USE_TOOL else [],   # (3) no () on get_weather!
        )

    # ---- Groq path: function tools work anywhere (they run on YOUR machine) ---------
    # Hosted WebSearchTool is OpenAI-only, so this is the note's section 5 as-is:
    # "WebSearchTool removed - still 27°C: the answer came from YOUR function".
    from openai import AsyncOpenAI
    from agents import OpenAIChatCompletionsModel, set_tracing_disabled

    set_tracing_disabled(True)
    groq = AsyncOpenAI(api_key=os.getenv("GROQ_API_KEY"), base_url="https://api.groq.com/openai/v1")
    return Agent(
        name="Hello World Agent",
        instructions=INSTRUCTIONS,
        tools=[get_weather] if USE_TOOL else [],
        model=OpenAIChatCompletionsModel(model=os.getenv("GROQ_MODEL", "openai/gpt-oss-120b"), openai_client=groq),
    )


if __name__ == "__main__":
    if "--show-schema" in sys.argv:
        # get_weather is no longer a plain function - the decorator returned a FunctionTool.
        print("tool name   :", get_weather.name)
        print("description :", get_weather.description)
        print("parameters  :", json.dumps(get_weather.params_json_schema, indent=2))
        sys.exit(0)

    agent = build_agent()
    print(f"[{os.getenv('LLM_PROVIDER', 'openai')} | tools: {[t.name if hasattr(t, 'name') else type(t).__name__ for t in agent.tools] or 'none'}]")
    print(f"> {QUESTION}\n")
    result = Runner.run_sync(agent, QUESTION)
    print("\n" + result.final_output)
