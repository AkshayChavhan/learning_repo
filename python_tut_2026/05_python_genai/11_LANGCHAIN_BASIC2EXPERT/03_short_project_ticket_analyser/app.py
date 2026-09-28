import json
from pathlib import Path
import os
import sys

# Re-launch under myenv/ if this is the wrong interpreter. MUST come before the
# src imports below, which are what actually blow up on the repo-root .venv.
import _bootstrap  # noqa: E402,F401

from src.workflow import build_workflow, process_ticket
from src.llm import create_llm

PROJECT_ROOT = Path(__file__). resolve(). parent
INPUT_FILE = PROJECT_ROOT / "data" / "support_tickets.json"
OUTPUT_FILE = PROJECT_ROOT / "data" / "output"/ "support_ticket_analysis.json"

def load_tickets(file_path):
    path = Path(file_path)
    if not path.exists():
        print(f"Error: File not found: {path}")
        sys.exit(1)
    try:
        with open(path, "r" , encoding="utf-8") as file:
            tickets = json.load(file)
    except json.JSONDecodeError as error:
        print(f"Error: Invalid JSON in file: {path}: {error}")
        sys.exit(1)
    
    if not  isinstance(tickets, list) or not tickets:
        print(f"Error: Invalid tickets data in file: {path}: {tickets}")
        sys.exit(1)
    return tickets

def save_results(results , file_path):
    path = Path(file_path)
    path.parent.mkdir(parents= True    , exist_ok= True)

    # Convert pydantic models into plain dict for json  saving
    serializable = [
        result.model_dump() if hasattr(result, "model_dump") else result
        for result in results 
    ]

    with path.open("w", encoding="utf-8") as file:
        json.dump(serializable,file,indent=2, ensure_ascii=False) 
    return path

def main():
    print("="* 40)
    print("AI SUPPORT TICKET AUTOMATION")
    print("="* 40)
    print()

    # 1. Load Tickets
    tickets = load_tickets(INPUT_FILE)
    print(f"Loaded {len(tickets)} tickets from {INPUT_FILE.name}")
    print()

    # 2. Initialize LLM and build workflow once
    llm  = create_llm()
    workflow = build_workflow(llm)

    results = []

    #  3. Process each ticket one by one
    for ticket in tickets:
        ticket_id = ticket.get("ticket_id", "UNKNOWN")
        print(f"Processing ticket : {ticket_id}")

        try:
            result = process_ticket(ticket, workflow)
            results.append(result)
        except Exception as error:
            print(f"Error while processing ticket -> {ticket_id} : {error}")
            print()
            continue
        print()

    if not results:
        print("No tickets  were processed successfully.")
        sys.exit(1)

    # `results` (the accumulated list), not `result` (the last loop variable).
    output_path = save_results(results, OUTPUT_FILE)

    print("="*40)
    print("Processing Completed!!")
    print(f"{len(results)} of {len(tickets)} tickets processed")
    print("Results saved to :")
    print(output_path.as_posix())      # call it - otherwise this prints the method
    print("="*40)

if __name__ == "__main__":
    main()

