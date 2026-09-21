CREATE TABLE IF NOT EXISTS customer_metrics (
 customer_id VARCHAR(128), churned INTEGER, churn_date DATE, segment VARCHAR(128), metadata_complete BOOLEAN
);
CREATE TABLE IF NOT EXISTS structured_records (
 source_key VARCHAR(1024), row_number BIGINT, data_json VARCHAR(65535)
);
CREATE TABLE IF NOT EXISTS document_chunks (
 source_key VARCHAR(1024), chunk_number INTEGER, text VARCHAR(65535),
 token_count INTEGER, embedding VARCHAR(65535)
);
CREATE TABLE IF NOT EXISTS dataset_metadata (
 source_key VARCHAR(1024), column_name VARCHAR(512), data_type VARCHAR(256),
 required_metadata_present BOOLEAN
);
CREATE TABLE IF NOT EXISTS etl_audit (
 source_table VARCHAR(512), row_count BIGINT, processed_at TIMESTAMP DEFAULT GETDATE()
);
