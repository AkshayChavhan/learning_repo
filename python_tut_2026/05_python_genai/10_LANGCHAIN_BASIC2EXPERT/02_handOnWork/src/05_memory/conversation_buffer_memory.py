from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import _bootstrap  # noqa: F401  re-launches under myenv/ if python3 is the wrong one

from langchain_classic.memory import ConversationBufferMemory
from langchain_core.messages import AIMessage, HumanMessage

from llm_client import get_llm
from utils.helpers import print_seperator, print_title


def main():
    print_title("Conversation Buffer Memory")
    memory = ConversationBufferMemory(return_messages=True)
    memory.save_context({"input": "Hi"}, {"output": "What's up?"})
    memory.save_context({"input": "Not much, you?"}, {"output": "Just hanging out here."})
    memory.save_context({"input": "What is up?"}, {"output": "Just working on my project."})
    
    # load_memory_variables() takes the chain's current inputs as a required
    # argument. ConversationBufferMemory ignores it - it replays everything it
    # stored regardless - but the argument is still part of the interface, so
    # pass an empty dict. Memories that DO read it are the summarising and
    # retrieval-backed ones, which need the current question to decide what to
    # pull back.
    history = memory.load_memory_variables({})

    print("Complete conversation:")
    print(history)
    print("--------------------------------")

    for index, message in enumerate(history["history"],start=1):
        print(f"Message {index}: {message}")
        print("--------------------------------")

if __name__ == "__main__":
    main()