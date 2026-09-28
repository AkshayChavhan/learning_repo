from llm_client import get_llm
from utils.helpers import print_title, print_seperator

def main():
    print_title("LangChain ChatBot Test")
    llm = get_llm()
    print(f"LLM Loaded Successfully: {llm.__class__.__name__}")
    print_seperator()
    print("Type 'exit' to uit. \n")

    while True:
        user_input = input("You: ")

        if user_input.lower() in ["exit", "quit"]:
            print("\nGoodbye!!")
            break

        response = llm.invoke(user_input)
        print(f"\nAI: {response.text}\n\n")

if __name__ == "__main__":
    main()