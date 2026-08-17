"""
OpenAI ChatGPT API - Complete Learning Guide
=============================================

This file demonstrates 8 core concepts of using OpenAI ChatGPT in Python:
  1. Basic text generation
  2. Chat conversations (with history)
  3. System prompts (role-based instructions)
  4. Configuration (temperature, max_tokens)
  5. Structured output (JSON responses)
  6. Streaming (real-time response chunks)
  7. Token counting (understanding API costs)
  8. Error handling (handling API errors)

Key Concept: OpenAI uses a STATELESS API. YOU manage conversation history.
Compare to Gemini (stateful) - the server keeps track of history.

Setup:
  1. pip install openai tiktoken
  2. Get API key: https://platform.openai.com/api/keys (needs payment)
  3. Set env var: $env:OPENAI_API_KEY = "your-key"

Cost comparison:
  - Gemini free tier: 100-1500 requests/day
  - OpenAI: Paid, starts with $5 free trial credits
"""

from openai import OpenAI
import os
import json
import tiktoken

# Load API key from environment variable
# Environment vars are a secure way to store secrets (don't hardcode them!)
API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    raise ValueError(
        "OPENAI_API_KEY not found! Set it via: $env:OPENAI_API_KEY = 'your-key'"
    )

# Create an OpenAI client object
# Unlike Gemini's global configure(), each client is independent
# This lets you use multiple API keys simultaneously if needed
client = OpenAI(api_key=API_KEY)

# Which model to use
# Options: "gpt-4o" (most capable, most expensive)
#          "gpt-4o-mini" (cheaper, good for learning)
#          "gpt-4" (older, less capable, still expensive)
MODEL = "gpt-4o-mini"


def basic_text_generation():
    """
    Example 1: BASIC TEXT GENERATION

    The simplest way to use OpenAI:
    1. Create a client
    2. Call client.messages.create() with a message list
    3. Extract the response text

    Key difference from Gemini:
    - OpenAI uses "messages" (list of dicts with role + content)
    - You must pass messages as a list, even for a single prompt
    - Response is nested: response.content[0].text (not just response.text)

    Mental model: Send a list of messages → model processes them → response object back
    """
    print("=" * 60)
    print("1. BASIC TEXT GENERATION")
    print("=" * 60)

    # Step 1: Create a message list
    # In OpenAI, everything is a message with a role and content
    # Roles: "user" (you), "assistant" (model), "system" (instructions)
    messages = [{"role": "user", "content": "Write a one-line Python joke"}]

    # Step 2: Send the message and get a response
    # messages.create() is the main method (not generate_content like Gemini)
    response = client.messages.create(model=MODEL, messages=messages)

    # Step 3: Extract the text from the response
    # response.content is a list, so we take [0] and then .text
    # (Gemini just uses response.text directly)
    print(f"Prompt: Write a one-line Python joke")
    print(f"Response:\n{response.content[0].text}")
    print()


def chat_conversation():
    """
    Example 2: CHAT CONVERSATIONS

    OpenAI keeps conversations STATELESS - YOU manage the history.
    For each new message, you must pass the entire conversation history.

    How it works (OpenAI's stateless approach):
    1. Create a messages list
    2. Add the first user message
    3. Get the assistant's response and add it to the list
    4. Add the next user message
    5. Send the full list to get the next response

    ADVANTAGE: Full control, deterministic, easy to test
    DISADVANTAGE: More work to manage history, costs more (re-send old messages)

    This is different from Gemini's chat.start_chat() which handles it server-side.
    """
    print("=" * 60)
    print("2. CHAT CONVERSATION (Multi-turn)")
    print("=" * 60)

    # Step 1: Start with empty messages list
    # This is how you maintain "state" in OpenAI - manually
    messages = []

    # Step 2: First exchange
    print("Turn 1:")
    user_msg1 = "What's 2+2?"
    # Add user message to history
    messages.append({"role": "user", "content": user_msg1})

    # Get response
    response1 = client.messages.create(model=MODEL, messages=messages)
    assistant_reply1 = response1.content[0].text

    print(f"  User: {user_msg1}")
    print(f"  Bot: {assistant_reply1}")
    print()

    # Step 3: Second exchange
    print("Turn 2:")
    # Add assistant's response to history (important!)
    messages.append({"role": "assistant", "content": assistant_reply1})

    user_msg2 = "Double that number"
    # Add new user message
    messages.append({"role": "user", "content": user_msg2})

    # Get response - pass ALL messages (full history)
    # This is why OpenAI is stateless - you control everything
    response2 = client.messages.create(model=MODEL, messages=messages)

    print(f"  User: {user_msg2}")
    print(f"  Bot: {response2.content[0].text}")
    print(
        f"  (Notice: The model understood 'that number' refers to 4 because we sent the full history)"
    )
    print()


def system_prompt():
    """
    Example 3: SYSTEM PROMPT (Role-based instructions)

    In OpenAI, the system prompt is just the first message with role="system".
    You pass it alongside other messages.

    Use cases:
    - Customer support bot: "You are a helpful customer service agent"
    - Code reviewer: "You are an expert Python code reviewer"
    - Teacher: "Explain concepts simply for beginners"

    Key difference from Gemini:
    - Gemini: system_instruction parameter in model init
    - OpenAI: First message in the messages list with role="system"
    """
    print("=" * 60)
    print("3. SYSTEM PROMPT (Role-based instruction)")
    print("=" * 60)

    # Step 1: Create messages list with system prompt as first message
    messages = [
        # System message sets the context/role
        {
            "role": "system",
            "content": "You are a helpful Python tutor. Explain concepts briefly and with examples.",
        },
        # User question comes after
        {"role": "user", "content": "What is a decorator in Python?"},
    ]

    # Step 2: Send all messages together
    # OpenAI will use the system message to guide its behavior
    response = client.messages.create(model=MODEL, messages=messages)

    print("System Prompt: You are a helpful Python tutor")
    print(f"User Question: What is a decorator in Python?")
    print(f"Response:\n{response.content[0].text}")
    print()


def with_config():
    """
    Example 4: CONFIGURATION (Temperature, Max Tokens)

    You can control model behavior with parameters to messages.create().

    Key parameters:
    - temperature: 0.0-2.0 (lower = deterministic, higher = creative)
      • 0.0: Always same output (e.g., "2+2=4")
      • 0.5: Balanced (good for most tasks)
      • 1.0+: Creative, unpredictable (e.g., story writing)

    - max_tokens: Maximum length of response
      • Protects against long, expensive responses
      • E.g., max_tokens=100 limits to ~100 words

    Key difference from Gemini:
    - Gemini: Uses generation_config with GenerationConfig object
    - OpenAI: Direct kwargs (simpler!)

    Why this matters:
    - Cost control: Shorter responses = lower bills
    - Behavior control: Lower temp for facts, higher temp for creativity
    """
    print("=" * 60)
    print("4. CONFIGURATION (Temperature & Max Tokens)")
    print("=" * 60)

    # Step 1: Pass config directly as kwargs (much simpler than Gemini!)
    response = client.messages.create(
        model=MODEL,
        messages=[{"role": "user", "content": "Generate a creative story opening"}],
        temperature=0.9,  # High temp = creative
        max_tokens=100,  # Limit to ~100 words
    )

    print(
        "Config: temperature=0.9 (creative), max_tokens=100 (short response)"
    )
    print(f"Prompt: Generate a creative story opening")
    print(f"Response:\n{response.content[0].text}")
    print()


def structured_output():
    """
    Example 5: STRUCTURED OUTPUT (JSON Responses)

    Sometimes you need data in a specific format (JSON), not just text.
    E.g., extract name/age, or get a list of suggestions.

    How it works:
    1. Set response_format to {"type": "json_object"}
    2. Ask the model to return JSON in your prompt
    3. Parse the response as JSON

    Key difference from Gemini:
    - Gemini: response_mime_type + response_schema (more rigid)
    - OpenAI: response_format flag (simpler, but you must ask for JSON in prompt)

    Trade-off:
    - Gemini: Schema enforcement (guaranteed format)
    - OpenAI: Flexibility (model decides structure, but simpler setup)
    """
    print("=" * 60)
    print("5. STRUCTURED OUTPUT (JSON Response)")
    print("=" * 60)

    # Step 1: Set response_format to json_object
    response = client.messages.create(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": "Extract name and age from: 'Alice is 28 years old'. Return as JSON with 'name' and 'age' keys.",
            }
        ],
        response_format={"type": "json_object"},  # Much simpler than Gemini!
    )

    # Step 2: Parse the JSON response
    data = json.loads(response.content[0].text)
    print("Prompt: Extract name and age from: 'Alice is 28 years old'")
    print("Requested format: JSON with 'name' and 'age' keys")
    print(f"Response:\n{json.dumps(data, indent=2)}")
    print()


def streaming():
    """
    Example 6: STREAMING (Real-time Response Chunks)

    By default, messages.create() waits for the ENTIRE response.
    With streaming, you get chunks of text as they're generated.

    Benefits:
    - Faster perceived response (text appears immediately)
    - Lower memory usage (don't hold entire response)
    - Better for interactive chatbots

    Key difference from Gemini:
    - Gemini: Pass stream=True flag
    - OpenAI: Use client.messages.stream() context manager (more Pythonic)
    """
    print("=" * 60)
    print("6. STREAMING (Real-time Response Chunks)")
    print("=" * 60)

    print("Prompt: List 3 Python tips")
    print("Response (streamed):")

    # Step 1: Use messages.stream() context manager
    # This is more Pythonic than Gemini's stream=True flag
    with client.messages.stream(
        model=MODEL,
        messages=[{"role": "user", "content": "List 3 Python tips"}],
        max_tokens=100,
    ) as stream:
        # Step 2: Iterate over text chunks as they arrive
        for text in stream.text_stream:
            print(text, end="", flush=True)

    print("\n")  # New line after streaming


def token_counting():
    """
    Example 7: TOKEN COUNTING

    Tokens are "pieces" of text. OpenAI charges per 1M input tokens + output tokens.
    Understanding token counts helps you:
    1. Estimate costs before making expensive calls
    2. Stay under rate limits
    3. Understand model context limits (e.g., 128k token limit for gpt-4o)

    OpenAI makes you use an external library: tiktoken
    (Gemini has it built-in: model.count_tokens())

    Rough rule of thumb:
    - 1 token ≈ 4 English characters
    - 1 token ≈ 0.75 English words
    """
    print("=" * 60)
    print("7. TOKEN COUNTING (API Cost Estimation)")
    print("=" * 60)

    # Step 1: Get the encoding for the model
    # tiktoken is a separate library (external, unlike Gemini's built-in)
    encoding = tiktoken.encoding_for_model(MODEL)

    # Step 2: Encode text to tokens
    text = "How many tokens does this sentence have?"
    tokens = encoding.encode(text)

    print(f"Text: '{text}'")
    print(f"Token count: {len(tokens)}")
    print(f"Rough estimation: {len(text)} chars ≈ {len(tokens)} tokens")
    print()


def error_handling():
    """
    Example 8: ERROR HANDLING

    APIs can fail for many reasons:
    - Rate limit exceeded (too many requests)
    - Invalid API key
    - Network timeout
    - Bad input (invalid model name)

    Common OpenAI exceptions:
    - RateLimitError: Too many requests
    - APIError: Server error
    - AuthenticationError: Invalid API key
    - InvalidRequestError: Bad input

    Best practice: Wrap API calls in try/except blocks.
    """
    print("=" * 60)
    print("8. ERROR HANDLING (Catching Exceptions)")
    print("=" * 60)

    try:
        # Make an API call
        response = client.messages.create(
            model=MODEL,
            messages=[
                {"role": "user", "content": "Explain quantum physics in detail"}
            ],
            max_tokens=50,
        )

        print("Status: Success ✓")
        print(f"Response (first 150 chars):\n{response.content[0].text[:150]}...")

    except Exception as e:
        # Catch all OpenAI exceptions
        # (You could also catch specific ones like RateLimitError)
        print(f"Status: Error ✗")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {e}")

    print()


# ============================================================================
# MAIN - Run all examples
# ============================================================================

if __name__ == "__main__":
    """
    This runs all 8 examples in sequence.
    Each function is independent - you can comment out any to skip it.
    """
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + "  OPENAI CHATGPT API - COMPLETE LEARNING GUIDE".center(58) + "║")
    print("╚" + "=" * 58 + "╝")
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
    print("  3. Compare with llm_gemini.py to see Gemini's approach")
    print("  4. Notice differences: stateless vs stateful, config style, token counting")
    print("  5. Build a chatbot using the chat_conversation() pattern")
