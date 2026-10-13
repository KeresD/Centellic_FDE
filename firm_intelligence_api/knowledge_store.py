# texts... is imported, not rewritten
# bedding provider has not changed... only where the vectors get stored

import knowledge
import chunk_index

# our chosen strategy
CHUNK_STRATEGY = "seelctions_contextual"
    
def count() -> int:
    return chunk_index.collection_for(CHUNK_STRATEGY).count()

def build_index() -> int:
    """chunk and embed the corpus - free if nothing has changed since the last build."""
    return chunk_index.build(CHUNK_STRATEGY)["embedding_tokens"]


# Chroma will give us back distance, lower = closer.
def search(question: str, top_k: int = 3) -> list[dict]:
    '''Embed the question and let Chroma do the storing.'''
    query_vectors, _ = knowledge.embed_texts([question], input_type="query")
    query_vectors, _ = knowledge.embed_texts([question], input_type="query")
    
    return chunk_index.search_with_vectors(CHUNK_STRATEGY, query_vectors, k=top_k)[0]