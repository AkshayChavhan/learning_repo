# LangChain Notes

Sample Markdown input. The header levels below are what
`MarkdownHeaderTextSplitter` splits on — each `#`, `##` and `###` becomes
chunk metadata rather than being thrown away.

## Core Components

### Models

A common chat interface over many providers. Swap OpenAI for Gemini, Anthropic
or a local Ollama model and everything downstream stays identical.

### Prompts

Reusable templates with dynamic variables. `PromptTemplate` for plain text,
`ChatPromptTemplate` for system/human/AI message structure.

### Output Parsers

Turn model text into structured Python objects. `with_structured_output()` is
preferred where the provider supports it; `PydanticOutputParser` is the
fallback that puts format instructions in the prompt instead.

## Runnables

Almost everything is a Runnable, so everything composes with the pipe operator.

```python
chain = prompt | model | parser
result = chain.invoke({"topic": "vector databases"})
```

### RunnableParallel

Runs several chains over the same input and collects the results as a dict.

### RunnableBranch

Routes to a different chain based on a condition. Takes `(condition, runnable)`
tuples, then one bare runnable as the default.

### RunnablePassthrough

Forwards its input unchanged. Use `.assign()` to add computed keys while
keeping the originals — the pattern RAG needs so the question survives
alongside the retrieved documents.

## Retrieval

### Document Loaders

Read source material into `Document` objects. `TextLoader`, `PyPDFLoader`,
`CSVLoader`, `WebBaseLoader` and `DirectoryLoader` all live in
`langchain-community`, not in `langchain` itself.

### Text Splitters

Cut documents into chunks. `RecursiveCharacterTextSplitter` is the usual
default; `MarkdownHeaderTextSplitter` preserves document structure by keeping
the header trail as metadata.

### Embeddings and Vector Stores

Embeddings map text to vectors positioned so similar meanings sit close
together. Vector stores index those vectors so the nearest chunks to a question
can be found quickly.

## Gotchas

| Gotcha | Detail |
|---|---|
| Loaders are not in `langchain` | They live in `langchain-community` |
| `WebBaseLoader` ignores 404s | Returns an empty `Document`, raises nothing |
| Parsers check shape, not truth | A valid object can hold invented values |
| Chunk size is a trade-off | Too large dilutes signal, too small loses context |
