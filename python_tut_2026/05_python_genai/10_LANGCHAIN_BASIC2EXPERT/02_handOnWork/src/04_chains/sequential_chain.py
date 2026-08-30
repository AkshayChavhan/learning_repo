from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import _bootstrap  # noqa: F401  re-launches under myenv/ if python3 is the wrong one

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from llm_client import get_llm
from utils.helpers import print_seperator, print_title

def main():
    print_title("Sequential Chain")
    
    llm = get_llm()

    title_prompt = PromptTemplate.from_template(
        "Generate a catchy blog title about {topic} for Genz audience."
    )

    print(f"title_prompt: \n {title_prompt}")
 
    outline_prompt = PromptTemplate.from_template(
        """
        Create a blog outline for the following title.
            Title: {title}
            Target Group is Genz audience.
        """
    )
    print(f"outline_prompt: \n {outline_prompt}")

    title_chain = title_prompt | llm | StrOutputParser()
    outline_chain = outline_prompt | llm | StrOutputParser()

    topic = "Fat loss program"
    print(f"Topic: \n {topic}")

    print_seperator()

    title = title_chain.invoke({"topic" : topic})
    print(f"Generate title:\n {title}")
    print_seperator()

    outline = outline_chain.invoke({"title" : title})
    print(f"Generate outline:\n {outline}")
    print_seperator()


if __name__ == "__main__":
    main()