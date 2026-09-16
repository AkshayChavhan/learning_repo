from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import _bootstrap  # noqa: F401  re-launches under myenv/ if python3 is the wrong one

from llm_client import get_llm

def chat_with_model() -> None:

    llm = get_llm()

    prompt = """
    Explain what LangChain is in exactly three concise bullet points.
    """

    print("-" * 80)
    print("USER PROMPT: \n")
    print(prompt.strip())
    print("-" * 80)

    print("\nGenerating response ... \n")
    response = llm.invoke(prompt)

    print("-" * 80)
    print("AI RESPONSE: \n")
    print(response.text)
    print("-" * 80)

    print("-" * 80)
    print("AI RESPONSE TYPE: \n")
    print(response.type)
    print("-" * 80)

    # The whole object at once - the closest thing to console.log(obj) in JS.
    # .text above is only ONE field on the AIMessage; everything the provider
    # sent back is in here. model_dump_json() nests it properly, so you can
    # scan for what you need instead of reading one flat line.
    #
    #   print(response)                  same data, one unreadable line
    #   response.pretty_print()          just the role header and the content
    #   response.model_dump()            the same tree as a Python dict
    #
    # Worth looking for:
    #   usage_metadata      token counts - provider-neutral, use this for cost
    #   finish_reason       "stop" is normal; "length" means max_tokens TRUNCATED
    #                       the reply, and nothing else would tell you
    #   additional_kwargs   provider extras, e.g. gpt-oss puts its chain-of-
    #                       thought in reasoning_content
    print("-" * 80)
    print("FULL RESPONSE OBJECT: \n")
    print(response.model_dump_json(indent=2))
    print("-" * 80)

if(__name__ == "__main__"):
    chat_with_model()

# ======================================================================
#  Concept Summary
 
#  The entry point for every LangChain app: build a chat model, call .invoke()
#  with a prompt, read the reply.

#  Read response.text, not response.content. .text is a langchain_core property
#  that returns a plain string for every provider, while .content can be a list
#  of content blocks (Gemini does this) and breaks string operations.
#  response.type tells you the message role - "ai" for a model reply.

# ======================================================================