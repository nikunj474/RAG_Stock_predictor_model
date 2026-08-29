# Financial News Retrieval Pipeline

Semantic search over roughly a decade of financial news, so that a question like
*"what was being written about semiconductor supply chains in late 2022"* returns
the actual articles rather than a keyword match on "semiconductor".

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

The interesting problem here is not the model. It is that a few million
headlines will not fit in memory, a sequential embedding run takes days, and an
exact nearest-neighbour scan over a few million 768-dimension vectors is far too
slow to sit behind a query. This repository is the pipeline that deals with all
three.

---

## Pipeline

```
GDELT + Kaggle news        yfinance
   (~20 GB raw)          (S&P 500 OHLCV)
         │                     │
         ▼                     ▼
   cleaning + chunking    ticker cleaning
         │                     │
         ▼                     │
  DistilBERT embeddings        │
  768-d, CLS-pooled,           │
  L2-normalised, on GPU        │
         │                     │
         ▼                     ▼
     Postgres + pgvector on AWS RDS
                 │
                 ▼
        HNSW index (cosine)
                 │
                 ▼
       sub-second top-k retrieval
```

### 1. Ingest

`gdelt_pypi_2018_2023.ipynb` pulls roughly 20 GB of global news from the GDELT
API. `download_kaggle_news.py` fetches the Kaggle news-category dataset.
`S&P500.ipynb` pulls matching price history from yfinance.

### 2. Clean

`Cleaning/` handles the parts that are only obvious once the data is in front of
you: chunked processing so a 20 GB file never lands in memory at once, dropping
malformed and empty records, and normalising columns across two sources that
disagree about almost every field name.

### 3. Embed

`DistilBERT_run_gpu.py` is the production run. Headline and description are
concatenated, tokenised with padding and truncation, and pushed through
`distilbert-base-uncased`; the CLS token is taken as the sentence vector and L2
normalised so that cosine similarity reduces to a dot product.

Three details matter for throughput:

- **Super-batching.** Batches of 512 are grouped into super-batches of 10 and
  written to Parquet as a group, so the process does 1 write per 5,120 rows
  instead of 1 per 512.
- **Batch-level failure isolation.** A single oversized or malformed batch used
  to kill a multi-hour run. Failures are now caught per batch, recorded to a
  separate `failed_batches.parquet`, and the run continues.
- **Explicit memory reclamation.** `gc.collect()` and cache clearing between
  super-batches, because the accumulated activations otherwise exhaust 24 GB of
  VRAM partway through.

Run on a local RTX 3090. `Generate Embeddings/` keeps the earlier iterations
(first pass, multi-file pass, third pass) since the progression from a naive
loop to the batched version is most of the actual work.

### 4. Store and index

`ddl.py` and `ddl2.py` are the two schema revisions; the second normalises
company fundamentals away from the price series. `Insert into Database
(+cleaning)/` streams the Parquet output into Postgres with pgvector, in chunks,
with validation passes that check embedding dimensionality and row counts before
and after the load.

`HNSW_index.py` builds the index and documents the part that is easy to miss:
on a small RDS instance the default `maintenance_work_mem` is far too low to
build an HNSW graph over millions of vectors, so the file records the memory and
parallel-worker settings the build actually needed, alongside the `m` and
`ef_construction` values that were tried and what they cost.

---

## Running it

```bash
pip install -r requirements.txt
export RAG_DATA_DIR=/path/with/plenty/of/space
export PG_HOST=... PG_DB=... PG_USER=... PG_PASSWORD=...
python DistilBERT_run_gpu.py
```

All paths and credentials resolve through `config.py`. Nothing is hardcoded, and
nothing is committed: the raw corpora are tens of gigabytes and the generated
embeddings are larger still. 500-row samples of the cleaned news and ticker
tables live in [`data/samples/`](data/samples) so the schemas are readable
without downloading anything.

---

## Repository layout

| Path | Contents |
|:--|:--|
| `config.py` | Path and connection settings, read from the environment |
| `DistilBERT_run_gpu.py` | Production embedding run: batched, GPU, fault-isolated |
| `Generate Embeddings/` | Earlier embedding iterations, kept for the progression |
| `Cleaning/` | Chunked cleaning for the news and price datasets |
| `Insert into Database (+cleaning)/` | Load into Postgres, plus validation passes |
| `HNSW_index.py` | Index build and the RDS tuning it required |
| `ddl.py`, `ddl2.py` | Schema, first and second revision |
| `Play/` | API exploration notebooks |
| `cuda_test.py` | GPU availability check |

---

## Notes

Built as a graduate team project. My work was the embedding pipeline and the
vector store: the batched GPU run, the Postgres and pgvector schema, the load
and validation path, and the HNSW index tuning.

## Licence

MIT. See [LICENSE](LICENSE).
