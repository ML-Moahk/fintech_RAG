from core.get_openai_key import get_openai_client

client = get_openai_client()

def embed_chunks(
        chunks:list [str],
        metadata: dict,
        batch_size: int = 16) -> list[dict]:
    
    embedded_chunks = []

    for i in range (0, len(chunks), batch_size):
        batch = chunks[i:i + batch_size]
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=batch
        )
        for text, item in zip(batch, response.data):
            embedded_chunks.append({
                "text": text,
                "embedding": item.embedding,
                "metadata": metadata
            })

    return embedded_chunks


#
    