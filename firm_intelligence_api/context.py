"""
How retrieval hits become the text the model reads
Failure: lost in the middle
"""

# hits
def order_for_context(hits: list[dict]) -> list[dict]:
    """Reorder retrieved chunks so the strongest sit at the start and end
    of the context, and the weakest fall in the middle.

    Mitigates "lost in the middle": models use information at the edges
    of a long context more reliably than information in the middle.
    Only changes placement, never which chunks are included.
    
    Best hit first, second best last, weakest in the middle.

    Example: ranked goes from [0.9, 0.8, 0.6, 0.5, 0.4] -> [0.9, 0.6, 0.4, 0.5, 0.8]
    """
    ranked = sorted(hits, key=lambda h: h["score"], reverse=True)
    front = ranked[0::2] # a, c, e
    back = ranked[1::2] # b, d
    return front + back[::-1] # a, c, e, d, b

def build_context(hits: list[dict]) -> str:
    """The exact text block the model sees, one labelled section per hit."""
    return "\n\n".join(f"[{h['id']}] {h['title']}\n{h['text']}" 
                       for h in order_for_context(hits))