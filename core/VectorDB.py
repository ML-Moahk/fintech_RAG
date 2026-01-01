import chromadb
import uuid
def store_in_chroma(embedded_chunks):

    if not embedded_chunks:
        raise ValueError("No embedded chunks to store.")
    
    chroma_client = chromadb.PersistentClient(
        path = r"C:\Users\Owner\Fintech_RAG\Data"
    )

    collection = chroma_client.get_or_create_collection(
        name="finance_doc"
    )

    collection.add(
        documents=[item['text']for item in embedded_chunks],
        embeddings=[item['embedding'] for item in embedded_chunks],
        metadatas=[item['metadata'] for item in embedded_chunks],
        ids=[str(uuid.uuid4()) for _ in embedded_chunks] 
    )
    
