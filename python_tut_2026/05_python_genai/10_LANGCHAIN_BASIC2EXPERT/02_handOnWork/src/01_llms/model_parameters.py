from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from llm_client import get_llm
from utils.helpers import print_seperator, print_title

PARAMETER_DEMOS = [
    {
        "title": "Temperature",
        "description": (
            "Controls randomness. Lower values generate more deterministic responses, while higher"
        ),
        "params": { "temperature": 0.1},
        "prompt": "Suggest three AI startup ideas."
    },
    {
        "title": "Max Tokens",
        "description": (
            "Limits the maximum number of tokens the model can generate"
        ),
        "params": { "max_tokens": 50},
        "prompt": "Explain langchain in beginner friendly way."
    },
    {
        "title": "Top-P",
        "description": (
            "Controls nucleus sampling by selecting tokens from the most probable candidates."
        ),
        "params": { "top_p": 0.5},
        "prompt": "Suggest three AI startup ideas."
    },
    {
        "title": "Frequency Penalty",
        "description": (
            "Reduces repetitation by discouraging the model from using the same words repeatedly"
        ),
        "params": { "frequency_penalty": 1.2},
        "prompt": "Write a short paragraph about AI."
    },
    {
        "title": "Presence Penalty",
        "description": (
            "Encourages the model to introduce new ideas and vocab."
        ),
        "params": { "presence_penalty": 1.2},
        "prompt": "Suggest future technologies for smart cities."
    },
    {
        "title": "Stop Sequence",
        "description": (
            "Stop text generation when a specified sequence is encountered."
        ),
        "params": { "stop": ["4."]},
        "prompt": "List five popular programming languages as numbered list."
    },
]

def main() -> None:

    llm = get_llm()
    print_title("Common LLM Parameters")
    
    for demo in PARAMETER_DEMOS:
        print(demo["description"])

        response = llm.bind(**demo["params"]).invoke(demo["prompt"])

        print("\nResponse:\n")
        print(response.text)
        print_seperator()

if __name__ == "__main__":
    main()