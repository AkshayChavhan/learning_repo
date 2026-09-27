from dataclasses import dataclass , field


@dataclass
class SourceCitation:
    """
    A single  source citation extracted from a retrieved document chunk.

    Attributes:
        Filename (str) : Name of the source file (for example , refund_policy.pdf).
        page ( int | None): Page number when available (pdf. None for the DOCX. 
        Preview  (str) : Short text preview of the retrieved chunk,
    """

    filename: str
    page: int | None = None
    preview: str = ""

@dataclass
class RAGResponse:
     """
     Final answer  returned  by the convenrsational RAG pipeline.

     Attribute:
        Answe (str): The LLM-generated answer.
        sources (list[SourceCitation]): Unique source citations used for the answer.
        num_chunk (int): How many dcument chunks were retrieved for this question.

    Example:
        response = RAGResponse(
            answer="The refund  period is 30 days.",
            sources = [SourceCitation(filename="refund_policy.pdf" , page=1)],
            num_chunk=4,
        )
        print(response.asnwer)        )
     """

     answer : str
     sources: list[SourceCitation] = field(default_factory=list)
     num_chunks: int = 0


     