from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import _bootstrap  # noqa: F401  re-launches under myenv/ if python3 is the wrong one

from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from llm_client import get_llm
from utils.helpers import print_seperator, print_title

def main():
    print_title("Messages-Placeholder")
    llm = get_llm()

    chat_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are an helpful AI tutor who answers the questions based on ongoing conversation."
            ),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{question}"),
        ]
    )

# Below we havent learnt yet.So adding simulation ""chat_history"""
    chat_history = [
        HumanMessage(content="What is Langchain?"),
        AIMessage(
            content=(
                "LangChain is a framework for building applications"
                "powered by Large Language Models."
            )
        ),
        HumanMessage(content="What is Prompt Templates?"),
        AIMessage(
            content=(
                "Prompt Template help create reusable prompts by"
                "allowing dynamic variables."
            )
        ),
    ]

    messages = chat_prompt.invoke(
        {
        "chat_history": chat_history ,
        "question": "Can you summerize both concept in simple terms ?"
        }
    )

    print("Formatted messages:\n")

    # for message in messages.messages:
    #     print(f"{message.type.upper()}:")
    #     print(message.content)
    #     print()

    print_seperator()
     
    response = llm.invoke(messages)

    print("LLM Responses:\n")
    print(response.text)

if __name__ == "__main__":
    main()