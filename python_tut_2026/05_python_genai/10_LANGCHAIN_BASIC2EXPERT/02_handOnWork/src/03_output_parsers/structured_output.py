from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import _bootstrap  # noqa: F401  re-launches under myenv/ if python3 is the wrong one


from llm_client import get_llm
from utils.helpers import print_seperator, print_title

# JSON SCHEMA
movie_review_schema = {
    "title": "MovieReview",
    "description": "Schema for a moview review",
    "type":"object",
    "properties": {
        "movie_name": {
            "type": "string",
            "description": "Name of the movie."
        },
        "rating": {
            "type": "number",
            "description": "Rating out of 10."
        },
        "summary": {
            "type": "string",
            "description": "Short review of the movie."
        },
        "genres": {
            "type": "array",
            "items": {"type":"string"},
            "description": "List of movie genres."
        }
    },
    "required": ["movie_name", "rating" , "summary" , "genres"]
}

def main() -> None:
    """Demostrates structured output."""

    print_title("Structured Output")

    llm = get_llm().with_structured_output(movie_review_schema)

    response = llm.invoke(
        """
        Review the movie 'Interstellar'.

        Keep the summary under 60 words.
        """
    )

    print("Structured Response: \n")
    print(response)

    print_seperator()

    print("Accessing Invidual Fields:\n")

    print(f"Movie Name : {response['movie_name']}")
    print(f"Rating     : {response['rating']}")
    print(f"Genres     : {response['genres']}")
    print(f"Summary    : {response['summary']}")

if __name__ == "__main__":
    main()