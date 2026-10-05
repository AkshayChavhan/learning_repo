from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from  langgraph.graph import StateGraph ,START ,  END
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv

# Reads .env into the environment. ChatGoogleGenerativeAI (what google_genai
# resolves to) looks for GOOGLE_API_KEY there - without this call it only
# sees a key you exported by hand in the shell.
load_dotenv()

llm = init_chat_model(
    model="models/gemini-3.6-flash",
    model_provider="google_genai"
)

class State(TypedDict):
    messages: Annotated[list , add_messages]


def chatbot(state: State):
    response =llm.invoke(state.get("messages"))
    print("\n\nInside chatbot node" , state)
    return { "messages" : [response]}

def samplenode (state: State):
    print("\n\nInside samplenode node" , state)
    return {"messages": ["Sample Message Appended."]}

graph_builder = StateGraph(State)

graph_builder.add_node("chatbot" , chatbot)
graph_builder.add_node("samplenode", samplenode)

graph_builder.add_edge(START , "chatbot")
graph_builder.add_edge("chatbot", "samplenode")
graph_builder.add_edge("samplenode", END)

graph = graph_builder.compile()

updated_state = graph.invoke(State({"messages": ["Hi , My name is Piyush Garg"]}))
print("\n\nUpdated State  ->", updated_state)
