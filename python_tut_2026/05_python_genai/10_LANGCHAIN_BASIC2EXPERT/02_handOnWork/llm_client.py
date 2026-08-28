import json
import os

from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI

load_dotenv()

def load_config(config_path: str = 'config.json') -> dict :
    with open(config_path , "r") as file:
        return json.load(file)
    
def get_llm():
    config = load_config()
    provider = config["provider"].lower()

    if provider == "openai":
        return ChatOpenAI(
            model = config["openai"]["model"],
            temperature = config["openai"]["temperature"],
            max_tokens = config["openai"]["max_token"],
            api_key = os.getenv("OPENAI_API_KEY")
        )
    elif provider == "gemini":
        return ChatGoogleGenerativeAI(
            model = config["gemini"]["model"],
            temperature = config["gemini"]["temperature"],
            max_tokens = config["gemini"]["max_token"],
            api_key = os.getenv("GOOGLE_API_KEY")
        )
    elif provider == "anthropic":
        return ChatAnthropic(
            model = config["anthropic"]["model"],
            temperature = config["anthropic"]["temperature"],
            max_tokens = config["anthropic"]["max_token"],
            api_key = os.getenv("ANTHROPIC_API_KEY")
        )
    elif provider == "groq":
        # Groq is the fallback when Gemini's free daily quota runs out. It is
        # OpenAI-API-compatible, so the only thing that changes is the class,
        # the key and the model id.
        return ChatGroq(
            model = config["groq"]["model"],
            temperature = config["groq"]["temperature"],
            max_tokens = config["groq"]["max_token"],
            api_key = os.getenv("GROQ_API_KEY")
        )
    else:
        raise ValueError(
            f"Unsupported provider: {provider}. "
            f"Expected one of: openai, gemini, anthropic, groq"
        )