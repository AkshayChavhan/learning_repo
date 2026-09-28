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

# MultiQueryRetriever lives in langchain_classic, NOT langchain.retrievers -
# that path does not exist in LangChain 1.x and raises ModuleNotFoundError.
from langchain_classic.retrievers.multi_query import MultiQueryRetriever

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
    print_title("Multi Query Retrieval")

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
        embedding = embeddings,
    )

    # from_llm with an UNDERSCORE - `from.llm` is attribute access on a method
    # that does not exist. This retriever needs a CHAT MODEL as well as
    # embeddings, because it asks the model to rewrite the question; get_llm()
    # reads config.json, currently Groq.
    retriever = MultiQueryRetriever.from_llm(
        retriever = vector_store.as_retriever(search_kwargs={"k": 2}),
        llm = get_llm(),
        include_original = True,
    )

    query = "Explain Large Language Models"
    print(f"Query: \n{query}")
    print_seperator()

    documents = retriever.invoke(query)
    print(f"Documents returned: {len(documents)}")
    print_seperator()

    for idx, doc in enumerate(documents, start=1):
        print(f"Retrieval Document {idx} \n")
        print(doc.page_content)
        print_seperator()


if __name__ == "__main__":
    main()

# ======================================================================
#  Concept Summary
 
#  MultiQueryRetriever asks an LLM to rewrite your question several different
#  ways, runs a retrieval for EACH version, and returns the union of the hits.

#  It attacks a specific weakness of similarity search: one phrasing gives one
#  point in vector space, so a relevant chunk worded differently can sit just
#  outside the top k and be missed entirely. Several phrasings cover more of
#  that space, and the union catches what any single query would have dropped.

#  Two costs. It needs a CHAT MODEL as well as embeddings - one extra LLM call
#  per retrieval to generate the variants - and it returns MORE than k documents,
#  since k applies per sub-query before deduplication. include_original=True
#  adds your untouched question to the set, which is worth keeping: the rewrites
#  are only as good as the model that produced them.

# ======================================================================
