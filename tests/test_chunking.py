from app.chunking import chunk_text
def test_chunking():
    chunks=chunk_text("This is a sentence. "*700)
    assert chunks
    assert all(0<x["token_count"]<=900 for x in chunks)
