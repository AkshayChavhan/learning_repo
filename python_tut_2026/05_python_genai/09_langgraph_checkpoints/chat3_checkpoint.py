"""chat3_checkpoint.py - a LangGraph chatbot that REMEMBERS between runs.

chat.py forgot everything the moment it finished. Every run started from an
empty message list. This one adds a *checkpointer*: after each step LangGraph
saves the state to MongoDB, so the next run picks the conversation back up.

    START -> chatbot -> END        (+ state saved to MongoDB after each step)

The conversation is identified by a `thread_id`. Same thread_id means same
history; a new thread_id starts a fresh conversation. That one string is how
a real chat app keeps thousands of users' conversations apart.

Setup, once:

    uv venv --seed --python 3.12        # --seed puts a real pip inside the venv
    source .venv/bin/activate
    pip install langgraph langchain langchain-openai python-dotenv \\
                langgraph-checkpoint-mongodb

    The package is python-dotenv, NOT dotenv. `pip install dotenv` pulls a
    deprecated stub. Both are imported as `from dotenv import load_dotenv`,
    which is why picking the wrong one is easy to miss.

Pin what you installed, so the setup is repeatable:

    pip freeze > requirements.txt       # run this INSIDE the venv
    pip install -r requirements.txt     # rebuild it later

Run `freeze` inside the venv. Outside it, you capture every package on the
machine, system libraries included.

You also need MongoDB running - the checkpointer writes there. It is
defined in docker-compose.yml next to this file:

    docker compose up -d          # start it in the background
    docker compose ps             # check it is running
    docker compose down           # stop it
    docker compose down -v        # stop it AND wipe the saved conversations

    This file is named docker-compose.yml, one of the names Docker finds on
    its own, so a bare `docker compose up` works. (The RAG folder's file is
    called docker-composer.yml - with an r - which Docker does NOT recognise,
    so that one needs `-f docker-composer.yml`.)

The compose file also declares a named volume, mongodb_data, so your
conversations survive `docker compose down`. Only `down -v` deletes them.

    Check the port is open:  nc -z localhost 27017 && echo open

Put your key in .env next to this file:

    OPENAI_API_KEY=sk-...

Run it:

    python chat3_checkpoint.py          # after activating
    ./.venv/bin/python chat3_checkpoint.py

Run it twice with the same thread_id. The second run still knows your name -
that is the whole point.
"""

from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph , START , END
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv

# The MongoDB checkpointer ships in its own package,
# `langgraph-checkpoint-mongodb`, not in langgraph itself.
from langgraph.checkpoint.mongodb import MongoDBSaver

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
    # so the model always sees the full context. With a checkpointer that
    # history includes earlier RUNS, not just earlier nodes.
    response = llm.invoke(state.get("messages"))
    return { "messages": [response]}

# The builder collects nodes and edges. Nothing runs until .compile().
graph_builder = StateGraph(State)

# add_node(name, function) - the name is how edges refer to it.
graph_builder.add_node("chatbot" , chatbot)

# Edges define the order. START and END are built-in markers for the
# entry and exit points.
graph_builder.add_edge(START,"chatbot")
graph_builder.add_edge("chatbot" ,END)


# Compiled with NO checkpointer: this version forgets everything between
# runs. Kept here only for contrast - it is not the one used below.
graph = graph_builder.compile()


def compile_graph_with_checkpointer(checkpointer):
    """Same graph, but told where to save state after every step.

    The checkpointer is passed at compile time, not build time - so one
    builder can produce both a forgetful graph and a remembering one.
    """
    return graph_builder.compile(checkpointer=checkpointer)


# user:password@host:port/database
# admin:admin comes from MONGO_INITDB_ROOT_USERNAME/PASSWORD in
# docker-compose.yml. Change one and you must change the other.
# "lg" is the database name - Mongo creates it on first write.
DB_URI = "mongodb://admin:admin@localhost:27017/lg"

# `with` because the saver holds a database connection and must close it.
with MongoDBSaver.from_conn_string(DB_URI) as checkpointer:
    graph_with_checkpointer = compile_graph_with_checkpointer(checkpointer)

    # thread_id names the conversation. Reuse it to continue that chat;
    # change it to start a clean one. It must sit under "configurable".
    config = {
        "configurable": {
        "thread_id":'piyush'
        }
    }

    # stream() yields as the graph runs, instead of waiting for the end
    # like invoke() does. stream_mode="values" means each chunk is the
    # WHOLE state so far, so [-1] is the newest message.
    for chunk in graph_with_checkpointer.stream(State({"messages": ["Hi ,My name is Akshay Chavhan"]}),config, stream_mode="values"):
        # pretty_print() formats a message with its role, instead of
        # dumping the raw object.
        chunk["messages"][-1].pretty_print()
