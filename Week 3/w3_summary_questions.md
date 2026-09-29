# Questions

## 1. Explain one of the key steps in the RAG process.
When a query comes in, it gets embedded with the dedicated function (in firm_intelligence it's ` input_type ="query"`) and compared against the stored document vectors/ vector database. The top few closest/relative chunks to the query vectors are pulled out. Those chunks are the only evidence the model sees.  If retrieval brings back the wrong docs, then the answer cannot be better than the evidence, so this step sets the ceiling on quality of the output.

## 2. Explain what an embedding actually is.
List of numbers (vectro) that = the meaning of a piece of text. The embedding model = trained so that the texts with similar meaning end up close together in that space, even when they share no words.
### Example:
    - "Lateral partner recruitment in London"
    - "UK lateral hiring"
Both land near each other. Cosine similarity measures how close two vectors point in the same direction. The embedding doesn't store the text, but stores the position that stands for its meaning.

## 3. Explain why retrieval can fail even when it looks like it's working.
The query always returns something. Top-k gives 'k' amount of results set in the code file, even when none of them actually answer the question, and the score can look reasonable. Nothing gives errors. Some common causes for why retrieval can fail include: 
    - answer isn't in the corpus at all
    - question uses different framing than the documents
    - right document ranks 4th when you only take top-k = 3
    - chunking splits the key sentence away from its context

In this code file there was a quieter version, where it was calling `search()` on an empty Chroma collection it returns `[]`. This trigegrs a refusal that looks like "nothing relevant" when the real problem is "you never indexed". The only way to catch this kind of failure is to measure it, for example throuh golden set and recall@k. 

    Recall@k = (relevant documents in the top k) / (total relevant documents)

Recall@k - measures whether retrieval found the right documents and it's the fraction of the relevant documents that show up in the top-k results.

    How it's used:
        - build the golden set - questions paired with the docs that should answer them
        - run every question through the search
        - average recall@k across all of them - tells you how often retrieval gets the right evidence in fron of the model.

    Things to know:
        - Depends on the k - a bigger k almost always gives a higher recall. With 8 doc and k = 8 its always 1.0, which tells you nothing. Pick the k you actually see, here top_k = 3.
        - It ignores the order of docs - revevant doc in position 1 and one in position 3 count as the same. Metrics like MRR and nDCG reward ranking the right doc higher.
        - It ignores junk - extra irrelevant resutls don't lower recall. Precision@k is the metric that measures that

It's usually the first retrieval metric people check, because if recall is low, the right document never reaches the model and no prompt can fix that.

## 4. Explain what the relevance floor does.
`RELEVANCE_FLOOW = 0.35` = minimum similarity score. In /ask, any hit below it is thrown away before the model is called. If nothing survives, the endpoint returns `"refused": True` without calling the LLM.

This stops the model from being handed weak context and producing a confident-sounding answer from it. Also saves the cost of a call that can't produce a grounded answer. Trade-off is that if set too high and you refuse good questions, set it too low and junk gets through.

## 5. Explain the difference between retrieval and generation in RAG.
Retrieval finds evidence through embedding, vector search, and ranking.
it's deterministic and cheap, and there's no language model involved. Generation in RAG writes the answer.

`answer_from_context()` sends retrieved text plus the question to Claude (because ANTHROPIC_API_KEY) with a grounded system prompt. 

Retrieval and Generation fail differently.

Retrieval fails by fetching the wrong things. Generation fails by misreading or ignoring the right htings, or by going beyong them. That's why you evaluate them separately.

## 6. Explain what changed when we moved from the in-memory index to Chroma.
Only where the vectors live and how they're searched changed. the Voyage embeddings didn't change.

- Persistence: 
    In memory `INDEX` vanished every time uvicorn --reload restarted. Chroma writes to `./chroma_store` on disk, so that the index survives restarts.
- Search:
    your hand written cosine loop was replaced by Chroma's HNSW index, a graph structure that fins approximate nearest neighbours fast at scale.
- Scores:
    Chroma returns distance (lower = closer), so the score was converted with `1 - distance` to keep the same similarity scale the 0.35 floor was calibrated on in firm_intelligence_api 
- Idempotency:
    `upsert` means re-indexing overwrites instead of duplicating

Router barely changed because the same function names and `INDEX` bookkeeping list was kept. 

## 7. Explain how tool use works, at a high level.
Model never runs anything itself. You describe the available tools (here `search_knowledge_base` with a `query` field). 

The model can reply with a strcutured request:
"call this tool with this input"

My code then executes `_execute_tools`, runs the tool and sends the result back. The model then either asks for another call or writes the final answer. 

It's a loop: 
- model asks
- code executes
- results goes back
- repeat

Difference from plain RAG is that the model decides whether and what to search, instead of you always searching once up front.

## 8. Explain what context engineering means, in your own words.
This is deciding what foes into the model's context widow, and in what form. The prompt wording is part of it, but so are:

- which chunks = retrieved and how many
- relevance floor that filters them
- how results = formatted (IDs, titles, scores)
- system prompt's grounding rules
- what you deliberately leave out

Model can only reason over what's in front of it, so shaping that input = mode of the job.

## 9. Explain why we capped the tool-use loop.
Because model controls when it stops, and nothing guarantees that it will. It might keep re-searching with slightly different queries, get stuck on errors, or loop on an empty result.

Each iteration = a paid API call and adds latency.
`MAX_ITERATIONS = 4` = a hard upper bound. If it's hit, the return `stop_reason: "max_iterations` nistead of hanging or running up a bill. It's the same idea as a timeout: a set limit on something you don't fully control.

## 10. Explain why the UI needed its own separate environment.
UI - Streamlit

It needed it's own separate application with its own dependencies. Putting it in the API's venv risks version clashes with packages like FastAPI, Pydantic or chromadb.

Keeping it separate also keeps the architecture honest: the UI is just a client that calls your API over HTTP, the way any other consumer would. It doesn't import your Python modules directly - so you can change, redeploy or replace either side without breaking the other.