"""chat2.py - a LangGraph graph that can BRANCH.

chat.py ran a fixed line of nodes, every time. This one adds a *conditional
edge*: a function inspects the state and decides which node runs next. That
branching is the main reason to use LangGraph instead of a plain loop.

    START -> chatbot -> evaluate -> evaluate_response  (picks one)
                                           |
                            is_good True   +--> endnode                   -> END
                            is_good False  +--> chatbot_gemini -> endnode -> END

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


# Sent to the model when it grades an answer. Demanding one word makes the
# reply trivial to parse - ask for a sentence and you have to interpret prose.
JUDGE_PROMPT = """You grade answers to questions. Reply with exactly one word:

GOOD - the answer is correct, on topic, and actually answers the question
BAD  - it is wrong, empty, off topic, or refuses to answer

One word. No explanation."""


def evaluate(state: State):
    """Judge the answer and record the verdict in the state.

    This must be a NODE, not the router. LangGraph only keeps changes that a
    node RETURNS - anything a router writes into state is thrown away, so
    is_good would silently stay None if this lived in evaluate_response.
    """
    print("evaluate node", state)
    answer = (state.get("llm_output") or "").strip()

    # Cheap check first. An empty answer is bad without asking anyone,
    # and skipping the call saves money on the obvious cases.
    if not answer:
        return {"is_good": False}

    # LLM-as-judge: ask the model to grade the answer it just produced.
    verdict = client.chat.completions.create(
        model="gpt-4.1-mini",
        temperature=0,          # grading should be repeatable, not creative
        messages=[
            {"role": "system", "content": JUDGE_PROMPT},
            {"role": "user",
             "content": f"Question: {state.get('user_query')}\n\nAnswer: {answer}"},
        ],
    ).choices[0].message.content

    # Anything other than a clear GOOD counts as bad. Better to retry a fine
    # answer than to wave a broken one through.
    is_good = verdict.strip().upper().startswith("GOOD")
    print(f"  judge said {verdict.strip()!r} -> is_good={is_good}")
    return {"is_good": is_good}


def evaluate_response(state:State) -> Literal["chatbot_gemini" , "endnode"]:
    """The ROUTER. Decides where the graph goes next.

    A router is not a normal node - it does no work and changes nothing.
    It just returns the NAME of the node to run next, as a string. The name
    must match an add_node() name exactly or the graph fails.

    The Literal[...] return type lists the only destinations it can pick.
    LangGraph reads that to draw the graph and to catch typos early.
    """
    print("evaluate_response router", state)
    return "endnode" if state.get("is_good") else "chatbot_gemini"


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
graph_builder.add_node("evaluate",evaluate)
graph_builder.add_node("chatbot_gemini",chatbot_gemini)
graph_builder.add_node("endnode",endnode)


# A normal edge is unconditional: always go from A to B.
graph_builder.add_edge(START , "chatbot")
graph_builder.add_edge("chatbot" , "evaluate")

# A conditional edge hands control to the router. Whatever string
# evaluate_response returns becomes the next node.
graph_builder.add_conditional_edges("evaluate", evaluate_response)


graph_builder.add_edge("chatbot_gemini" , "endnode")
graph_builder.add_edge("endnode" , END)

# compile() checks the graph (nodes reachable, edges valid) and returns
# something runnable.
graph = graph_builder.compile()

# invoke() runs the graph once and returns the final state. Only user_query
# is set at the start; the other keys get filled in along the way.
updated_state = graph.invoke(State({"user_query":"Hey , What is 2+2"}))
print(updated_state)
