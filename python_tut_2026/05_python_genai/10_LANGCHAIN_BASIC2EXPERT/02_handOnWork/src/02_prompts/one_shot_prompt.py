from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import _bootstrap  # noqa: F401  re-launches under myenv/ if python3 is the wrong one

from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from llm_client import get_llm
from utils.helpers import print_seperator, print_title

def main():
    print_title("One-Shot Prompting")
    llm = get_llm()

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are an expert sentiment analysis assistant."
            ),
            (
                "human",
                """
                Classify the sentiment as Positive, Negetive or Neutral.
                
                Example:
                
                Review: "The laptop is fast, lightweight, and has an amazing battery life."
                Sentiment: Positive

                Now classify the following review:
                Review: "{review}"
                """,                     
            ),
        ]
    )

    messages = prompt.invoke(
        {
            "review":"The phone looks premium, but its battery drains very quickly."
        }
    )

    print("Formatted messages:\n")

    for message in messages.messages:
        print(f"{message.type.upper()}:")
        print(message.content)
        print()

    print_seperator()
     
    response = llm.invoke(messages)

    print("LLM Response:\n")
    print(response.text)

if __name__ == "__main__":
    main()