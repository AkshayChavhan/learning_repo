# Text generation with a small model (runs on CPU in ~1 second)
# This is the BEGINNER example — use this first to understand the pattern

from transformers import pipeline

# Load a small model (124M params, ~350 MB)
# GPT-2 is NOT gated, so no authentication needed
print("Loading model... (first time: downloads ~350 MB)")
pipe = pipeline("text-generation", model="gpt2")

# Generate text from a prompt
prompt = "The future of artificial intelligence is"
print(f"\nPrompt: {prompt}")
print("Generating...\n")

result = pipe(
    prompt,
    max_length=60,           # how long the output can be
    do_sample=True,          # random sampling (more creative)
    temperature=0.7,         # 0.0 = deterministic, 1.0+ = random
    num_return_sequences=1   # how many outputs to generate
)

# Extract the text
generated_text = result[0]["generated_text"]
print(f"Output:\n{generated_text}")
