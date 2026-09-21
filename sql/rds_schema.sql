CREATE TABLE IF NOT EXISTS documents (
 id BIGSERIAL PRIMARY KEY, source_key TEXT NOT NULL UNIQUE, content_type TEXT NOT NULL,
 raw_text TEXT NOT NULL, created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE TABLE IF NOT EXISTS document_chunks (
 id BIGSERIAL PRIMARY KEY, document_id BIGINT NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
 chunk_number INTEGER NOT NULL, text TEXT NOT NULL, token_count INTEGER NOT NULL,
 created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(), UNIQUE(document_id,chunk_number)
);
CREATE INDEX IF NOT EXISTS document_chunks_document_idx ON document_chunks(document_id);
