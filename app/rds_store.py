import psycopg
from .config import settings
class RDSStore:
    def __init__(self):
        self.info={"host":settings.rds_host,"port":settings.rds_port,"dbname":settings.rds_db,
                   "user":settings.rds_user,"password":settings.rds_password}
    def insert_document(self,source_key,text,content_type="application/pdf"):
        with psycopg.connect(**self.info) as c:
            with c.cursor() as cur:
                cur.execute("""INSERT INTO documents(source_key,content_type,raw_text)
                VALUES (%s,%s,%s) ON CONFLICT(source_key) DO UPDATE SET raw_text=EXCLUDED.raw_text
                RETURNING id""",(source_key,content_type,text))
                return cur.fetchone()[0]
    def insert_chunks(self,document_id,chunks):
        with psycopg.connect(**self.info) as c:
            with c.cursor() as cur:
                for x in chunks:
                    cur.execute("""INSERT INTO document_chunks(document_id,chunk_number,text,token_count)
                    VALUES (%s,%s,%s,%s) ON CONFLICT(document_id,chunk_number)
                    DO UPDATE SET text=EXCLUDED.text,token_count=EXCLUDED.token_count""",
                    (document_id,x["chunk_number"],x["text"],x["token_count"]))
