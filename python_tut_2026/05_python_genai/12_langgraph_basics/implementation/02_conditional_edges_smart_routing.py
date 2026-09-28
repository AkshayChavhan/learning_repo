"""chat2.py - a LangGraph graph that can genuinely BRANCH.

chat.py runs a fixed line of nodes every time. This one adds a *conditional
edge*: a router function inspects the state and decides which node runs next.

    START -> chatbot -> evaluate -> evaluate_response  (router, picks one)
                                           |
                            is_good True   +--> endnode                   -> END
                            is_good False  +--> chatbot_gemini -> endnode -> END

This file originally had `if True: return endnode` in the router - a
hardcoded branch that always took the same path no matter what the model
answered. Two things make the branch real now:

  1. `evaluate` is a NODE, not the router. LangGraph only keeps state changes
     a node RETURNS - if the judging happened inside evaluate_response
     instead, is_good would silently stay None and the router would have
     nothing real to read.
  2. `evaluate_response` returns a STRING - "endnode" or "chatbot_gemini" -
     matching an add_node() name exactly. Returning the function itself
     (the original `return endnode`, no quotes) is not a name LangGraph can
     use as a destination.

Put your key in .env next to this file:

    OPENAI_API_KEY=sk-...

Run it:

    python chat2.py
"""

from dotenv import load_dotenv
from typing_extensions import TypedDict
from typing import Optional, Literal
from langgraph.graph import StateGraph, START, END
from openai import OpenAI

# Reads .env into environment variables. OpenAI() then finds OPENAI_API_KEY
# there by itself - the name must match exactly or the key stays invisible.
load_dotenv()
client = OpenAI()


class State(TypedDict):
    user_query: str
    llm_output: Optional[str]
    is_good: Optional[bool]


def chatbot(state: State):
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "user", "content": state.get("user_query")}
        ]
    )

    state["llm_output"] = response.choices[0].message.content
    return state


# Sent to the model when it grades an answer. Demanding one word keeps the
# reply trivial to parse - ask for a sentence and you have to interpret prose.
JUDGE_PROMPT = """You grade answers to questions. Reply with exactly one word:

GOOD - the answer is correct, on topic, and actually answers the question
BAD  - it is wrong, empty, off topic, or refuses to answer

One word. No explanation."""


def evaluate(state: State):
    """Judge the answer and record a REAL verdict in the state.

    This must be a NODE, not the router - LangGraph only keeps changes a node
    RETURNS, so is_good would silently stay None if this lived in the router.
    """
    answer = (state.get("llm_output") or "").strip()

    if not answer:
        return {"is_good": False}

    verdict = client.chat.completions.create(
        model="gpt-4.1-mini",
        temperature=0,          # grading should be repeatable, not creative
        messages=[
            {"role": "system", "content": JUDGE_PROMPT},
            {"role": "user",
             "content": f"Question: {state.get('user_query')}\n\nAnswer: {answer}"},
        ],
    ).choices[0].message.content

    is_good = verdict.strip().upper().startswith("GOOD")
    return {"is_good": is_good}


def evaluate_response(state: State) -> Literal["chatbot_gemini", "endnode"]:
    """The ROUTER. Branches on the REAL verdict `evaluate` just wrote, instead
    of a hardcoded `if True:`. It must return a NAME (a string matching an
    add_node() call), never the function object itself.
    """
    return "endnode" if state.get("is_good") else "chatbot_gemini"


def chatbot_gemini(state: State):
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "user", "content": state.get("user_query")}
        ]
    )

    state["llm_output"] = response.choices[0].message.content
    return state


def endnode(state: State):
    return state


graph_builder = StateGraph(State)

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("evaluate", evaluate)
graph_builder.add_node("chatbot_gemini", chatbot_gemini)
graph_builder.add_node("endnode", endnode)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", "evaluate")
graph_builder.add_conditional_edges("evaluate", evaluate_response)

graph_builder.add_edge("chatbot_gemini", "endnode")
graph_builder.add_edge("endnode", END)

graph = graph_builder.compile()

updated_state = graph.invoke(State({"user_query": "Hey, What is 2+2 ?"}))

print(updated_state)


# ======================================================================
#  Graph flow
#
#      START -> chatbot -> evaluate -> evaluate_response  (router)
#                                              |
#                       is_good True   -------+--> endnode                   -> END
#                       is_good False  -------+--> chatbot_gemini -> endnode -> END
#
#  evaluate writes the real is_good the router reads - that's what replaced
#  the old hardcoded `if True:` with a genuine branch.
# ======================================================================
