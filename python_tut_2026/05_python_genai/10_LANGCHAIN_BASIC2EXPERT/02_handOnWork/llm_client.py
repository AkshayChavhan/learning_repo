import json
import os

from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI

# .env and config.json both sit next to THIS file. Resolve them from the file's
# own location, never the current working directory - otherwise running a script
# from src/02_prompts/ dies with FileNotFoundError: 'config.json', because the
# cwd is that subfolder rather than the project root.
_HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_CONFIG = os.path.join(_HERE, "config.json")

# Bare load_dotenv() guesses the path by walking up from the calling frame, which
# silently falls back to the cwd when there is no real file frame (python -c, a
# notebook, some test runners) - and then finds no key. Point it at the file.
load_dotenv(os.path.join(_HERE, ".env"))

def load_config(config_path: str = DEFAULT_CONFIG) -> dict :
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
        #
        # gpt-oss is a reasoning model, and max_tokens caps reasoning + answer
        # together - so thinking eats the budget before any visible text is
        # produced. Measured on a 3-token prompt: "low" spends ~17 reasoning
        # tokens where the default spends ~52. Raise it to "medium"/"high" for
        # work that genuinely needs the extra thinking.
        #
        # .get() rather than [...] so a config.json written before this option
        # existed still loads instead of raising KeyError.
        return ChatGroq(
            model = config["groq"]["model"],
            temperature = config["groq"]["temperature"],
            max_tokens = config["groq"]["max_token"],
            reasoning_effort = config["groq"].get("reasoning_effort", "low"),
            api_key = os.getenv("GROQ_API_KEY")
        )
    else:
        raise ValueError(
            f"Unsupported provider: {provider}. "
            f"Expected one of: openai, gemini, anthropic, groq"
        )