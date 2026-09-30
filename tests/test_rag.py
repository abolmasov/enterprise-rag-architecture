from src.pipeline.rag import RagPipeline


def test_grounded_answer_includes_citation():
    rag = RagPipeline()
    rag.ingest_text("policy-1", "All vendor access requires quarterly review.")
    result = rag.ask("vendor access review")
    assert result.citations
    assert "quarterly" in result.answer.lower() or result.citations
