"""
Google Gemini API - Complete Learning Guide
============================================

This file demonstrates 8 core concepts of using Google Gemini (GenAI) in Python:
  1. Basic text generation
  2. Chat conversations (with history)
  3. System prompts (role-based instructions)
  4. Configuration (temperature, max_tokens)
  5. Structured output (JSON responses)
  6. Streaming (real-time response chunks)
  7. Token counting (understanding API costs)
  8. Error handling (handling blocked content)

Key Concept: Gemini's chat object keeps the conversation history for you.
Compare to OpenAI (stateless) - there you manage the message list yourself.

Setup:
  1. pip install google-genai      (the NEW SDK; google-generativeai is retired)
  2. Get free API key: https://aistudio.google.com/
  3. Set env var: $env:GEMINI_API_KEY = "your-key"   (PowerShell)
                  export GEMINI_API_KEY="your-key"   (bash)
"""

# ═════════════════════════════════════════════════════════════════════════════
# SSL FIX - required on this machine because Avast intercepts HTTPS
# ═════════════════════════════════════════════════════════════════════════════
# Avast Antivirus "Web/Mail Shield" acts as a man-in-the-middle: it decrypts
# every HTTPS connection and re-signs it with its own root certificate.
#
# Chrome trusts that root because it reads the Windows certificate store.
# Python does NOT read the Windows store - it ships its own bundle (certifi),
# which has never heard of Avast. Hence: CERTIFICATE_VERIFY_FAILED.
#
# Two things are needed:
#   1. A CA bundle = certifi + the Avast root  (built into ~/.certs/ca-bundle.pem)
#   2. Turning OFF the VERIFY_X509_STRICT flag. Python 3.13+ enables it by
#      default, and it rejects Avast's root because Avast marks the
#      "BasicConstraints" extension non-critical, which RFC 5280 forbids.
#
# Chain verification and hostname checking stay fully ON. We only relax the
# one RFC-conformance nitpick that Avast violates.
#
# The permanent alternative: Avast > Menu > Settings > Protection >
# Core Shields > Web Shield > uncheck "Enable HTTPS scanning". Then delete
# this whole block.
import os
import ssl

_CA_BUNDLE = os.path.expanduser(r"~\.certs\ca-bundle.pem")

if os.path.exists(_CA_BUNDLE):
    os.environ.setdefault("SSL_CERT_FILE", _CA_BUNDLE)
    _original_context = ssl.create_default_context

    def _context_with_avast_root(*args, **kwargs):
        kwargs.setdefault("cafile", _CA_BUNDLE)
        context = _original_context(*args, **kwargs)
        context.verify_flags &= ~ssl.VERIFY_X509_STRICT
        return context

    ssl.create_default_context = _context_with_avast_root
# ═════════════════════════════════════════════════════════════════════════════

import json
import logging

from google import genai
from google.genai import errors, types

# The SDK logs a chatty "automatic function calling" notice on every call.
# We are not using function calling, so quiet it down.
logging.getLogger("google_genai").setLevel(logging.ERROR)

# Load API key from environment variable
# Environment vars are a secure way to store secrets (don't hardcode them!)
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError(
        "GEMINI_API_KEY not found! Set it via: $env:GEMINI_API_KEY = 'your-key'"
    )

# The client object holds your credentials. Create it once, reuse everywhere.
#
# retry_options: popular models get overloaded and return 503 UNAVAILABLE.
# That is temporary and not your bug, so retry with exponential backoff:
# wait 1s, then 2s, then 4s... up to 5 attempts. Without this, a busy moment
# on Google's side crashes your script.
client = genai.Client(
    api_key=API_KEY,
    http_options=types.HttpOptions(
        retry_options=types.HttpRetryOptions(
            attempts=5,
            initial_delay=1.0,
            max_delay=30.0,
            exp_base=2.0,
            http_status_codes=[429, 500, 502, 503, 504],
        ),
    ),
)

# Which Gemini model to use
#   "gemini-3.1-flash-lite"  cheapest + highest free-tier quota (used here)
#   "gemini-3.6-flash"       stronger answers, smaller free quota
#   "gemini-3.1-pro-preview" most capable, smallest free quota
#
# QUOTA WARNING: the free tier allows only ~20 requests per day PER MODEL.
# One full run of this file makes ~9 calls, so you get about 2 runs per day
# before a 429 RESOURCE_EXHAUSTED. The quota is per model, so switching the
# line below to another model gives you a fresh bucket.
#
# Tip: "gemini-flash-latest" / "gemini-flash-lite-latest" are aliases that
# always point at the current model, so they never break when Google retires
# a version number. List what your key can access with: client.models.list()
MODEL = "gemini-3.1-flash-lite"


def basic_text_generation():
    """
    Example 1: BASIC TEXT GENERATION

    The simplest way to use Gemini:
    1. Call client.models.generate_content() with a model + prompt
    2. Read response.text

    Mental model: You send text in -> the model processes it -> text comes out.
    No conversation history, no system instructions. One request, one response.
    """
    print("=" * 60)
    print("1. BASIC TEXT GENERATION")
    print("=" * 60)

    # `contents` is your prompt. `model` picks which Gemini to talk to.
    response = client.models.generate_content(
        model=MODEL,
        contents="Write a one-line Python joke",
    )

    # response.text is the convenience accessor for the generated string
    print("Prompt: Write a one-line Python joke")
    print(f"Response:\n{response.text}")
    print()


def chat_conversation():
    """
    Example 2: CHAT CONVERSATIONS

    Unlike basic_text_generation(), a chat keeps conversation history, so the
    model remembers what was said earlier.

    How it works:
    1. client.chats.create() makes a chat session
    2. chat.send_message() appends to the history and gets a reply

    ADVANTAGE: History is managed for you
    DISADVANTAGE: Stateful, so harder to test and parallelize
    """
    print("=" * 60)
    print("2. CHAT CONVERSATION (Multi-turn)")
    print("=" * 60)

    chat = client.chats.create(model=MODEL)

    # Turn 1 - a plain question
    print("Turn 1:")
    response1 = chat.send_message("What's 2+2?")
    print("  User: What's 2+2?")
    print(f"  Bot: {response1.text}")
    print()

    # Turn 2 - "that number" only makes sense if the history was kept
    print("Turn 2:")
    response2 = chat.send_message("Double that number")
    print("  User: Double that number")
    print(f"  Bot: {response2.text}")
    print("  (Notice: the model resolved 'that number' to 4 from turn 1)")
    print()


def system_prompt():
    """
    Example 3: SYSTEM PROMPT (Role-based instructions)

    A system prompt tells the model HOW to behave - its role and tone.

    Use cases:
    - Customer support bot: "You are a helpful customer service agent"
    - Code reviewer: "You are an expert Python code reviewer"
    - Teacher: "Explain concepts simply for beginners"

    In Gemini it goes in config.system_instruction.
    In OpenAI it's the first message with role="system".
    """
    print("=" * 60)
    print("3. SYSTEM PROMPT (Role-based instruction)")
    print("=" * 60)

    response = client.models.generate_content(
        model=MODEL,
        contents="What is a decorator in Python?",
        config=types.GenerateContentConfig(
            system_instruction=(
                "You are a helpful Python tutor. "
                "Explain concepts briefly and with examples."
            ),
        ),
    )

    print("System Prompt: You are a helpful Python tutor")
    print("User Question: What is a decorator in Python?")
    print(f"Response:\n{response.text}")
    print()


def with_config():
    """
    Example 4: CONFIGURATION (Temperature, Max Tokens)

    Key parameters:
    - temperature: 0.0-2.0 (lower = deterministic, higher = creative/random)
      - 0.0: Always the same output (good for facts, extraction)
      - 0.5: Balanced (default for most tasks)
      - 1.0+: Creative, unpredictable (good for story writing)

    - max_output_tokens: Maximum length of the response
      - Protects against long, expensive responses

    - thinking_level: how much internal reasoning the model does ("low"/"high")
      GOTCHA: on Gemini 3 models, thinking tokens are billed against
      max_output_tokens. Leave thinking high with a small max_output_tokens
      and the model burns the whole budget reasoning, so your visible answer
      arrives truncated mid-sentence. thinking_level="low" leaves room for
      the answer you actually want to see.
      (Gemini 3 also rejects thinking_budget=0 - it cannot be turned off.)

    Why this matters:
    - Cost control: shorter responses = lower API bills
    - Quality control: low temp for facts, high temp for creativity
    """
    print("=" * 60)
    print("4. CONFIGURATION (Temperature & Max Tokens)")
    print("=" * 60)

    response = client.models.generate_content(
        model=MODEL,
        contents="Generate a creative story opening",
        config=types.GenerateContentConfig(
            temperature=0.9,         # High temp = creative, unpredictable
            max_output_tokens=1200,  # Must cover thinking + the answer
            thinking_config=types.ThinkingConfig(thinking_level="low"),
        ),
    )

    print("Config: temperature=0.9, max_output_tokens=1200, thinking_level=low")
    print("Prompt: Generate a creative story opening")
    print(f"Response:\n{response.text}")

    # Proof of the gotcha above: see how much of the budget thinking ate.
    # If finish_reason is MAX_TOKENS, the answer was cut off - raise the cap.
    usage = response.usage_metadata
    print(
        f"\nToken budget: {usage.thoughts_token_count} thinking "
        f"+ {usage.candidates_token_count} answer = "
        f"{usage.thoughts_token_count + usage.candidates_token_count} / 1200"
    )
    print(f"Finish reason: {response.candidates[0].finish_reason.name}")
    print()


def structured_output():
    """
    Example 5: STRUCTURED OUTPUT (JSON Responses)

    Sometimes you don't want prose - you want data your code can use.

    How it works:
    1. Set response_mime_type to "application/json"
    2. Provide a response_schema describing the shape you want
    3. Gemini returns JSON matching that schema

    Useful for:
    - Data extraction (pull fields out of free text)
    - Feeding a backend that expects JSON
    - Validation (the schema enforces the format)
    """
    print("=" * 60)
    print("5. STRUCTURED OUTPUT (JSON Response)")
    print("=" * 60)

    response = client.models.generate_content(
        model=MODEL,
        contents="Extract name and age from: 'Alice is 28 years old'",
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema={
                "type": "object",
                "properties": {
                    "name": {"type": "string"},   # Must be a string
                    "age": {"type": "integer"},   # Must be an integer
                },
                "required": ["name", "age"],
            },
        ),
    )

    # The response is JSON text, so parse it into a real Python dict
    data = json.loads(response.text)
    print("Prompt: Extract name and age from: 'Alice is 28 years old'")
    print("Requested format: JSON with 'name' (string) and 'age' (integer)")
    print(f"Response:\n{json.dumps(data, indent=2)}")
    print(f"Parsed as Python: name={data['name']!r}, age={data['age']!r}")
    print()


def streaming():
    """
    Example 6: STREAMING (Real-time Response Chunks)

    generate_content() waits for the WHOLE response before returning.
    generate_content_stream() yields chunks as they are produced.

    Benefits:
    - Faster perceived response (text appears immediately)
    - Lower memory use (no need to hold the full response)
    - Much better UX for chatbots

    Trade-off:
    - Final metadata (like finish_reason) only arrives at the end
    """
    print("=" * 60)
    print("6. STREAMING (Real-time Response Chunks)")
    print("=" * 60)

    print("Prompt: List 3 Python tips")
    print("Response (streamed):")

    stream = client.models.generate_content_stream(
        model=MODEL,
        contents="List 3 Python tips",
    )

    for chunk in stream:
        # Some chunks carry only metadata, so text can be None
        if chunk.text:
            print(chunk.text, end="", flush=True)

    print("\n")


def token_counting():
    """
    Example 7: TOKEN COUNTING

    Tokens are "pieces" of text. The API bills per 1M tokens.
    Counting them helps you:
    1. Estimate cost before making an expensive call
    2. Stay under rate limits
    3. Stay under the model's context window

    Gemini has count_tokens() built in.
    (OpenAI needs the external 'tiktoken' library for this.)

    Rough rule of thumb:
    - 1 token is about 4 English characters
    - 1 token is about 0.75 English words
    """
    print("=" * 60)
    print("7. TOKEN COUNTING (API Cost Estimation)")
    print("=" * 60)

    text = "How many tokens does this sentence have?"
    response = client.models.count_tokens(model=MODEL, contents=text)

    print(f"Text: '{text}'")
    print(f"Character count: {len(text)}")
    print(f"Actual token count: {response.total_tokens}")
    print(f"Rule of thumb estimate: {len(text) // 4} tokens")
    print()


def error_handling():
    """
    Example 8: ERROR HANDLING

    APIs fail. Networks drop, quotas run out, safety filters block content.
    Handle it instead of crashing.

    Common google.genai errors:
    - errors.ClientError  -> 4xx: bad key, bad request, quota exceeded
    - errors.ServerError  -> 5xx: Google-side problem, worth retrying
    - errors.APIError     -> the parent class of both

    Best practice: catch the specific ones first, generic Exception last.
    """
    print("=" * 60)
    print("8. ERROR HANDLING (Catching Exceptions)")
    print("=" * 60)

    try:
        response = client.models.generate_content(
            model=MODEL,
            contents="Explain quantum physics in detail",
        )
        print("Status: Success")
        print(f"Response (first 150 chars):\n{response.text[:150]}...")

    except errors.ClientError as e:
        # Your fault: bad API key, malformed request, quota exceeded
        print("Status: Client error (4xx)")
        print(f"Error: {e}")

    except errors.ServerError as e:
        # Google's fault: retrying later usually helps
        print("Status: Server error (5xx)")
        print(f"Error: {e}")

    except Exception as e:
        # Anything else: network, SSL, parsing
        print("Status: Unexpected error")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {e}")

    print()


# ============================================================================
# MAIN - Run all examples
# ============================================================================

if __name__ == "__main__":
    """
    Runs all 8 examples in sequence.
    Each function is independent - comment any out to skip it.
    """
    print("\n")
    print("+" + "=" * 58 + "+")
    print("|" + "  GOOGLE GEMINI API - COMPLETE LEARNING GUIDE".center(58) + "|")
    print("+" + "=" * 58 + "+")
    print("\n")

    basic_text_generation()
    chat_conversation()
    system_prompt()
    with_config()
    structured_output()
    streaming()
    token_counting()
    error_handling()

    print("=" * 60)
    print("ALL EXAMPLES COMPLETED!")
    print("=" * 60)
    print("\nNext steps:")
    print("  1. Try modifying the prompts to see different responses")
    print("  2. Experiment with different temperatures (0.0 vs 1.0)")
    print("  3. Compare with llm_chatgpt.py to see OpenAI's approach")
    print("  4. Build a chatbot combining chat_conversation() + error_handling()")
