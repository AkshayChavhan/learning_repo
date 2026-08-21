from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph , START , END



class State(TypedDict):
    messages: Annotated[list , add_messages]


def chatbot(state:State):
    print("\n\nInside chatbot node")
    return { "messages": ["Hi , This is a message from chatbot"]}


def sampleNode(state: State):
    print("\n\nInside chatbot sample node")
    return { "messages":["Sample Message Appended"]}


graph_builder = StateGraph(State)

graph_builder.add_node("chatbot" , chatbot)
graph_builder.add_node("sampleNode" , sampleNode)

graph_builder.add_edge(START,"chatbot")
graph_builder.add_edge("chatbot","sampleNode")
graph_builder.add_edge("sampleNode",END)


# {START} -> chatbot  -> sampleNode -> END


graph = graph_builder.compile()

updated_state = graph.invoke(State({"messages": ["Hi ,My name is Akshay Chavhan"]}))

print("Updated State" , updated_state)
