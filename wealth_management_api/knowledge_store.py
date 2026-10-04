"""Embedding and vector storage. Voyage turns text into vectors; Chroma stores and searches them.
Nothing in here knows about FastAPI or Claude."""

import os
from typing import Any, cast

import chromadb
import config
from chromadb.api.types import PyEmbeddings, Where
from data_doc.documents import DOCUMENTS
from voyageai.client import Client  # type: ignore[import-untyped]

voyage = Client(api_key=os.environ["VOYAGE_API_KEY"], max_retries=3, timeout=30)

chroma = chromadb.PersistentClient(path=config.CHROMA_PATH)
collection = chroma.get_or_create_collection(
    name=config.CHROMA_COLLECTION,
    # HNSW is the graph index Chroma uses for fast nearest-neighbour search.
    # Cosine (not Chroma's default L2) because we compare direction, not length.
    configuration={"hnsw": {"space": "cosine"}},
)


# ---------- embedding ----------

def embed_texts(texts: list[str], input_type: str) -> tuple[PyEmbeddings, int]:
    """input_type tells Voyage whether these are documents being stored or a query being asked."""
    result = voyage.embed(texts=texts, model=config.EMBED_MODEL, input_type=input_type)
    # Voyage's types allow int vectors, but those only come back for compressed
    # output_dtype values, which we never request. PyEmbeddings is Chroma's own type.
    return cast(PyEmbeddings, result.embeddings), result.total_tokens


# ---------- indexing ----------

def _doc_id(doc: dict) -> str:
    return f"doc-{doc['document_id']:03d}"     # 7 becomes "doc-007", which Claude cites


def _metadata(doc: dict) -> dict[str, Any]:
    # Chroma metadata values must be str, int, float or bool, so None keys are left out
    meta: dict[str, Any] = {"title": doc["title"], "document_type": doc["document_type"],
                            "date": doc["date"]}
    for key in ("fund_id", "mandate_id"):
        if doc.get(key) is not None:
            meta[key] = doc[key]
    return meta


def count() -> int:
    return collection.count()


def build_index() -> dict:
    """Embed every document, upsert by id, and remove vectors for documents that no longer exist."""
    ids = [_doc_id(doc) for doc in DOCUMENTS]
    texts = [doc["content"] for doc in DOCUMENTS]
    vectors, tokens = embed_texts(texts, input_type="document")

    # upsert: safe to re-run; existing ids are overwritten, new ones are added
    collection.upsert(
        ids=ids,
        embeddings=vectors,
        documents=texts,
        metadatas=[_metadata(doc) for doc in DOCUMENTS],
    )

    # upsert never deletes, so remove anything Chroma holds that the source no longer has
    current = set(ids)
    stale = [i for i in collection.get()["ids"] if i not in current]
    if stale:
        collection.delete(ids=stale)

    return {"indexed": len(ids), "removed": len(stale),
            "embedding_tokens": tokens, "embed_model": config.EMBED_MODEL}


# ---------- searching ----------

def search(question: str, top_k: int = config.SEARCH_TOP_K, where: Where | None = None) -> list[dict]:
    """Embed the question and return the closest documents, best first.
    where: optional metadata filter, e.g. {"mandate_id": 2}."""
    if collection.count() == 0:
        raise RuntimeError("Index is empty - call POST /knowledge/index first")

    query_vectors, _ = embed_texts([question], input_type="query")
    result = collection.query(query_embeddings=query_vectors, n_results=top_k, where=where)

    ids = result["ids"][0]
    metadatas = (result["metadatas"] or [[]])[0]
    texts = (result["documents"] or [[]])[0]
    distances = (result["distances"] or [[]])[0]

    return [
        {
            "id": doc_id,
            "title": meta["title"],
            "document_type": meta["document_type"],
            "date": meta["date"],
            "text": text,
            # Chroma returns distance (lower = closer); 1 - distance gives similarity (higher = closer)
            "score": round(1 - distance, 4),
        }
        for doc_id, meta, text, distance in zip(ids, metadatas, texts, distances, strict=True)
    ]


def format_context(results: list[dict]) -> str:
    """Turn search results into the context block Claude answers from."""
    return "\n\n".join(f"[{r['id']}] {r['title']} (dated {r['date']})\n{r['text']}" for r in results)