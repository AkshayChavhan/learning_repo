"""chat2.py - a LangGraph graph that can BRANCH.

chat.py ran a fixed line of nodes, every time. This one adds a *conditional
edge*: a function inspects the state and decides which node runs next. That
branching is the main reason to use LangGraph instead of a plain loop.

    START -> chatbot -> evaluate_response  (picks one)
                              |
                              +--> endnode                     -> END
                              +--> chatbot_gemini -> endnode   -> END

Setup, once:

    uv venv --seed --python 3.12        # --seed puts a real pip inside the venv
    source .venv/bin/activate
    pip install langgraph openai python-dotenv

Pin what you installed, so the setup is repeatable:

    pip freeze > requirements.txt       # run this INSIDE the venv
    pip install -r requirements.txt     # rebuild it later

Run `freeze` inside the venv. Outside it, you capture every package on the
machine, system libraries included.

Put your key in .env next to this file:

    OPENAI_API_KEY=sk-...

Run it:

    python chat2.py                     # after activating
    ./.venv/bin/python chat2.py         # without activating
"""

from dotenv import load_dotenv
from typing_extensions import TypedDict
from typing import Literal, Optional
from langgraph.graph import StateGraph , START , END
from openai import OpenAI

# Reads .env into environment variables. OpenAI() then finds OPENAI_API_KEY
# there by itself - the name must match exactly or the key stays invisible.
load_dotenv()
client = OpenAI()


class State(TypedDict):
    """The dictionary that is handed from node to node.

    Every node receives this and returns it (or the parts it changed).
    Think of it as the graph's memory.

    Optional[...] fields start out missing and get filled in as nodes run:
    llm_output is None until chatbot writes to it.

    Note there is no `Annotated[..., add_messages]` here like in chat.py.
    These are plain values, so a node writing llm_output OVERWRITES whatever
    was there. Reducers are what make values accumulate instead.
    """
    user_query:str
    llm_output: Optional[str]
    is_good: Optional[bool]


def chatbot(state: State):
    """First node: send the user's question to the model, store the reply."""
    print("chatbot node", state)
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            { "role": "user", "content":state.get("user_query")}
        ]
    )

    # .choices is a list because the API can return several alternatives.
    # [0] is the first (and here, only) one.
    state["llm_output"] = response.choices[0].message.content
    return state


def evaluate_response(state:State) -> Literal["chatbot_gemini" , "endnode"]:
    """The ROUTER. This one decides where the graph goes next.

    A router is not a normal node - it does no work and changes nothing.
    It just returns the NAME of the node to run next, as a string. The name
    must match an add_node() name exactly or the graph fails.

    The Literal[...] return type lists the only destinations it can pick.
    LangGraph reads that to draw the graph and to catch typos early.
    """
    print("evaluate_response node", state)

    # Hardcoded for now, so this always ends immediately and chatbot_gemini
    # never runs. Replace `True` with a real check - for example, whether
    # llm_output is empty or too short - to make the other branch fire.
    if True:
        return "endnode"

    return "chatbot_gemini"


def chatbot_gemini(state: State):
    """The fallback branch: retry the question with another model.

    Currently unreachable, because evaluate_response always returns
    "endnode" above.
    """
    print("chatbot_gemini node", state)
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages= [
            {"role": "user","content":state.get("user_query")}
        ]
    )

    state["llm_output"] = response.choices[0].message.content
    return state


def endnode(state:State):
    """Last stop. Does nothing but show the final state."""
    print("endnode node", state)
    return state


# The builder collects nodes and edges. Nothing runs until .compile().
graph_builder = StateGraph(State)


# add_node(name, function) - the name is the label edges and routers use.
graph_builder.add_node("chatbot",chatbot)
graph_builder.add_node("chatbot_gemini",chatbot_gemini)
graph_builder.add_node("endnode",endnode)


# A normal edge is unconditional: always go from A to B.
graph_builder.add_edge(START , "chatbot")

# A conditional edge hands control to the router. Whatever string
# evaluate_response returns becomes the next node.
graph_builder.add_conditional_edges("chatbot", evaluate_response)


graph_builder.add_edge("chatbot_gemini" , "endnode")
graph_builder.add_edge("endnode" , END)

# compile() checks the graph (nodes reachable, edges valid) and returns
# something runnable.
graph = graph_builder.compile()

# invoke() runs the graph once and returns the final state. Only user_query
# is set at the start; the other keys get filled in along the way.
updated_state = graph.invoke(State({"user_query":"Hey , What is 2+2"}))
print(updated_state)
