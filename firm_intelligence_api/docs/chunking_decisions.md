# Chunking decision

**Date:** <today>  **Decided by:** <you>  **Corpus:** documents.py + corpus.py (16 documents)
**Eval set:** eval_set.py (29 answerable, 3 unanswerable)  **Embedding model:** voyage-3-lite

## Decision
We serve `<strategy>` with a relevance floor of `<floor>`.

1. Three floors were run end to end. The results shown before are for `sections_contextual`:
    - 0.35, 0.45, 0.53, 0.55

| Floor | Answer acc. | Refusal acc. | Model calls | Avg input tokens |
|---|---|---|---|---|
| 0.35 | 0.97 | 1.00 | 30 | 420 |
| 0.45 | 0.97 | 1.00 | 30 | 410 |
| 0.53 | 0.97 | 1.00 | 30 | 346 |
| 0.55 | 0.90 | 1.00 | 29 | 312 |

As shown above 0.35, 0.45 and 0.53 have idential output in terms of their answers accuracy (0.97) and refusals accuracy (1.00).

### Output at floor 0.35
.venv/bin/python -m eval_retrieval
Building indexes (free if nothing has changed)...
  whole_document          16 chunks  up to date       0 tokens
  fixed_100               46 chunks  up to date       0 tokens
  fixed_overlap_25        55 chunks  up to date       0 tokens
  sentences_100           49 chunks  up to date       0 tokens
  sections_plain          71 chunks  up to date       0 tokens
  sections_contextual     71 chunks  up to date       0 tokens

Embedded 32 questions once (382 tokens), reused for every strategy.

strategy                 R@1   R@3   R@5    MRR  ctx words  top ans  top unans
------------------------------------------------------------------------------
whole_document          0.69  1.00  1.00   0.84        862     0.56       0.43
fixed_100               0.48  0.79  0.90   0.61        273     0.60       0.49
fixed_overlap_25        0.52  0.93  0.97   0.67        277     0.61       0.50
sentences_100           0.41  0.76  0.90   0.57        262     0.60       0.50
sections_plain          0.31  0.86  0.93   0.54        186     0.61       0.52
sections_contextual     0.86  1.00  1.00   0.93        197     0.66       0.50

Missed at k=3:
  whole_document         none
  fixed_100              q02, q05, q08, q09, q22, q26
  fixed_overlap_25       q02, q09
  sentences_100          q02, q03, q04, q08, q09, q20, q22
  sections_plain         q02, q04, q09, q22
  sections_contextual    none

Saved eval_results/retrieval.json

## --floor 0.35
.venv/bin/python -m eval_answers sections_contextual fixed_overlap_25 whole_document --floor 0.35
floor = 0.35

strategy                answers  refusals  calls  avg in tokens
sections_contextual        0.97      1.00     30            420
    false refusals: q24
    wrong or not refused: none
fixed_overlap_25           0.79      1.00     30            461
    false refusals: q02, q17, q18, q24, q28
    wrong or not refused: q09
whole_document             0.97      1.00     30            923
    false refusals: q24
    wrong or not refused: none

## --floor 0.45
.venv/bin/python -m eval_answers sections_contextual fixed_overlap_25 whole_document --floor 0.45
floor = 0.45

strategy                answers  refusals  calls  avg in tokens
sections_contextual        0.97      1.00     30            410
    false refusals: q24
    wrong or not refused: none
fixed_overlap_25           0.62      1.00     30            400
    false refusals: q02, q08, q09, q12, q13, q14, q15, q17, q18, q24, q28
    wrong or not refused: none
whole_document             0.90      1.00     29            794
    false refusals: q12, q24, q28
    wrong or not refused: none

## --floor 0.53
.venv/bin/python -m eval_answers sections_contextual fixed_overlap_25 whole_document --floor 0.53 
floor = 0.53

strategy                answers  refusals  calls  avg in tokens
sections_contextual        0.97      1.00     30            346
    false refusals: q24
    wrong or not refused: none
fixed_overlap_25           0.55      1.00     27            333
    false refusals: q02, q07, q08, q09, q12, q13, q14, q15, q17, q18, q22, q24, q28
    wrong or not refused: none
whole_document             0.59      1.00     22            664
    false refusals: q04, q05, q06, q10, q12, q14, q15, q18, q19, q24, q28, q29
    wrong or not refused: none

## --floor 0.55
.venv/bin/python -m eval_answers sections_contextual fixed_overlap_25 whole_document --floor 0.55
floor = 0.55

strategy                answers  refusals  calls  avg in tokens
sections_contextual        0.90      1.00     29            312
    false refusals: q06, q09, q24
    wrong or not refused: none
fixed_overlap_25           0.55      1.00     27            318
    false refusals: q02, q07, q08, q09, q12, q13, q14, q15, q17, q18, q22, q24, q28
    wrong or not refused: none
whole_document             0.55      1.00     21            627
    false refusals: q04, q05, q06, q10, q12, q14, q15, q16, q18, q19, q24, q28, q29
    wrong or not refused: none

0.35, 0.45 and 0.53 are identical on both accuracies. 0.53 is the cheapest of the three with
input tokens per call, because it filters out more weak chunks.


## Evidence
Answer and refusal accuracy at floor 0.35:

| Strategy | R@1 | R@3 | MRR | Context words@3 | Answer acc. | Refusal acc. |
|---|---|---|---|---|---|---|
| whole_document | 0.69 | 1.00 | 0.84 | 862 | 0.97 | 1.00 |
| sections_contextual | 0.86 | 1.00 | 0.93 | 197 | 0.97 | 1.00 |
| fixed_overlap_25 | 0.52 | 0.93 | 0.67 | 277 | 0.79 | 1.00 |

Answer accuracy by floor (refusal accuracy was 1.00 for every strategy at every floor):

| Floor | sections_contextual | fixed_overlap_25 | whole_document |
|---|---|---|---|
| 0.35 | 0.97 | 0.79 | 0.97 |
| 0.45 | 0.97 | 0.62 | 0.90 |
| 0.53 | 0.97 | 0.55 | 0.59 |
| 0.55 | 0.90 | 0.55 | 0.55 |

`sections_contextual` - Keeps sections disctinct so matches specific questions more strongly and loses fewer answers as floor rises from 0.35 -> 0.55. It has the strongest retrieval results with the the highest recall and precision accuracy at the lowest token usage for it's results.
`whole_document` - blends all sections into one vector which makes individual questions match less strongly as context 'blend' into each other. At floor 0.55 only 21 models were called and 11 out of 32 questions were refused.

The results 

## Why this one
<Two or three sentences. Which number decided it, and what you gave up.>
Chosen --floor 0.53 because the results for this floor have the strongest answer accuracy and refusal accuracy to token usage ratio compared to the other floors that were tested. 0.35 has higher token usage but the same accuracies and 0.55 has lower accuracies with far lower token usage than 0.35, 0.45, and 0.53. So the best of three was 0.53 for the floor would be the best choice. By choosing 0.53 as the floor we have retained the best possible accuracies for the call while maintaining the lowest possible token usages.

## Known weaknesses
<Questions the winner still misses, by kind. Which ones need hybrid retrieval, not better chunking?>
- The floor margin is 0.003: q06 (0.533) sits just above 0.53. Any change that lowers its score
slightly (rewording, new/different embedding model, new or edited documents) makes it a false refusal.
- q24 (exact-id, LP-3307): right chunk retrieved, but scored 0.280, below the floor, so refused
at the gate. Needs hybrid retrieval, not better chunking.
- q31 and q32 can't be separated from answerable questions by any floor as they reach the model
and rely on it to refuse. It did this in every run.
- The fallback, fixed_overlap_25, produced the only wrong answer in any run (q09 at floor 0.35): evidence wasn't retrieved, and the model answered from related chunks instead of refusing.


## Revisit when
<What would make this decision wrong: a new document type, a new embedding model, longer documents.>
- Answer accuracy drops on any of the future reruns.
- The embedding model changes: scores shift and the floor must be tuned again.
- Hybrid retrieval is added: q24 may clear the floor, and the floor itself may need resetting.
- The chunking strategy changes.
- If the eval set grows the floor needs to be revisited.