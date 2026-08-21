"""A minimal LangGraph chatbot: START -> chatbot -> sampleNode -> END.

LangGraph runs your nodes as a graph instead of top-to-bottom code. Each node
is a plain function that receives the current state and returns the bits of
state it wants to change. LangGraph merges those changes and moves along the
edges to the next node.

Setup, once:

    uv venv --python 3.12                       # or: python3 -m venv .venv
    source .venv/bin/activate
    uv pip install langgraph langchain langchain-openai python-dotenv

    The package is python-dotenv, NOT dotenv. `pip install dotenv`
    pulls a deprecated stub. Both are imported as `from dotenv import
    load_dotenv`, which is why picking the wrong one is easy to miss.

Pin what you installed, so the setup is repeatable:

    uv pip freeze > requirements.txt             # plain pip: pip freeze > requirements.txt
    uv pip install -r requirements.txt          # rebuild it later

Run `freeze` inside the venv. Outside it, you capture every package on
the machine, system libraries included.

Put your key in .env next to this file:

    OPENAI_API_KEY=sk-...

Run it:

    ./.venv/bin/python chat.py
"""

from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph , START , END
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv


# Read .env into environment variables. The OpenAI client looks for
# OPENAI_API_KEY there - the name must match exactly or the key is invisible.
load_dotenv()

# init_chat_model picks the right client from the provider name, so swapping
# to another model later is a one-line change.
llm = init_chat_model(
    model="gpt-4.1-mini",
    model_provider="openai"
)


class State(TypedDict):
    """The shared memory every node reads from and writes to.

    Annotated[list, add_messages] attaches a *reducer*. When a node returns
    "messages", add_messages APPENDS to the list instead of overwriting it -
    which is what makes the conversation build up. A plain `list` here would
    throw away the history on every node.

    add_messages also converts plain strings into message objects
    (HumanMessage, AIMessage) and gives each one an id.

    Careful: a node returning a key that is NOT in this class is silently
    dropped - no warning, no error. That is the most common LangGraph bug.
    """
    messages: Annotated[list , add_messages]


def chatbot(state:State):
    """Send the conversation so far to the model, append its reply."""
    # state.get("messages") is the whole history, not just the last message,
    # so the model always sees the full context.
    response = llm.invoke(state.get("messages"))
    return { "messages": [response]}


def sampleNode(state: State):
    """A second node, here only to show the graph really does run in order."""
    print("\n\nInside chatbot sample node")
    return { "messages":["Sample Message Appended"]}


# The builder collects nodes and edges. Nothing runs until .compile().
graph_builder = StateGraph(State)

# add_node(name, function) - the name is how edges refer to it.
graph_builder.add_node("chatbot" , chatbot)
graph_builder.add_node("sampleNode" , sampleNode)

# Edges define the order. START and END are built-in markers for the
# entry and exit points.
graph_builder.add_edge(START,"chatbot")
graph_builder.add_edge("chatbot","sampleNode")
graph_builder.add_edge("sampleNode",END)


# {START} -> chatbot  -> sampleNode -> END


# compile() validates the graph (every node reachable, no dangling edges)
# and returns something runnable.
graph = graph_builder.compile()

# invoke() runs the whole graph once and returns the final state.
# The starting message is a plain string; add_messages turns it into a
# HumanMessage on the way in.
updated_state = graph.invoke(State({"messages": ["Hi ,My name is Akshay Chavhan"]}))

# Final state: every message from every node, in the order they were added.
print("Updated State" , updated_state)


# to run code
# ./.venv/bin/python chat.py
