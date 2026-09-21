from app.query_engine import QueryEngine
QUESTIONS=[
"Does our current customer churn rate (from the data warehouse) align with what our documented retention strategy says we should be seeing?",
"Based on our data governance policy documents, are any of the currently-ingested datasets missing required metadata fields (check against the Glue Catalog)?"]
e=QueryEngine()
for q in QUESTIONS:
    r=e.answer(q); print("="*80); print(q); print(r["answer"]); print("ROUTE:",r["route"]); print("SQL:",r["sql"])
