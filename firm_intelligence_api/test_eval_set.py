import re

from corpus import CORPUS_DOCUMENTS
from documents import DOCUMENTS
from eval_set import EVAL_SET, answerable
from eval_tools import contains_evidence, keywords_present, normalise

ALL_DOCS = {d["id"]: d for d in DOCUMENTS + CORPUS_DOCUMENTS}

def section_containing(body: str, evidence: str) -> tuple[str, str]:
    """Return (heading, section text) for the section holding the evidence."""
    for part in re.split(r"(?m)^##", body):
        heading, _, text = part.partition("\n")
        if contains_evidence(text, evidence):
            return heading.strip(), text    
    raise AssertionError(f"Evidence not found in any section:{evidence}")


# test ids = unique
def test_doc_ids_are_unique():
    seen = set()
    for d in DOCUMENTS + CORPUS_DOCUMENTS:
        assert d["id"] not in seen, f"Duplicate id: {d["id"]}"
        seen.add(d["id"])
    

# test every evidence span is in its documents
def test_every_evidence_in_doc():
    for q in answerable():
        doc = ALL_DOCS[q["doc_id"]]
        assert contains_evidence(doc["body"], q["evidence"]), q["id"]

# test every evidence span appears exactly once in the whole corpus
def test_evidence_appears_exactly_once():
    for q in answerable():
        found_in = []
        for doc in ALL_DOCS.values():
            if contains_evidence(doc["body"], q["evidence"]):
                found_in.append(doc["id"])
        assert len(found_in) == 1, f"{q['id']}: found in {found_in}"
        

# test keyword matching in whole world and refusal aware
def test_keywords_present():
    assert keywords_present("There is no office.", ["no"])
    assert not keywords_present("It is not open.", ["no"])           # whole word
    assert keywords_present("11 partners left.", ["eleven|11"])      # alternatives
    assert keywords_present("They are excluded.", ["exclud*"])       # prefix
    assert not keywords_present("An office in Lagos.", ["Lagos", "Nairobi"])  # all groups needed
    assert not keywords_present(None, ["2028"])                      # refusal