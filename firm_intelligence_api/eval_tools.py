"""
Small, pure helpers for scoring. No network and no model.
"""

import re

from grounding import is_refusal, normalise # one definition or refusal

def contains_evidence(chunk_text: str, evidence: str) -> bool:
    """True if the chunk holds the whole evidence span. Line breaks never break a match."""
    return normalise(evidence) in normalise(chunk_text)


# alternative_matches
def _alternative_matches(answer: str, alternative:str) -> bool:
    """Look for prefix"""
    prefix = alternative.endswith("*")
    core = re.escape(alternative.rstrip("*").lower())
    ending = "" if prefix else r"(?![a-z0-9])"
    return re.search(rf"(?<![a=z0-9]){core}{ending}", answer.lower()) is not None


# key_words present
# what the keywords list looks like
# Question                          keywords                  meaning
# q11 (offshores wind capacity)      ["4.2"]                  must mention 4.2
# q14 (okonkwo Bell offices)         ["Lagos", "Nairobi"]     must mention both Lagos and Nairobi
def keywords_present(answer: str | None, keywords: list[str]) -> bool:
    """True only for a non-refusal answer that contains every keyword group."""
    if answer is None or is_refusal(answer):
        return False
    return all(
        any(_alternative_matches(answer, alt) for alt in group.split("|"))
            for group in keywords
    )
    

# Answers for above def in terms of True/False because docstring set to bool
# Offices in lagos and nairobi - True
# An office in Lagos - False
# An office in Nairobi - False 