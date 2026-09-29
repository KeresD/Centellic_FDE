# texts... is imported, not rewritten
# bedding provider has not changed... only where the vectors get stored

import chromadb
from documents import DOCUMENTS
from knowledge import embed_texts

chroma = chromadb.PersistentClient(path="./chroma_store")

collection = chroma.get_or_create_collection(
    name="firm_documents", 
    # HNSW (hierachchial Navigable Small World) is a graph
    # based index used in vector databased to perform fast and appropriate 
    # nearest neighbour search in high dimensional data
    configuration={"hnsw": {"space": "cosine"}}
)

def count() -> int:
    return collection.count()

def build_index() -> int:
    '''Embed every document and hand the vectors to Chroma'''
    texts = [doc["body"] for doc in DOCUMENTS]
    vectors, tokens = embed_texts(texts, input_type="document")
    
    # upsert: idempotent - if data inserted already exists then it will overwrite, if not exists it will insert as new.
    collection.upsert(
        ids=[doc["id"] for doc in DOCUMENTS],
        embeddings=vectors,
        documents=texts,
        metadatas=[{"title": doc["title"], "type": doc["type"]} for doc in DOCUMENTS],
    )

    return tokens

# Chroma will give us back distance, lower = closer.
def search(question: str, top_k: int = 3) -> list[dict]:
    if collection.count() == 0:
        raise RuntimeError("Index is empty - call build_index() first")
    
    '''Embed the question and let Chroma do the storing.'''
    query_vectors, _ = embed_texts([question], input_type="query")
    
    result = collection.query(query_embeddings=query_vectors, n_results=top_k)
    
    return [
        {
            "id": doc_id,
            "title": metadata["title"],
            "text": text,
            # Chroma gives distance (lower = closer); convert to similarity for consistency
            # with your old cosine_similarity scores, where higher = more relevant
            # we will do 1 minus distance to flip from return distance, to similarity
            "score": 1 - distance,
        }
        for doc_id, metadata, text, distance in zip(
            result["ids"][0],
            result["metadatas"][0],
            result["documents"][0],
            result["distances"][0],
        )
    ]
    
    # things to note from our switch to Chroma
    
        # embed_texts is imported and not rewritten. Embedding provider hasn't changed - only storage has
        # configureation=...--> no optional, we are choosing something different from Chromas default
        # Chroma returns distance, we return similarity
            # in Chroma, lower = better, higher was better for ours - (1 - distance) --> converts
        # upsert instead of add -> add fails on an id that already exists, but upsert overwrites