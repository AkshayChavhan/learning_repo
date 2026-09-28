from typing import Literal
from pydantic import BaseModel, Field 


# Allowed values used across triage and resolution stages

Category = Literal[
    "billing",
    "technical",
    "account",
    "cancellation_refund",
    "order_delivery",
    "general",
]

Priority = Literal[
    "low",
    "medium",
    "high",
    "critical",
] 

ResolutionType = Literal[
    "self_service",
    "resolve",
    "escalate",
    "request_information",
]

class TicketTriage(BaseModel):
    category: Category = Field(description="The category of the ticket")
    priority: Priority = Field(description="The priority of the ticket")
    language: str = Field(description="The language of the ticket")

class BillingAnalysis(BaseModel):
    issue: str = Field(description="The issue with the billing")
    amount: str = Field(description="The amount of the billing")
    transaction_count: int = Field(description="The number of charges mentioned.")
    refund_requested: bool = Field(description="Whether the user has requested a refund.")

class TechnicalAnalysis(BaseModel):
    issue: str = Field(description="The issue with the technical support")
    affected_features: str = Field(description="The features that are affected by the issue")
    error_message: str = Field(description="The error message from the technical support")
    troubleshooting_required: bool = Field(description="Whether the user needs troubleshooting")

class AccountAnalysis(BaseModel):
    issue: str = Field(description="The issue with the account")
    access_problem: bool = Field(description="Whether the user has access problem")
    verification_required: bool = Field(description="Whether the user needs verification")
    account_status: str = Field(description="The status of the account")

class CancellationRefundAnalysis(BaseModel):
    request_type: str = Field(description="The type of the request")
    reason: str = Field(description="The reason for the request")
    refund_required: bool = Field(description="Whether the user needs a refund")
    retention_opportunity: bool = Field(description="Whether the user is a retention opportunity")

class OrderDeliveryAnalysis(BaseModel):
    issue: str = Field(description="The issue with the order delivery")
    order_status: str = Field(description="The status of the order")
    delivery_problem: bool = Field(description="Whether the user has a delivery problem")
    customer_request: str = Field(description="The customer request")

class GeneralAnalysis(BaseModel):
    issue: str = Field(description="The issue with the ticket")
    customer_request: str = Field(description="The customer request")
    additional_context: str = Field(description="Additional context about the ticket")

class ResolutionDecision(BaseModel):
    resolution_type: ResolutionType = Field(description="The resolution type")
    recommended_action: str = Field(description="The recommended actions")
    requires_human: bool = Field(description="Whether the resolution requires human intervention")
    reason: str = Field(description="The reason for the resolution decision")

class TicketResult(BaseModel):
    ticket_id: str
    customer_name: str
    category: str
    priority: str
    language: str
    case_summary: str
    resolution_type: str
    recommended_action: str
    requires_human: bool
    resolution_reason: str
    response: str
