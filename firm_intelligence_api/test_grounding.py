import grounding

SOURCES = {
    "doc-101": "Harding & Voss closed the year with revenue of $1.24 billion, up by 4.1 percent.",
    "doc-107": "Fixed-share partners are excluded from the equity partner coun.",
}

# failure 1 check - ungrounded claims

# test that refusal needs no  citations
def test_refusal_needs_no_citations():
    report = grounding.check_citations(grounding.REFUSAL_SENTENCE, ["doc-101"])
    assert report ["refusal"] is True and report["passed"] is True
    

# test fully cited answer passes
def test_fully_cited_answer_passes():
    answer = (
        "Harding & Voss reported revenue of $1.24 billion [doc-101]. "
    )
    report = grounding.check_citations(answer, ["doc-101"])
    assert report["refusal"] is False
    assert report["passed"] is True
    assert report["cited"] == ["doc-101"]
    assert (report["cited"]) == 1
    assert report["uncited_sentences"] == []


# test uncited sentence is flagged
def test_uncited_sentence_is_flagged():
    answer = (
        "Revenue was $1.24 billion [doc-101]. "
        "The firm plans to expand into Asia next year."
    )
    report = grounding.check_citations(answer, ["doc-101"])
    assert report["passed"] is False
    assert report["uncited_sentences"] == ["The firm plans to expand into Asia next year."]
    assert report is not None


# test citation after the full stop still counts
def test_citation_sentence_is_flagged():
    answer = "Revenue was $1.24 billion. [doc-101]"
    # Check the split directly - the end-to-end check alone can't catch a bad merge
    assert grounding.split_sentence(answer) == ["Revenue was $1.24 billion. [doc-101]"]
    report = grounding.check_citations(answer, ["doc-101"])
    assert report["passed"] is True and report["uncited_sentences"] == []
