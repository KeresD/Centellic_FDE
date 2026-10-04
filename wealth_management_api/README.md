## Run the API

    cd wealth_management_api
    python -m venv .venv && source .venv/bin/activate
    pip install -r requirements.txt
    export ANTHROPIC_API_KEY=...  VOYAGE_API_KEY=...
    uvicorn main:app --reload

## Environment variables
Copy `.env.example` to `.env` and fill in the two API keys. Everything else has a sensible default.

| Variable | Required | Default | Purpose |
|---|---|---|---|
1. `ANTHROPIC_API_KEY` | Yes | – | Claude: summaries, analysis, grounded answers, agent |
2. `VOYAGE_API_KEY` | Yes | – | Document and query embeddings |
3. `ANTHROPIC_MODEL` | No | `claude-haiku-4-5-20251001` | Claude model for every call |
4. `VOYAGE_MODEL` | No | `voyage-3-lite` | Embedding model. Changing it means rebuilding the index and re-tuning the floor |
5. `RELEVANCE_FLOOR` | No | `0.33` | Minimum similarity for a document to reach Claude. If nothing clears it, `/ask` refuses without calling Claude |
6. `HOLDINGS_STALE_DAYS` | No | `45` | Holdings older than this produce a warning in compliance results |
7. `AGENT_MAX_ITERATIONS` | No | `5` | Hard limit on agent model calls per question |
8. `CHROMA_PATH` | No | `./chroma_store` | Where Chroma persists the vector index |
9. `CHROMA_COLLECTION` | No | `wrenford_documents` | Chroma collection name |
10. `SEARCH_TOP_K` | No | `3` | Documents returned per search |