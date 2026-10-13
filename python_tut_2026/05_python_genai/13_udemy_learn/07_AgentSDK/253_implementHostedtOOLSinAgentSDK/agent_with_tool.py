"""Hosted tools - web search out of the box.

Copy of hello.py plus two lines:  import WebSearchTool, put it in tools=[...].
The runner decides when to search, searches, feeds the result back, loops, answers.

Run:
    python agent_with_tool.py                              # default question, WITH the tool
    python agent_with_tool.py --no-tool                    # same question, tool removed -> "go search yourself"
    python agent_with_tool.py "What is on piyushgarg.dev?" # your own question

Providers:
    LLM_PROVIDER=openai (SDK default)  WebSearchTool - OpenAI builds and runs it (Responses API).
    LLM_PROVIDER=groq                  OpenAI's hosted tools can't run on Groq, but Groq has its own
                                       hosted tool: {"type": "browser_search"}, run on Groq's side.
                                       Same idea, same tools=[...] shape, different provider.
"""
import os
import sys

from dotenv import load_dotenv
from agents import Agent, Runner
from agents import WebSearchTool            # (1) import the hosted tool

load_dotenv()

USE_TOOL = "--no-tool" not in sys.argv
QUESTION = " ".join(a for a in sys.argv[1:] if not a.startswith("--")) \
    or "What is the weather in Patiala, Punjab right now?"

INSTRUCTIONS = (
    "You greet the user and answer using emojis, in a funny way. "
    "If you searched the web, say so."
)


def build_agent() -> Agent:
    if os.getenv("LLM_PROVIDER", "openai") != "groq":
        # ---- the lecture's code -------------------------------------------------
        return Agent(
            name="Hello World Agent",
            instructions=INSTRUCTIONS,
            tools=[WebSearchTool()] if USE_TOOL else [],   # (2) give it to the agent (a list)
        )

    # ---- Groq path --------------------------------------------------------------
    # Groq's hosted web search is a provider-specific tool entry, not an SDK class.
    # ModelSettings.extra_args is the SDK's pass-through: it is merged into the
    # chat.completions call last, so this `tools` list reaches Groq untouched.
    from openai import AsyncOpenAI
    from agents import ModelSettings, OpenAIChatCompletionsModel, set_tracing_disabled

    set_tracing_disabled(True)
    groq = AsyncOpenAI(api_key=os.getenv("GROQ_API_KEY"), base_url="https://api.groq.com/openai/v1")
    hosted_search = {"tools": [{"type": "browser_search"}]}   # Groq runs it server-side
    return Agent(
        name="Hello World Agent",
        instructions=INSTRUCTIONS,
        model=OpenAIChatCompletionsModel(
            model=os.getenv("GROQ_MODEL", "openai/gpt-oss-120b"),
            openai_client=groq,
        ),
        model_settings=ModelSettings(extra_args=hosted_search if USE_TOOL else None),
    )


if __name__ == "__main__":
    agent = build_agent()
    print(f"[{os.getenv('LLM_PROVIDER', 'openai')} | tool: {'ON' if USE_TOOL else 'OFF'}] {QUESTION}\n")
    result = Runner.run_sync(agent, QUESTION)
    print(result.final_output)
