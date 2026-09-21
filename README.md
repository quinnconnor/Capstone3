# Unit 3 Capstone — Intelligent Document Search Pipeline

## Architecture

```text
PDF/CSV/JSON -> S3 -> Lambda
                    PDF -> Textract -> chunk -> Sentence Transformers
                         -> RDS + OpenSearch
CSV/JSON -> Glue Crawler -> Glue Catalog -> Glue Spark ETL -> Redshift

Question -> Claude router
              |-> OpenSearch semantic search
              |-> SQL generation -> validator -> Redshift
              `-> both -> one Claude synthesis with DOC + SQL citations
```

## Important choices

* Embeddings use `sentence-transformers/all-MiniLM-L6-v2` locally, producing 384-dimensional vectors.
* Bedrock is used for Claude generation/classification/SQL generation, not embeddings.
* `BEDROCK_MODEL_ID` must be the inference-profile ID/ARN available to your account. The example follows the assignment's in-account ARN pattern.
* SQL is validated before execution and only a single SELECT is permitted.
* Every Claude call logs input/output tokens and an estimated cost to `token_usage.jsonl`.
* The ingestion Lambda is a container image because Sentence Transformers/PyTorch is too large for a normal Lambda zip.
* The two required synthesis questions are in `scripts/run_required_queries.py`.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
export AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
python scripts/test_bedrock.py
python scripts/test_sql_validator.py
pytest -q
```

Then configure AWS resources using `infra/README.md`, run the RDS/Redshift schemas, create the OpenSearch index, build/push the Lambda image, and configure the S3 trigger.

Upload:

```bash
aws s3 cp data/ s3://$S3_BUCKET/raw/ --recursive
```

Run an AI query:

```bash
python scripts/run_query.py "What does our retention strategy say about customer churn?"
```

Required synthesis tests:

```bash
python scripts/run_required_queries.py
```

Tokenomics:

```bash
python scripts/summarize_tokenomics.py --require-10
```

Charts:

```bash
python scripts/create_charts.py
```

## Required verification

Demonstrate that:
1. S3 contains PDF/CSV/JSON.
2. PDF -> Textract -> 500–1000-ish token chunks.
3. Embeddings are dimension 384.
4. RDS contains extracted text/chunks.
5. OpenSearch returns relevant semantic matches.
6. Glue crawler discovers schemas.
7. Glue ETL loads Redshift.
8. Redshift contains structured data and document vectors.
9. At least two Matplotlib charts are generated.
10. Bedrock smoke test succeeds.
11. SQL validation has 5+ cases including `SELECT ...; DROP TABLE ...;`.
12. Ten-query tokenomics summary is produced.
13. Both required synthesis questions produce one integrated answer with both `[DOC:...]` and `[SQL:...]` citations.
