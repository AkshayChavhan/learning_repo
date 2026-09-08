from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import _bootstrap  # noqa: F401  re-launches under myenv/ if python3 is the wrong one

from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.messages import AIMessage, HumanMessage

from llm_client import get_llm
from utils.helpers import print_seperator, print_title

def main():
    print_title("Chat Message History")
    chat_history = InMemoryChatMessageHistory()
    chat_history.add_messages([
        HumanMessage(content="What is the capital of France?"),
        AIMessage(content="The capital of France is Paris."),
    ])
    chat_history.add_messages([
        HumanMessage(content="What is the capital of Germany?"),
        AIMessage(content="The capital of Germany is Berlin."),
    ])
    print(chat_history.messages)

if __name__ == "__main__":
    main()

# ======================================================================
#  Concept Summary
 
#  Chat history is just an ordered list of Message objects - the substrate every
#  memory class is built on.

#  InMemoryChatMessageHistory stores HumanMessage and AIMessage in order and
#  replays them. Models are stateless: they remember nothing between calls, so
#  "memory" is only ever text you resend. Understanding that makes every memory
#  class below it obvious.

# ======================================================================