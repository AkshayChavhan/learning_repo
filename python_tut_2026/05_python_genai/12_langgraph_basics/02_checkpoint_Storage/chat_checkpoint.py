from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from  langgraph.graph import StateGraph ,START ,  END
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.mongodb import MongoDBSaver


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

graph_builder = StateGraph(State)

graph_builder.add_node("chatbot" , chatbot)

graph_builder.add_edge(START , "chatbot")
graph_builder.add_edge("chatbot", END)

# Compiled with NO checkpointer - this version forgets everything
# between runs. Kept only for contrast; it is not used below.
graph = graph_builder.compile()

def compile_graph_checkpointer(checkpointer):
    return graph_builder.compile(checkpointer=checkpointer)

# user:password@host:port/database - "langgraph_basics" is the database
# name; Mongo creates it on first write, so any name works here.
DB_URI = "mongodb://admin:admin@localhost:27017/langgraph_basics"
with MongoDBSaver.from_conn_string(DB_URI) as checkpointer:
    graph_with_checkpointer = compile_graph_checkpointer(checkpointer)
    config = {
        "configurable": {
            "thread_id": "piyush"
        }
    }
    updated_state = graph_with_checkpointer.invoke(
        State({"messages": ["Hi , My name is Piyush Garg"]}),
        config,
    )
    print("\n\nUpdated State  ->", updated_state)


