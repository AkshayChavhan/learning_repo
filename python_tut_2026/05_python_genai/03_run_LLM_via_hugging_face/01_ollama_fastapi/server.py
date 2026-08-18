# (to run the server) python -m fastapi dev server.py

from fastapi import FastAPI
from ollama import Client

client = Client(
    host="http://localhost:11434"  # default port for ollama and start docker ollama
)
app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

def chat_with_ollama(prompt: str):
    response = client.chat(
        model="llama3.1:8b",  # default model for ollama
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.message.content

@app.post("/chat")
def chat(prompt: str):
    return chat_with_ollama(prompt)