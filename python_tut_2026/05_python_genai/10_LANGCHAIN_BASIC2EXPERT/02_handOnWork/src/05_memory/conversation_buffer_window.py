from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import _bootstrap  # noqa: F401  re-launches under myenv/ if python3 is the wrong one

from langchain_classic.memory import ConversationBufferWindowMemory
from langchain_core.messages import AIMessage, HumanMessage

from llm_client import get_llm
from utils.helpers import print_seperator, print_title


def main():
    print_title("Conversation Buffer Window Memory")
    memory = ConversationBufferWindowMemory(k=2, return_messages=True)

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

    # The {} is the chain's current inputs - required by the interface, ignored
    # by this memory. See conversation_buffer_memory.py for the full note.
    #
    # Only the last k=2 exchanges come back, so this prints 4 messages, not 18.
    # The other 7 pairs are NOT deleted though - save_context appends every one
    # of them, and the window is just a slice taken on the way out:
    #
    #     self.chat_memory.messages[-self.k * 2:]
    #
    # So memory.chat_memory.messages still holds all 18. k bounds what the model
    # is shown and therefore the token bill; it does not bound what is retained.
    history = memory.load_memory_variables({})

    print("Complete conversation:")
    print(history)
    print("--------------------------------")

    for index, message in enumerate(history["history"],start=1):
        print(f"Message {index}: {message}")
        print("--------------------------------")

if __name__ == "__main__":
    main()