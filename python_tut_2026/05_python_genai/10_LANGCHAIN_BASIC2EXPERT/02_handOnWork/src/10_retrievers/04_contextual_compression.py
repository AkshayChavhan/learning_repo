from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import _bootstrap  # noqa: F401  re-launches under myenv/ if python3 is the wrong one

# Third-party imports go BELOW _bootstrap. Above it they run before the re-exec
# fires, so the wrong interpreter dies on the import instead of being switched.
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Both live in langchain_classic, NOT langchain.retrievers - that path does not
# exist in LangChain 1.x and raises ModuleNotFoundError.
from langchain_classic.retrievers import ContextualCompressionRetriever
from langchain_classic.retrievers.document_compressors import LLMChainExtractor

# --- OPENAI ALTERNATIVE (commented) -----------------------------------------
# from langchain_openai import OpenAIEmbeddings
# ----------------------------------------------------------------------------

from llm_client import get_llm
from utils.helpers import print_seperator , print_title

load_dotenv()

# See 09_embeddings_vectorstores/embeddings.py - text-embedding-004 is 404 on
# this account, so only gemini-embedding-001 / -2 / -2-preview are served.
EMBEDDING_MODEL = "models/gemini-embedding-001"

# --- OPENAI ALTERNATIVE (commented) -----------------------------------------
# OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"
# ----------------------------------------------------------------------------


def main():
    print_title("Contextual compression Retriever")

    loader = TextLoader(PROJECT_ROOT / "data" / "input" / "sample.txt", encoding="utf-8")
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 200,
        chunk_overlap = 50,
    )
    chunks = splitter.split_documents(documents)
    print(f"Chunks indexed: {len(chunks)}")
    print_seperator()

    # ACTIVE: Gemini
    embeddings = GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL)

    # --- OPENAI ALTERNATIVE (commented) -------------------------------------
    # Swap the two lines to switch providers - nothing else changes, because both
    # classes implement the same Embeddings interface. Dimensions differ though
    # (Gemini 3072, OpenAI 1536), so an index built with one must be REBUILT,
    # never reused, with the other.
    #
    # embeddings = OpenAIEmbeddings(model=OPENAI_EMBEDDING_MODEL)
    # ------------------------------------------------------------------------

    vector_store = FAISS.from_documents(
        chunks,
        embeddings,
    )

    base_retriever = vector_store.as_retriever(search_kwargs={"k": 4})

    # from_llm with ONE l in llm. The extractor is what needs the chat model:
    # it reads each retrieved chunk and pulls out only the parts that answer
    # the question, so there is one LLM call PER retrieved document.
    compressor = LLMChainExtractor.from_llm(get_llm())

    retriever = ContextualCompressionRetriever(
        base_retriever = base_retriever,
        base_compressor = compressor,
    )

    query = "What are LLM models ?"
    print(f"Query: {query}")
    print_seperator()

    # Compare against the uncompressed hits so the trimming is visible.
    raw = base_retriever.invoke(query)
    documents = retriever.invoke(query)
    print(f"Before compression: {len(raw)} documents, "
          f"{sum(len(d.page_content) for d in raw)} characters")
    print(f"After  compression: {len(documents)} documents, "
          f"{sum(len(d.page_content) for d in documents)} characters")
    print_seperator()

    for idx, doc in enumerate(documents, start=1):
        print(f"Retrieval Document {idx} \n")
        print(doc.page_content)
        print_seperator()


if __name__ == "__main__":
    main()

# ======================================================================
#  Concept Summary
 
#  ContextualCompressionRetriever wraps a base retriever and runs every hit
#  through a compressor before returning it. LLMChainExtractor is a compressor
#  that asks an LLM to keep only the sentences answering the question.

#  Retrieval works on whole chunks, so a hit is relevant as a unit while most of
#  its text may be irrelevant to this particular question. That padding costs
#  context window and dilutes the signal the answering model sees. Compression
#  trims each hit down to the part that earned its place.

#  The cost is calls: one LLM call PER retrieved document, on top of the answer
#  call - so k=4 means five requests for one question. It can also return FEWER
#  documents than the base retriever, because a chunk with nothing relevant in
#  it is dropped entirely rather than returned empty.

# ======================================================================
