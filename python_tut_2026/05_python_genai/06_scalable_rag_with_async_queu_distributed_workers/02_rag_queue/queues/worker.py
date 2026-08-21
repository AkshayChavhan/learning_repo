import os
from dotenv import load_dotenv

from openai import OpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore

load_dotenv()

# OpenAI client is used to connect to the OpenAI API
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Embedding model is used to convert the text into a vector
embedding_model = OpenAIEmbeddings(model="text-embedding-3-large")

# Qdrant vector store is used to read the vectors from the database.
# NOTE: QdrantVectorStore(...) takes a `client`, NOT a `url`. To connect by URL
# use the from_existing_collection() classmethod instead.
# Built lazily so importing this module does not require Qdrant to be running -
# only the worker actually needs it, the API server does not.
_vector_db = None


def get_vector_db():
    global _vector_db
    if _vector_db is None:
        _vector_db = QdrantVectorStore.from_existing_collection(
            collection_name="rag_collection",
            embedding=embedding_model,
            url="http://localhost:6333",
        )
    return _vector_db


# Vector store is used to store the vectors in the database
def process_query(query):
    print(f"Processing query: {query}")
    search_results = get_vector_db().similarity_search(query, k=3)
    print(f"Search results: {search_results}")
    
    context = "\n\n\n".join([f"Page Content: {result.page_content}" for result in search_results])

    SYSTEM_PROMPT = """
    You are a helpful assistant that can answer questions about the following context:
    {context}
    """
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": query}
        ]
    )
    print(f"Response: {response.choices[0].message.content}")
    return response.choices[0].message.content

