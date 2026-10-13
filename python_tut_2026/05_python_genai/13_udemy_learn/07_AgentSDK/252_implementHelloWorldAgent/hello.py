"""Hello World Agent - the OpenAI Agents SDK in three real lines.

    Agent(...)            -> name + instructions (+ tools, handoffs, guardrails later)
    Runner.run_sync(...)  -> the whole loop: LLM call -> tool calls -> repeat -> final answer
    result.final_output   -> the text the agent ended with

Run:
    python hello.py                       # OpenAI (the SDK's default) - needs OPENAI_API_KEY with credits
    LLM_PROVIDER=groq python hello.py     # same Agent/Runner, model served by Groq (free tier)
"""
import os

from dotenv import load_dotenv
from agents import Agent, Runner

load_dotenv()  # OPENAI_API_KEY (and GROQ_API_KEY) come from ./.env, never from code


def pick_model():
    """None -> the SDK default (OpenAI). Or a Groq-backed model via the SDK's
    OpenAIChatCompletionsModel: any OpenAI-compatible endpoint can serve an Agent."""
    if os.getenv("LLM_PROVIDER", "openai") != "groq":
        return None

    from openai import AsyncOpenAI
    from agents import OpenAIChatCompletionsModel, set_tracing_disabled

    set_tracing_disabled(True)  # tracing uploads runs to OpenAI's dashboard; needs an OpenAI key
    groq = AsyncOpenAI(api_key=os.getenv("GROQ_API_KEY"), base_url="https://api.groq.com/openai/v1")
    return OpenAIChatCompletionsModel(
        model=os.getenv("GROQ_MODEL", "openai/gpt-oss-120b"),  # llama-3.3-70b-versatile is retired on Groq (404)
        openai_client=groq,
    )


# 1. define the agent: a name + instructions (+ tools later)
hello_agent = Agent(
    name="Hello World Agent",
    instructions="You greet the user and answer using emojis, in a funny way.",
    model=pick_model(),
)

if __name__ == "__main__":
    # 2. run it with an input - no while-loop, no messages list, no tool dispatch: Runner does it
    result = Runner.run_sync(hello_agent, "Hello, my name is Akshay")

    # 3. read the final answer
    print(result.final_output)
