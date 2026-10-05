"""Single place that builds the chat model every chain shares."""

import os
from pathlib import Path

from dotenv import load_dotenv

# .env sits at the project root, one level above src/. Resolve it from this
# file rather than the cwd, so `python app.py` and `python -m src.workflow`
# both find it.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / ".env")

# Which provider to use. OpenAI is what the architecture diagram calls for, but
# it is paid - a spent balance fails with:
#   429 ... 'code': 'credit_balance_exhausted'
# Groq is OpenAI-API-compatible and has a free tier, so switching provider is
# the only change needed; every chain downstream is identical.
_PROVIDERS = {
    "openai": ("OPENAI_API_KEY", "OPENAI_MODEL", "gpt-4.1-mini"),
    "groq": ("GROQ_API_KEY", "GROQ_MODEL", "openai/gpt-oss-120b"),
}


def create_llm():
    """Return the chat model used by every stage of the workflow.

    temperature=0 because this is a classification/extraction pipeline - we
    want the same ticket to produce the same category every run.
    """
    provider = os.getenv("LLM_PROVIDER", "openai").strip().lower()
    if provider not in _PROVIDERS:
        raise ValueError(
            f"Unsupported LLM_PROVIDER: {provider!r}. "
            f"Expected one of: {', '.join(_PROVIDERS)}"
        )

    key_var, model_var, default_model = _PROVIDERS[provider]
    api_key = os.getenv(key_var)
    if not api_key:
        raise RuntimeError(
            f"{key_var} is not set, but LLM_PROVIDER={provider}. "
            f"Copy .env.example to .env and fill it in."
        )

    model = os.getenv(model_var, default_model)

    if provider == "openai":
        from langchain_openai import ChatOpenAI

        return ChatOpenAI(model=model, temperature=0, api_key=api_key)

    from langchain_groq import ChatGroq

    # reasoning_effort="low": gpt-oss thinks before answering and that thinking
    # counts against the token budget. Low is plenty for classification.
    return ChatGroq(
        model=model,
        temperature=0,
        reasoning_effort="low",
        api_key=api_key,
    )


def with_schema(llm, schema):
    """Attach a structured-output schema, using the best method per provider.

    Groq's default `function_calling` path intermittently returns the JSON as
    plain assistant text instead of a tool call, and the API then rejects its
    own output:

        400 tool_use_failed - "Tool choice is required, but model did not call
        a tool"

    It happens on vague tickets, where the model has little to extract. Measured
    on "I have a technical issue.": function_calling 0/3, json_schema 3/3.
    `json_schema` uses Groq's native constrained decoding, so the shape is
    guaranteed rather than requested.
    """
    if llm.__class__.__name__ == "ChatGroq":
        structured = llm.with_structured_output(schema, method="json_schema")
    else:
        structured = llm.with_structured_output(schema)

    # gpt-oss is a REASONING model: now and then its chain-of-thought lands in
    # the output slot instead of the JSON, and Groq rejects its own generation
    # with 400 output_parse_failed. It is stochastic, not deterministic - the
    # same ticket that failed 1/17 in one run passed 5/5 on re-run - so one
    # retry turns a dropped ticket into a slightly slower one.
    return structured.with_retry(stop_after_attempt=3)
