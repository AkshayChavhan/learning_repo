from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import _bootstrap  # noqa: F401  re-launches under myenv/ if python3 is the wrong one

from langchain_classic.memory import ConversationTokenBufferMemory
from langchain_core.messages import AIMessage, HumanMessage

from llm_client import get_llm
from utils.helpers import print_seperator, print_title


def main():
    print_title("Conversation Token Buffer Memory")
    llm = get_llm()
    # llm= is here as a TOKEN COUNTER, not a generator - no request is ever sent
    # to Groq by this script. The keyword is max_token_limit; pydantic ignores
    # unknown kwargs, so a misspelling like maxTokens=100 is silently dropped and
    # you quietly get the 2000 default instead of an error.
    memory = ConversationTokenBufferMemory(llm=llm, max_token_limit=100, return_messages=True)

    conversations = [
        ("Hi, how are you?", "I'm good, thank you!"),
        ("What is your name?", "My name is John."),
        ("What is your favorite color?", "My favorite color is blue."),
        ("What is your favorite food?", "My favorite food is pizza."),
        ("What is your favorite animal?", "My favorite animal is a dog."),
        ("What is your favorite book?", "My favorite book is The Great Gatsby."),
        ("What is your favorite movie?", "My favorite movie is The Godfather."),
        ("What is your favorite music?", "My favorite music is jazz."),
        ("What is your favorite sport?", "My favorite sport is basketball."),
    ]

    for human, ai  in conversations:
        memory.save_context({"input": human}, {"output": ai})

    # {} is the chain's current inputs - required by the interface, ignored
    # here. See conversation_buffer_memory.py for the full note.
    history = memory.load_memory_variables({})

    print("Complete conversation:")
    print(history)
    print("--------------------------------")

    for index, message in enumerate(history["history"],start=1):
        print(f"Message {index}: {message}")
        print("--------------------------------")
        
if __name__ == "__main__":
    main()