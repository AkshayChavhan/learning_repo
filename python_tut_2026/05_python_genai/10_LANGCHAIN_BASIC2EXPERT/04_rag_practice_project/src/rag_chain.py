import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

from src.schemas import RAGResponse , SourceCitation
from src.vectorstore import format_docs, get_retriever , load_vectorstore


load_dotenv()

DEFAULT_PROMPT_PATH = Path("prompts/rag_prompt.txt")
DEFAULT_CHAT_MODEL = "models/gemini-3.6-flash"

def load_rag_prompt( prompt_path: str | Path = DEFAULT_PROMPT_PATH) -> PromptTemplate :
    path = Path(prompt_path)
    if not path.exists():
        raise FileNotFoundError(f"RAG prompt file not found : {path}")

    template_text = path.read_text(encoding="utf-8")
    return PromptTemplate(
        template = template_text,
        input_variables=["context" , "chat_history" , "question"],
    )

def get_llm() -> ChatGoogleGenerativeAI:
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY is missing. Add it to your .env file")

    model_name = os.getenv("GEMINI_CHAT_MODEL", DEFAULT_CHAT_MODEL)

    try:
        return ChatGoogleGenerativeAI(
            model = model_name,
            google_api_key=api_key,
            temperature = 0,
        )
    except Exception as e:
        raise RuntimeError(
            "Could not create the Gemini chat client. "
            "Check GOOGLE_API_KEY and GEMINI_CHAT_MODEL in your .env file"
        ) from e

def get_llm_display_name() -> str:
    model_name = os.getenv("GEMINI_CHAT_MODEL" , DEFAULT_CHAT_MODEL)
    return f"Google / {model_name}"

def format_chat_history(messages: list[dict]) -> str:
    if not messages:
        return "No previous conversation"

    lines = []
    for msg in messages:
        role = msg.get("role", "user")
        content = msg.get("content","").strip()
        if not content:
            continue
        label = "User" if role == "user" else "Assistant"
        lines.append(f"{label}: {content}")
    return "\n".join(lines) if lines else "No previous conversation."

def extract_sources(docs: list[Document]) -> list[SourceCitation] :
    citations: list[SourceCitation] = []
    seen: set[tuple[str,int | None]] = set()

    for doc in docs:
        filename = doc.metadata.get("filename") or doc.metadata.get("source", "unknown")
        page = doc.metadata.get("page")
        key = (str(filename) , page)

        if key in seen :
            continue
        seen.add(key)

        preview = doc.page_content.strip().replace("\n" , " ")
        if len(preview) > 160:
            preview = preview[:157] + "..."

        citations.append(
            SourceCitation(
                filename=filename,
                page=page,
                preview=preview
            )
        )

    return citations


def ask_question(
    question:str,
    chat_history: list[dict] | None = None,
    k: int | None = None
) -> RAGResponse:
    """
    Run one conversational RAG turn and return an answer with sources.

    ### Steps
    1. **Load the FAISS knowledge base**
    2. Retrieve the top-k relevant chunks
    3. Combine conversation history + retrieved context in the prompt
    4. Call the OpenAI chat model
    5. Return the answer and source citations

    ### Args
    * **question (str):** The user's current question.
    * **chat_history (list[dict] | None):** Previous chat messages for memory.
    * **k (int | None):** Optional override for how many chunks to retrieve.

    ### Returns
    * **RAGResponse:** Answer text, source citations, and chunk count.

    ### Raises
    * **FileNotFoundError:** If the knowledge base has not been built yet.
    * **ValueError:** If the API key is missing or the question is empty.
    * **RuntimeError:** If retrieval or generation fails.

    Example:
        response = ask_question(
            "What about international customers?",
            chat_history=[
                {"role": "user", "content": "What is the refund policy?"},
                {"role": "assistant", "content": "The refund period is 30 days."},
            ],
        )

        print(response.answer)
    """

    cleaned_question = (question or "").strip()

    if not cleaned_question:
        raise ValueError("Please enter a question.")

    history = chat_history or []

    # Load knowledge base and retrieve relevant chunks for this question
    vectorstore = load_vectorstore()
    retriever = get_retriever(vectorstore , k=k)

    try:  
        retrieved_docs = retriever.invoke(cleaned_question)
    except Exception as e:
        raise RuntimeError(
            "retrieval failed.Try rebuilding the knowledge base."
        ) from e

    context = format_docs(retrieved_docs)
    history_text = format_chat_history(history)
    prompt = load_rag_prompt()
    llm = get_llm()

    final_prompt = prompt.format(
        context = context,
        chat_history = history_text,
        question = cleaned_question,
    )

    try: 
        result = llm.invoke(final_prompt)
        # .text is a str on every provider. .content can be a LIST of content
        # blocks (Gemini does this), which would print as [{'type': 'text', ...}].
        answer = result.text if hasattr(result, "text") else str(result.content)
    except Exception as e:
        message = str(e).lower()
        if "api_key" in message or "authentication" in message or "unauthorized" in message:
            raise ValueError(
                "Gemini rejected the API key. Check GOOGLE_API_KEY in your .env file."
            ) from e
        raise RuntimeError(
            "The chat model failed to generate an answer. Please try again."
        ) from e

    return RAGResponse(
        answer= str(answer).strip(),
        sources = extract_sources(retrieved_docs),
        num_chunks = len(retrieved_docs),
    )