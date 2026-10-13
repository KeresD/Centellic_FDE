"""Checks on generated answers. Pure functions - no network call, no model, no FastAPI
Failure 1 - ungrounded hallucination: sentences that carry no citations at all.
Failure 2 - citation drift: citations that point at the wronf source, or at no source."""

import re

REFUSAL_SENTENCE = "The provided documents do not answer that question."

# the fidall will return doc-001, rather than [doc-001]
CITATION = re.compile(r"\[(doc-\d{3})\]")

# normalise - lower-case and squash every run of white spaces, tabs/newlines into space
    # we need this as models wrap lines - so w/o normalise a refusal 
    # split across two lines would nor match
def normalise(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip(). lower()

# is_refusal - treats None as a refusal too.
    # we are standardising the refusal
    # /knowledge/ask returns answwer: None when it refuses before aclling the model, 
    # and the check should agree with the endpoint
def is_refusal(answer: str | None) -> bool:
    return answer is None or normalise(REFUSAL_SENTENCE) in normalise(answer)


def split_sentence(text: str) -> list[str]: # type: ignore
    """Split an answer into sentences, keeping a trailing citation with its sentence.
    Models can write both 'Revenue rose [doc-101].' and 'Revenue rose. [doc-101]
    The second format would otherwise leave '[doc-101]' as a sentence of its own."""
    
    pieces = []
    for line in text.splitlines():
        line = line.strip(" -*\t")
        if line:
            pieces.extend(p for p in re.split(r"(?<=[.!?])\s+", line) if p)
            
    sentences: list[str] = []
    for piece in pieces:
        if sentences and CITATION.sub("", piece).strip(" .") == "":
            sentences[-1] = f"{sentences[-1]} {piece}"
        else:
            sentences.append(piece)
    return sentences


# citations_in
def citations_in(text:str) -> list[str]:
    return CITATION.findall(text)

# check_citations
def check_citations(answer: str | None, source_ids: list[str]) -> dict:
    """Cheap structure check. Catches uncited claims and citations to source
    we never gave.""" 
    if answer is None or is_refusal(answer):
        return {"refusal": True, "cited": [], "invalid": [],
                "uncited_sentences": [], "passed": True}
    sentences = split_sentence(answer)
    cited = sorted(set(citations_in(answer)))
    invalid = [doc_id for doc_id in cited if doc_id not in source_ids]
    # uncited = very short sentences so things like ("Yes." or "In Summary:") are claims not worth policing 
    uncited = [s for s in sentences if not CITATION.search(s) and len(s.split()) >= 3]
    
    return {
        "refusal": False,
        "cited": cited,
        "invalid": invalid,
        "uncited_sentences": uncited,
        "passed": not invalid and not uncited,
    }

# create tests