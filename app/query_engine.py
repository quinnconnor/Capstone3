import json
from .bedrock import BedrockClaude
from .router import route_question
from .embeddings import embed_query
from .opensearch_store import OpenSearchStore
from .redshift_store import RedshiftStore
from .sql_validator import validate_sql

class QueryEngine:
    def __init__(self): self.llm=BedrockClaude(); self.search=OpenSearchStore(); self.warehouse=RedshiftStore()
    def _sql(self,q):
        p=f"""Generate READ-ONLY Amazon Redshift SQL for this question.
Return ONLY JSON {{"sql":"...","tables":[...]}}.
Use only SELECT and one statement. Allowed conceptual tables:
customer_metrics(customer_id,churned,churn_date,segment,metadata_complete),
structured_records(source_key,row_number,data_json),
document_chunks(source_key,chunk_number,text,token_count),
dataset_metadata(source_key,column_name,data_type,required_metadata_present).
Question: {q}"""
        raw=self.llm.invoke(p,"sql_generation",450)["text"]
        try: sql=json.loads(raw)["sql"]
        except Exception as e: raise ValueError(f"Claude did not return valid SQL JSON: {raw}") from e
        v=validate_sql(sql)
        if not v["valid"]: raise ValueError(f"Generated SQL rejected: {v['reason']}")
        return sql
    def _docs(self,q): return self.search.semantic_search(embed_query(q),5)
    def answer(self,q):
        route=route_question(q); rows=[]; docs=[]; sql=None
        if route in {"redshift","both"}: sql=self._sql(q); rows=self.warehouse.execute(sql)
        if route in {"opensearch","both"}: docs=self._docs(q)
        evidence=[f"[DOC:{x['source_key']}#chunk-{x['chunk_number']}] {x['text']}" for x in docs]
        if rows: evidence.append(f"[SQL:query] {json.dumps(rows,default=str)}")
        p=f"""Answer using ONLY this evidence. Do not invent facts.
For document claims cite [DOC:...]. For warehouse claims cite [SQL:query].
If both sources are required, produce ONE integrated answer, not two separate answers.
Question: {q}
Evidence:
{chr(10).join(evidence)}"""
        final=self.llm.invoke(p,"contextual_response",800)
        return {"question":q,"route":route,"sql":sql,"sql_rows":rows,"documents":docs,"answer":final["text"]}
