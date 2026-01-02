
import chromadb
from core.get_openai_key import get_openai_client
openai_client = get_openai_client()

chroma_path = r"C:\Users\Owner\Fintech_RAG\Data"
collection_name  = "finance_doc"
confidence_threshold = 1.0

def retrieve_similar_chunks(
    query: str,
    top_k: int = 3
) -> list[dict]:
    
    # 1. Embed the query
    embedding_response = openai_client.embeddings.create(
        model="text-embedding-3-small",
        input=query
    )
    query_embedding = embedding_response.data[0].embedding
    
    
    # 2. Connect to Chroma
    chroma_client = chromadb.PersistentClient(
        path=chroma_path
    )

    collection = chroma_client.get_or_create_collection(
        name=collection_name
    )
    # 3. Query Chroma 
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results = top_k,
        include = ["documents", "metadatas", "distances"]
    )
    distances = results["distances"][0]

    # 4. Confidence check
    best_distance = min(distances)

    if best_distance > confidence_threshold:
        return []  # Not confident enough
    
    # 5. Format results
    retrieved_chunks = []

    for i in range(len(results["documents"][0])):
        retrieved_chunks.append({
            "text": results["documents"][0][i],
            "metadata": results["metadatas"][0][i],
            #"distance": results["distances"][0][i] #distance changed to [i] to be more strict
            "distance": [i]
        })

    return retrieved_chunks 

