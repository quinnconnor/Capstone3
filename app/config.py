from dataclasses import dataclass
import os
from dotenv import load_dotenv
load_dotenv()

@dataclass(frozen=True)
class Settings:
    region: str = os.getenv("AWS_REGION","us-east-1")
    account_id: str = os.getenv("AWS_ACCOUNT_ID","")
    s3_bucket: str = os.getenv("S3_BUCKET","")
    s3_raw_prefix: str = os.getenv("S3_RAW_PREFIX","raw/")
    bedrock_model_id: str = os.getenv("BEDROCK_MODEL_ID","")
    embedding_model: str = os.getenv("EMBEDDING_MODEL","sentence-transformers/all-MiniLM-L6-v2")
    embedding_dim: int = int(os.getenv("EMBEDDING_DIM","384"))
    rds_host: str = os.getenv("RDS_HOST","")
    rds_port: int = int(os.getenv("RDS_PORT","5432"))
    rds_db: str = os.getenv("RDS_DB","documents")
    rds_user: str = os.getenv("RDS_USER","")
    rds_password: str = os.getenv("RDS_PASSWORD","")
    opensearch_endpoint: str = os.getenv("OPENSEARCH_ENDPOINT","")
    opensearch_index: str = os.getenv("OPENSEARCH_INDEX","document_chunks")
    opensearch_verify_certs: bool = os.getenv("OPENSEARCH_VERIFY_CERTS","true").lower()=="true"
    redshift_cluster_id: str = os.getenv("REDSHIFT_CLUSTER_ID","")
    redshift_workgroup_name: str = os.getenv("REDSHIFT_WORKGROUP_NAME","")
    redshift_database: str = os.getenv("REDSHIFT_DATABASE","dev")
    redshift_secret_arn: str = os.getenv("REDSHIFT_SECRET_ARN","")
    redshift_db_user: str = os.getenv("REDSHIFT_DB_USER","")
    redshift_data_api_timeout: int = int(os.getenv("REDSHIFT_DATA_API_TIMEOUT","60"))
    token_log_path: str = os.getenv("TOKEN_LOG_PATH","token_usage.jsonl")
    input_price: float = float(os.getenv("BEDROCK_INPUT_PRICE_PER_MILLION","3"))
    output_price: float = float(os.getenv("BEDROCK_OUTPUT_PRICE_PER_MILLION","15"))
settings=Settings()
