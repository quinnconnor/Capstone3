import os,boto3
from app.chunking import chunk_text
from app.embeddings import embed_texts
from app.rds_store import RDSStore
from app.opensearch_store import OpenSearchStore
s3=boto3.client("s3"); textract=boto3.client("textract")

def lambda_handler(event,context):
    rds=RDSStore(); search=OpenSearchStore(); out=[]
    for rec in event.get("Records",[]):
        bucket=rec["s3"]["bucket"]["name"]; key=rec["s3"]["object"]["key"].replace("%20"," ")
        if not key.startswith(os.getenv("S3_RAW_PREFIX","raw/")): continue
        if not key.lower().endswith(".pdf"):
            out.append({"key":key,"action":"deferred_to_glue"}); continue
        tx=textract.detect_document_text(Document={"S3Object":{"Bucket":bucket,"Name":key}})
        text="\n".join(b["Text"] for b in tx.get("Blocks",[]) if b.get("BlockType")=="LINE" and "Text" in b)
        chunks=chunk_text(text); vectors=embed_texts([x["text"] for x in chunks])
        for x,v in zip(chunks,vectors): x["embedding"]=v
        doc_id=rds.insert_document(key,text); rds.insert_chunks(doc_id,chunks)
        for x in chunks: search.index_chunk(f"{doc_id}-{x['chunk_number']}",key,doc_id,x)
        out.append({"key":key,"action":"processed","document_id":doc_id,"chunks":len(chunks),
                    "embedding_dimension":len(vectors[0]) if vectors else 0})
    return {"statusCode":200,"processed":out}
