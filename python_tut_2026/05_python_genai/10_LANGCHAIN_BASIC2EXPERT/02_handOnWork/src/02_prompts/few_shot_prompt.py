from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from llm_client import get_llm
from utils.helpers import print_seperator, print_title

def main():
    print_title("FEW-Shot Prompting")
    llm = get_llm()

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
                You are an AI assistant that categorizes customer support tickets.

                Classify each ticket into exactly one category from the following:
                -Billing
                -Technical Issue
                -Account Management
                -Feature Request
                -General Inquery

                Respond only with the category name.
                """
            ),
            (
                "human",
                f"""
                Example 1 
                Ticket:
                I was charged twice for my monthly subscription.

                Category:
                Billing

                -----------------------------------

                Example 2
                Ticket:
                I forgot my password and can't log into my account.

                Category:
                Account Management

                -----------------------------------

                Example 3
                Ticket:
                The mobile app crashes every time I upload a photo.

                Category:
                Technical Issue

                -----------------------------------

                Now classify this ticket:

                Ticket:
                {ticket}

                Category:
                """,                     
            ),
        ]
    )

    messages = prompt.invoke(
        {
            "ticket":(
                "It would be great if your platform could support"
                "dark mode for the dashboard."
            )
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