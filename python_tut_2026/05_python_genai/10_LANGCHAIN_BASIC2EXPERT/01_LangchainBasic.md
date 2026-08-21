# LangChain Components

## What is LangChain?

**LangChain** is an open-source framework designed to simplify the development of applications powered by **Large Language Models (LLMs)**.

It provides reusable components that help developers build LLM applications without having to handle everything from scratch.

LangChain helps with:

* Prompt management
* Conversation handling
* Document retrieval
* Structured outputs
* Memory management
* Tool calling
* RAG-based applications
* And many more LLM-related tasks

---

# Components of LangChain

Some of the commonly used LangChain components are:

### Core Components

* **LLMs**
* **Prompts**
* **Output Parsers**
* **Chains**
* **Memory**
* **Runnables**
* **Tool Calling**

### RAG Related Components

* **Retrieval**
* **Vector Stores**
* **Embeddings**
* **Text Splitters**
* **Document Loaders**

---

# 1. LLMs in LangChain

An **LLM (Large Language Model)** is the main component responsible for understanding the input and generating a response.

LangChain provides a common interface to work with different LLM providers.

For example:

* OpenAI
* Google Gemini
* Anthropic
* Local LLMs
* And others

### Example

![LLMs in LangChain](2.png)

The advantage is that application code can interact with different models through a consistent LangChain interface.

---

# 2. Prompts in LangChain

A **prompt** is the instruction or input given to an LLM.

LangChain provides components such as **Prompt Templates** to create reusable and dynamic prompts.

Instead of hardcoding the complete prompt every time, we can define a template and provide values dynamically.

### Example

![Prompts in LangChain](picture%201.png)

Prompt templates are useful when the same prompt structure needs to be reused with different inputs.

---

# 3. Output Parsers

LLMs normally return text.

Sometimes our application needs the response in a **specific format or structure**.

Output parsers help convert the LLM response into the required format.

For example, we may require:

* JSON
* List
* Specific fields
* Structured objects

### Example

If our application requires a predefined schema, the output parser can help ensure that the LLM response follows that expected structure.

> **Output Parsers are useful when we need a structured and predictable output from an LLM.**

---

# 4. Chains

A **Chain** connects multiple LangChain components together to perform a sequence of operations.

For example:

```text
User Input
    ↓
Prompt
    ↓
LLM
    ↓
Output Parser
    ↓
Final Output
```

### Example

![Chains in LangChain](picture%203.png)

LangChain supports different ways of combining operations, such as:

### Sequential / Linear Chain

Operations execute one after another.

```text
Input → Step 1 → Step 2 → Step 3 → Output
```

### Parallel Chain

Multiple operations can execute independently or in parallel.

```text
             → Step 1 →
Input →                  → Final Output
             → Step 2 →
```

Chains are useful when an application requires multiple steps to produce the final result.

---

# 5. Runnables

**Runnables** are standard building blocks in LangChain that allow us to compose and execute different components.

Many LangChain components can work together through the Runnable interface.

For example:

```text
Prompt → LLM → Output Parser
```

Each component can act as part of a larger Runnable sequence.

Runnables make it easier to **build, combine, and execute chains**.

---

# 6. Tools / Tool Calling

Tools allow an LLM to interact with **external functions or systems**.

Instead of only generating text, an LLM can decide when it needs to use a tool.

For example:

* Calculator
* Weather API
* Database
* Search API
* Custom application functions

### Example

![Tool Calling](4.png)

A typical flow can look like:

```text
User
  ↓
LLM
  ↓
Decides to use a tool
  ↓
Tool / API
  ↓
Tool Result
  ↓
LLM
  ↓
Final Response
```

Tool calling is useful when an LLM needs information or functionality that is not available through the model alone.

---

# 7. Memory

**Memory** allows an application to maintain information from previous interactions.

For example, in a chatbot:

```text
User: My name is Rahul.

Assistant: Nice to meet you, Rahul.

User: What is my name?

Assistant: Your name is Rahul.
```

Memory helps maintain context across conversations.

It is especially useful for:

* Chatbots
* Conversational applications
* Multi-turn interactions

---

# RAG Related Components

LangChain also provides components that are commonly used to build **RAG (Retrieval-Augmented Generation)** applications.

A basic RAG flow looks like:

```text
Documents
    ↓
Document Loader
    ↓
Text Splitter
    ↓
Embeddings
    ↓
Vector Store
    ↓
Retriever
    ↓
LLM
    ↓
Answer
```

The main components involved are:

### Document Loaders

Used to load data from sources such as:

* PDF files
* Text files
* Websites
* Documents
* Databases

### Text Splitters

Large documents are divided into smaller pieces called **chunks**.

This makes the documents easier to process and retrieve.

### Embeddings

Embeddings convert text into numerical representations called **vectors**.

These vectors help determine the semantic similarity between pieces of text.

### Vector Stores

Vector stores are used to store and search vector embeddings.

They allow us to find documents that are semantically similar to a user's query.

### Retrieval

Retrieval is the process of finding the most relevant information from the stored documents.

The retrieved information can then be provided to the LLM to generate a better answer.

---

# Overall LangChain Flow

The different components can be combined to build an LLM application:

```text
                    ┌──────────────┐
                    │    Prompt    │
                    └──────┬───────┘
                           ↓
┌──────────┐        ┌──────────────┐
│  Memory  │ ─────→  │     LLM      │
└──────────┘        └──────┬───────┘
                           ↓
                    ┌──────────────┐
                    │Output Parser │
                    └──────┬───────┘
                           ↓
                    ┌──────────────┐
                    │ Final Output │
                    └──────────────┘

Tools and RAG components can also be connected
to the application when required.
```

---

# Summary

LangChain provides a collection of reusable components for building applications powered by LLMs.

The important components covered here are:

| Component            | Purpose                                         |
| -------------------- | ----------------------------------------------- |
| **LLM**              | Generates responses                             |
| **Prompts**          | Defines instructions for the LLM                |
| **Output Parsers**   | Converts output into a required format          |
| **Chains**           | Connects multiple operations                    |
| **Runnables**        | Building blocks for composing operations        |
| **Tools**            | Allows LLMs to interact with external functions |
| **Memory**           | Maintains conversation context                  |
| **Document Loaders** | Loads documents                                 |
| **Text Splitters**   | Splits documents into smaller chunks            |
| **Embeddings**       | Converts text into vectors                      |
| **Vector Stores**    | Stores and searches vectors                     |
| **Retrieval**        | Finds relevant information                      |

Together, these components can be combined to build applications such as **chatbots, RAG systems, AI assistants, and other LLM-powered applications**.
