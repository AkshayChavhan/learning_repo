"""Agent as a tool - one agent calls another.

The user talks to the ORCHESTRATOR. When a question needs a specialist, the orchestrator
calls the specialist agent like a function (specialist.as_tool(...)), gets its final
answer back, and replies. The specialist runs its OWN loop with its OWN instructions.

Run:
    python agent_tool.py                                        # "Say 'Hello, how are you?' in Spanish."
    python agent_tool.py "Say 'Good morning' in French."
    python agent_tool.py "Say 'See you tomorrow' in Spanish and French."
    python agent_tool.py --trace                                # also print the tool calls that happened
"""
import os
import sys

from dotenv import load_dotenv
from agents import Agent, Runner

load_dotenv()


def make_model():
    """None -> SDK default (OpenAI). With LLM_PROVIDER=groq every agent gets this model."""
    if os.getenv("LLM_PROVIDER", "openai") != "groq":
        return None
    from openai import AsyncOpenAI
    from agents import OpenAIChatCompletionsModel, set_tracing_disabled

    set_tracing_disabled(True)
    groq = AsyncOpenAI(api_key=os.getenv("GROQ_API_KEY"), base_url="https://api.groq.com/openai/v1")
    return OpenAIChatCompletionsModel(model=os.getenv("GROQ_MODEL", "openai/gpt-oss-120b"), openai_client=groq)


MODEL = make_model()

# two specialists: plain agents, nothing special about them
spanish_agent = Agent(
    name="Spanish agent",
    instructions="You translate the user's message to Spanish. Reply with the translation only.",
    model=MODEL,
)

french_agent = Agent(
    name="French agent",
    instructions="You translate the user's message to French. Reply with the translation only.",
    model=MODEL,
)

# the orchestrator: the one the user talks to
orchestrator_agent = Agent(
    name="Orchestrator agent",
    instructions=(
        "You are a translation agent. You use the tools given to you to translate. "
        "If asked for multiple translations, call the relevant tools."
    ),
    tools=[
        spanish_agent.as_tool(                                   # agent -> tool
            tool_name="translate_to_spanish",                    # the name the LLM sees (like a function name)
            tool_description="Translate the user's message to Spanish",   # when to use it (like a docstring)
        ),
        french_agent.as_tool(
            tool_name="translate_to_french",
            tool_description="Translate the user's message to French",
        ),
    ],
    model=MODEL,
)


def show_trace(result):
    """What happened inside the run: which agent-tools were called, with what, and what came back."""
    print("\n--- trace ---")
    for item in result.new_items:
        if item.type == "tool_call_item":
            print(f"  call   {item.raw_item.name}({item.raw_item.arguments})")
        elif item.type == "tool_call_output_item":
            print(f"  output {item.output!r}")
        elif item.type == "message_output_item":
            print(f"  reply  by {item.agent.name}")


if __name__ == "__main__":
    question = " ".join(a for a in sys.argv[1:] if not a.startswith("--")) \
        or "Say 'Hello, how are you?' in Spanish."
    print(f"> {question}\n")
    result = Runner.run_sync(orchestrator_agent, question)
    print(result.final_output)
    if "--trace" in sys.argv:
        show_trace(result)
