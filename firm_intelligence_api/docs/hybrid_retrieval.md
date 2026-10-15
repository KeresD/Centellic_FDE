## 1. Rank or score? There are two families of fusion. Rank-based fusion (such as Reciprocal Rank Fusion) uses only each list's order. Score-based fusion rescales each list's scoresand adds them. What does each gain, and what does each throw away?

In hybrid retrieval, both lexical and semantic search is combined. There are two methods in the fusion retrieval.

Rank-based fusion retrieval completely ignores the raw numerical scores. It converts the results into ordered lists, assigns a mathematical penalty based strictly on each document's rank position, and adds those penalties together. It gains protection against outlier scales (scale invariance) because it relies solely on the position order of items in the list. This is important as the different scales (that the lexical retriever uses and the semantic retriever uses) impact the match. Its also simpler as you don’t need to normalise, rescale, or calibrate the scores. However, it throws away the absolute strength of the match and lacks the fine-grained precision needed to differentiate items closely.

Score-based fusion retrieval, on the other hand,  keeps the raw scores but recognises they are completely incompatible. It standardises the scoring distributions onto a matching scale (usually 0.0 to 1.0), applies a weight multiplier to balance them, and adds them up. This allows it to high calibration, precise relative distances, and exact match strengths. However, it throws away scale-independence, meaning it is vulnerable to being dominated by retrievers with larger numerical ranges unless explicitly normalized. I

More info: https://arxiv.org/abs/2210.11934


## 2. Does hybrid actually help? Find one published comparison with numbers: hybrid against keyword-only or vector-only. Note the dataset, the metric,the size of the gain, and who ran it.
Yes - https://arxiv.org/pdf/2502.16767v1

### Who ran it
Rayo, de la Rosa & Garrido (Universidad de los Andes), *A Hybrid Approach to Information Retrieval and Answer Generation for Regulatory Texts*, COLING 2025 (arXiv:2502.16767)

Rayo, de la Rosa and Garrido conducted this comparison on **ObliQA**, a dataset containing 27,869 regulatory questions from 40 documents. These results demonstrate improved retrieval in their study; they do not directly benchmark Postgres with pgvector.

# Retrieval Methods
Keyword-only = BM25 (lexical)
Vector-only = Semantic system
Hybrid = Hybrid system

Hybrid method integrates lexical and semantic retrieval methods. The paper we researched shows the usage of BM25 with embedding-based models to address nuanced language and diverse technologies inherent in regulatory domains.

### Dataset
- Dataset they used in this paper: 
    ObliQA, 27,869 regulatory questions from 40 Abu Dhabi Global Markets documents

    Regulatory documents are hard to search because they use specialised, varied wording. The authors found that combining keyword search (BM25) with meaning-based search (embeddings) works better than either one alone, and gives higher Recall@10 and MAP@10 scores.

    They also used an LLM to turn the retrieved passages into short, clear answers. But the answers weren’t always fully backed up by the source passages, so that part needs work.

    They tested three LLMs for writing the answers: GPT-3.5 Turbo and GPT-4o Mini (both via Azure OpenAI) and Llama 3.1 (via Groq). Each was scored on RePASs, which measures how well an answer is backed by the source passages, avoids contradicting them, and covers the obligations in them.

    GPT-3.5 Turbo scored highest, so they used it in the final system.

    Even the best model, at 0.57, didn’t beat the baseline system’s 0.58. Better retrieval didn’t lead to better answers here.

### Metrics:

- Metrics they used in this paper: 
    Recall@10 and MAP@10

| System | Recall@10 | MAP@10 |
|---|---:|---:|
| BM25 baseline | 0.7611 | 0.6237 |
| Custom BM25 | 0.7791 | 0.6415 |
| Semantic-only | 0.8103 | 0.6286 |
| **Hybrid (0.65 semantic + 0.35 lexical)** | **0.8333** | **0.7016** |

Although, the paper uses two configurations of the same retrieval method (BM25) it doesn't explain exactly what is different between them.

### Size of the gain:
- Against custom BM25 (keyword-only): Recall@10 improves by +5.4 pct.pts, MAP@10 improves by +6.0 pct.pts
- Against semantic-only (vector-only): Recall@10 improves by +2.3 pct.pts, MAP@10 improves by +7.3 pct.pts

Conclusion: Hybrid improves both Recall@10 and MAP@10 in this study. Against vector-only retrieval, MAP@10 increases by 7.3 percentage points and Recall@10 by 2.3 percentage points.

Next, they plan to:

- train the LLM on regulatory text
- tune the cut-off for which passages count as relevant
- find better ways to combine the two search scores

## 3. Where does the keyword half come from? In production, is it classic BM25 from an inverted index, or a learned sparse model? Find one example of each.

For paper discussed the keyword aspect uses classic BM25 - section 2.3 in the paper reports BM25 parameters of **k₁ = 1.5 and b = 0.75**.

### In production:

1. Classic BM25 from an inverted index: 
- Text is tokenized, the index finds documents containing those tokens, and BM25 scores matches using term frequency, term rarity, and document length.

e.g., Azure AI Search
- In a hybrid query, Azure AI Search runs full-text and vector searches in parallel. The full-text query searches text fields marked searchable, retrieves matches through an inverted index, and ranks them using BM25. This supplies the keyword component. The vector query produces a separate ranking based on vector similarity, and Reciprocal Rank Fusion (RRF) merges the two ranked lists into the final results. 
    - https://learn.microsoft.com/en-us/azure/search/hybrid-search-overview 

2. Learned sparse retrieval:
- A trained model assigns contextual importance weights to specific terms, producing sparse representations used for retrieval.

e.g., Elastic’s ELSER
- ELSER generates sparse representations of documents and queries as weighted terms, including learned term expansions that can bridge vocabulary differences. At indexing time, Elasticsearch stores the document terms and weights; at query time, it uses the query’s sparse representation to retrieve relevant documents. The weights come from a trained model rather than BM25’s frequency-based formula.
    - https://www.elastic.co/docs/explore-analyze/machine-learning/nlp/ml-nlp-elser

Elastic can combine ELSER results with BM25 results using Reciprocal Rank Fusion (RRF). In this configuration, BM25 supplies the keyword component and ELSER supplies the sparse semantic component—so learned sparse retrieval does not necessarily replace the keyword half.
    - https://www.elastic.co/search-labs/blog/improving-information-retrieval-elastic-stack-hybrid


## Advice for our app
The completed table from "Apply it to our app".
Should we add hybrid search? Yes or no, because ...

YES - Using this appraoch could  be generally beneficial and reduce false refusals.  For example, q24 where sementic serch was not enough to answer it. Our current implementation uses VoyageAI for embedding  ChromaDB for storage and semantic search. PostgreSQL with pgvector would allow hybrid approch, Postgres has full search text nativly and allows  storing documents/data.This abbility could be combined with pgvector  enabling semantic vector search as well in hybrid approach. This hybrid search could be be benificial to reduce false refusals espiaclly when data scales and theres more potential questions.
From a critical perspective,  it might be initally complex to set up the sql and migrate data to postgres.

## Open questions
What you could not answer in the time.

## 4. For your system, find out: Postgres with pgvector

PostgreSQL (Postgres) is a database that stores and queries data, such as documents, users, and records. It also has built-in keyword/full-text search.

Postgres with pgvector has no built-in hybrid search switch, so you implement it yourself in SQL:
- first build the full-text keyword representation (tsvector) and its GIN inverted index once.
    - full-text search = quickly locating rows containing specific words or terms across text documents.
    - GIN = generalised inverted index -->  a type of database index designed to handle complex or multi-value data types where a single database row can contain multiple individual values.
        e.g., arrays, JSONB docs, and full-text search vectors
- each search query we then pass two inputs:
    - query text
    - its embedding
    - where one part performs for keyword retrieval and the other performs for vector retrieval
        - retrieve keyword candidates using PostgreSQL full-text search and vector candidates using pgvector.
    - a final part fuses their rankings together in SQL
        - rank each candidate list separately, then combine their rankings using a fusion method such as Reciprocal Rank Fusion (RRF) which is a rank-based method.

With PostgreSQL’s native full-text search, the keyword ranking uses ts_rank or ts_rank_cd, rather than BM25.

https://www.postgresql.org/docs/17/textsearch-controls.html 

1. How you ask for a hybrid search: the query , setting or API.
    Postgres with pgvector has no built-in hybrid search switch or dedicated hybrid API. Instead, you write SQL that retrieves keyword and vector candidates separately, then combines their rankings.

    First, create a PostgreSQL full-text representation (tsvector) and a GIN inverted index once. For each search, supply the query text and its embedding. Retrieve keyword candidates using full-text search and vector candidates using pgvector, then fuse the results in SQL.

2. Which fusion method it uses, and its default settings.
    There is no built-in fusion method or set of hybrid defaults. The developer chooses the fusion logic and parameters.

The official pgvector example implements Reciprocal Rank Fusion (RRF), a rank-based method. Each document receives a contribution of 1 / (k + rank) from each candidate list; the contributions are added together. A document absent from a list receives zero contribution from that list.

The example settings:
- RRF constant k = 60.
- Up to 20 candidates from each retriever.
- Equal contributions from keyword and vector retrieval.
- Five final results.
- These are example settings, not pgvector defaults. 
https://github.com/pgvector/pgvector-python/blob/master/examples/hybrid_search/rrf.py

3. Whether you can weight one retriever above the other, and how.

Yes, hybrid retrieval using Postgre and pgvector allows lexical and semantic search results  influence/weightings  on the final ranking to be adjusted.. This is because when doing hybrid retrieval Postgre and pgvector it is typically implemented by manually combining full-text search and vector similarity search in SQL. The ranking formula can be adjusted to give greater influence to either lexical or semantic retrieval methods. This is evident in the examples in the blog post by Johnathan[3]  . Bringing it back to our project, using both lexical and semantic search and even being able to weight their output differently is very different to our current approach of using semantic search only voyageai vector embeddings in chromadb and ranking them on the cosine similarity scores.  It enables us to place greater emphasis on semantic similarity or exact keyword matching depending on the requirements of the application.

Offical postgresql documentation - theres a lot ,its index - relevent bit is "full search text" https://www.postgresql.org/docs/18/index.html

4. How it builds the keyword side: BM25, sparse vectors, or something else.
- Native PostgreSQL - keyword side uses full-text search using `tsvector`,a GIN inverted index, and `ts_rank_cd` ranking system, rather than BM25  or learned sparse embeddings.

    - `to_tsvector` converts the document text into normalised words. For example, with English processing, “The cats are running” becomes terms like “cat” and “run”, with common words removed.
    - GIN inverted index speeds up retrieval of documents containing the processed words from the search query.
    - the `@@` operators = PostgreSQL's full-text matching operator and it checks whether the document's processed text `tsvector` matches the search query `tsquery`, returning either `true` or `false`.
    - `ts_rank_cd` used in official pgvector examples, rank matches using cover density, including matching-term frequency and proximity.

PostgreSQL full-text search documentation - https://www.postgresql.org/docs/17/textsearch-controls.html
GIN indexing documentation - https://www.postgresql.org/docs/current/textsearch-indexes.html
Official pgvector hybrid example - https://github.com/pgvector/pgvector-python/blob/master/examples/hybrid_search/rrf.py

5. One limit or catch: a version requirement, a cloud-only feature, a cost.

One limitation this method of pgvector does not provide a complete, automatic hybrid retrieval pipeline out of the box. You must manually write up the SQL logic to fuse the outputs as shown in online examples and sources[1,2] . However  there is many examples and documentation to help with this online. In relation to our firm intelligence api project, it was reletivly simple to use Voyage embeddings for semantic search and chroma to store them in persistent way. On the other hand, there are many examples and extensive documentation of hybrid search which can be referred to.

Note – Cost not really -  Cloud only? (postgress no, it can be local)

https://github.com/pgvector/pgvector - official pgvector documentation, they have on github
https://jkatz05.com/post/postgres/hybrid-search-postgres-pgvector/ - Article on hybrid search approach exactly

6. What its documentation says about testing whether hybrid helps.

Offical postgres documentation has comprehensive guides on its native Full-Text Search (12 on index of documention) but nothing about "hybrid search"[3] . However, pgvector documentation on github supports hybrid search but doesn’t explicitly say its better in all situtions.[1]. Hybrid search methods can be used to boost retravel recall (relevancy of retrieved documents) and other metrics like MRR as highlighted by Johnathan Katz in his blog post where he gave a comphrensive example of implementing hybrid search with postgres and pgvector[2]. Linking back to our project, it might be worthwhile to explore if this improves the methods and stops false refusals like q24 where semantic search alone is not enough to answer it correctly.

https://github.com/pgvector/pgvector - official pgvector documentation, they have on github
https://jkatz05.com/post/postgres/hybrid-search-postgres-pgvector/ - Article on hybrid search approach exactly
https://www.postgresql.org/docs/18/index.html - offical postgresql documentation -theres a lot ,its index - relevent bit is "full search text"

------

## Summary:

Hybrid search means searching in two ways, then combining the results:
- Keyword search: finds matching words—useful for names, codes, and technical terms.
- Vector search: finds similar meaning—useful when the wording differs.

For Postgres with pgvector, remember: “Two searches, one SQL query, one combined ranking.”

1. How do you request it?
There’s no hybrid switch. You write SQL that takes the query text and its embedding, retrieves keyword and vector results separately, then combines them.

2. How does it combine results?
You choose the method. The official example uses Reciprocal Rank Fusion (RRF): each result earns points based on its position in each list. Higher positions earn more points; appearing in both lists adds both contributions.
The example uses k = 60, 20 candidates per search, and 5 final results. These are example choices, not pgvector defaults.

4. How does the keyword side work?
Think of four steps:
1. Process: to_tsvector turns text into processed words—for example, “running” becomes “run”.
2. Find: the GIN inverted index acts like a book’s index, pointing from words to documents.
3. Match: @@ checks whether a document matches the search.
4. Rank: ts_rank_cd scores matches, considering how often matching words appear and how close together they are.

Native PostgreSQL uses this full-text ranking, not BM25. You can add BM25 through an extension such as pg_textsearch, as Tiger Data demonstrates.

In our app:
- could mean more relevant chunks and fewer false refusals
- Postgres already supports keyword search, but its native ranking uses ts_rank or ts_rank_cd. pg_textsearch adds BM25 as another keyword-ranking option.
- You can then combine BM25 keyword results + pgvector semantic results, using RRF, to build hybrid search.

TLDR answer:
With pgvector, we write hybrid search ourselves in SQL. We run keyword and vector retrieval, then combine their rankings using something like RRF. There are no built-in hybrid defaults. Native Postgres uses full-text search for keywords; BM25 needs another extension.


Look up SPLAD after (BERJ tranformer) - part of keyword searches

bM25 --> look up which parameters can be tuned