import os 
from core.pdf_ingest import extract_text_from_pdf
from core.pdf_ingest import chunk_text
from core.embeddings import embed_chunks
from core.VectorDB import store_in_chroma


pdf_path = r"C:\Users\Owner\Downloads\finance.pdf"

def ingest_if_needed():
    from chromadb import PersistentClient
    chroma_client = PersistentClient(path=r"C:\Users\Owner\Fintech_RAG\Data")
    collection = chroma_client.get_or_create_collection("finance_doc")

    if collection.count() > 0:
        print("✅ Documents already ingested")
        return

    print("🚀 Ingesting documents...")

    extracted = extract_text_from_pdf(pdf_path)
    chunks = chunk_text(extracted["text"])
    embedded = embed_chunks(chunks, extracted["metadata"])
    store_in_chroma(embedded)

    print("✅ Ingestion complete")
