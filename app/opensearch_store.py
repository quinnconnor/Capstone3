import boto3
from opensearchpy import OpenSearch,RequestsHttpConnection
from requests_aws4auth import AWS4Auth
from .config import settings

class OpenSearchStore:
    def __init__(self):
        if not settings.opensearch_endpoint: raise ValueError("OPENSEARCH_ENDPOINT is required")
        host=settings.opensearch_endpoint.replace("https://","").replace("http://","").rstrip("/")
        c=boto3.Session().get_credentials()
        auth=AWS4Auth(c.access_key,c.secret_key,settings.region,"es",session_token=c.token)
        self.client=OpenSearch(hosts=[{"host":host,"port":443}],http_auth=auth,use_ssl=True,
            verify_certs=settings.opensearch_verify_certs,connection_class=RequestsHttpConnection,timeout=30)
    def ensure_index(self):
        if self.client.indices.exists(index=settings.opensearch_index): return
        self.client.indices.create(index=settings.opensearch_index,body={
            "settings":{"index":{"knn":True}},
            "mappings":{"properties":{
                "source_key":{"type":"keyword"},"document_id":{"type":"integer"},
                "chunk_number":{"type":"integer"},"text":{"type":"text"},"token_count":{"type":"integer"},
                "embedding":{"type":"knn_vector","dimension":settings.embedding_dim,
                    "method":{"name":"hnsw","engine":"nmslib","space_type":"cosinesimil"}}
            }}})
    def index_chunk(self,chunk_id,source_key,document_id,chunk):
        self.ensure_index()
        self.client.index(index=settings.opensearch_index,id=str(chunk_id),body={
            "source_key":source_key,"document_id":document_id,"chunk_number":chunk["chunk_number"],
            "text":chunk["text"],"token_count":chunk["token_count"],"embedding":chunk["embedding"]},refresh=True)
    def semantic_search(self,vector,k=5):
        self.ensure_index()
        r=self.client.search(index=settings.opensearch_index,body={"size":k,"query":{"knn":{"embedding":{"vector":vector,"k":k}}}})
        return [{"score":h["_score"],**h["_source"]} for h in r["hits"]["hits"]]
