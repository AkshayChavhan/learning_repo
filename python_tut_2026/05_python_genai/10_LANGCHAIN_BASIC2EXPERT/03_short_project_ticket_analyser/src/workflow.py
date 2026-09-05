from src.chains import (
    create_resolution_chain,
    create_response_chain,
    create_router,
    create_triage_chain,
)

from src.schemas import TicketResult

#Friendly labels used only for terminal display
CHAIN_LABELS = {
    "billing": "Billing Chain",
    "technical": "Technical Chain",
    "account": "Account Chain",
    "cancellation_refund": "Cancellation & Refund Chain",
    "general": "General Chain",
    "order_delivery": "Order Delivery Chain",
}

def build_workflow(llm):
    return {
        "triage_chain": create_triage_chain(llm),
        "router": create_router(llm),
        "resolution_chain": create_resolution_chain(llm),
        "response_chain": create_response_chain(llm),
    }

def process_ticket(ticket, workflow):
    """
    Run the full automation workflow for a single support ticket.

    Steps:
        1. Triage the ticket (category, priority, language)
        2. Route to a specialized analysis chain
        3. Decide the resolution
        4. Generate the customer response
        5. Return a final TicketResult

    Args:
        ticket (dict): One ticket with ticket_id, customer_name, and ticket.
        workflow (dict): Chains created by build_workflow().

    Returns:
        TicketResult: Final structured result for this ticket.

    Example:
        result = process_ticket(
            {
                "ticket_id": "TKT-1001",
                "customer_name": "Rahul Sharma",
                "ticket": "I was charged twice.",
            },
            workflow,
        )
        print(result.category, result.resolution_type)
    """

    # .get(...) with PARENTHESES. `ticket.get["customer_name"]` subscripts the
    # bound method object itself and raises TypeError.
    customer_name = ticket.get("customer_name")
    ticket_text = ticket.get("ticket")

    # Stage 1
    triage = workflow["triage_chain"].invoke(
        {
            "customer_name": customer_name,
            "ticket": ticket_text,
        }
    )
    # with_structured_output(TicketTriage) returns a pydantic MODEL, not a dict,
    # so read fields with attribute access - triage.get("category") raises.
    category = triage.category
    priority = triage.priority
    language = triage.language

    print("\nTriage Result:")
    print(f"Category: {category}")
    print(f"Priority: {priority}")
    # Single quotes inside the f-string expression: Python 3.11 does not allow
    # reusing the enclosing " inside {...}. PEP 701 lifted that only in 3.12.
    print(f"Routing  to: {CHAIN_LABELS.get(category, 'General Chain')}")


    # Stage 2 and 3 : Routing and Case Analysis
    # The key is "category" with NO trailing space - the RunnableBranch
    # conditions read x["category"], and "category " would KeyError.
    case_analysis = workflow["router"].invoke(
        {
            "category": category,
            "customer_name": customer_name,
            "ticket": ticket_text,
        }
    )

    # Convert analysis to text so later prompts stay simple and reusable
    case_analysis_text = case_analysis.model_dump_json(indent=2)

    # Stage  4 : Resolution Decision
    resolution = workflow["resolution_chain"].invoke(
        {
            "category": category,
            "customer_name": customer_name,
            "ticket": ticket_text,
            "priority": priority,
            "language": language,
            "case_analysis": case_analysis_text,
        }
    )

    print(f"\nResolution : {resolution.resolution_type}")
    print(f"Human Required: {'Yes' if resolution.requires_human else 'No'}")

    # Stage 5 : Customer Response
    # These keys must match the {placeholders} in prompts/response_prompt.txt.
    response = workflow["response_chain"].invoke(
        {
            "customer_name": customer_name,
            "ticket": ticket_text,
            "category": category,
            "priority": priority,
            "language": language,
            "case_analysis": case_analysis_text,
            "resolution_type": resolution.resolution_type,
            "recommended_action": resolution.recommended_action,
            "requires_human": resolution.requires_human,
            "resolution_reason": resolution.reason,
        }
    )

    # Stage 6 : Return the final result
    # response_chain ends in StrOutputParser(), so `response` is already a str.
    result = TicketResult(
        ticket_id=ticket.get("ticket_id"),
        customer_name=customer_name,
        category=category,
        priority=priority,
        language=language,
        case_summary=case_analysis_text,
        resolution_type=resolution.resolution_type,
        recommended_action=resolution.recommended_action,
        requires_human=resolution.requires_human,
        resolution_reason=resolution.reason,
        response=response.strip(),
    )

    print("\nFinal Result:")
    print(f"Category: {result.category}")
    print(f"Priority: {result.priority}")
    print(f"Resolution Type: {result.resolution_type}")
    print(f"Recommended Action: {result.recommended_action}")
    print(f"Human Required: {'Yes' if result.requires_human else 'No'}")
    print(f"Resolution Reason: {result.resolution_reason}")

    return result
