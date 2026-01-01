import os 
import chromadb
chroma_client = chromadb.PersistentClient(
        path=r"C:\Users\Owner\Fintech_RAG\Data"
    )

collection = chroma_client.get_collection(name="finance_doc")

print("Collection name:", collection.name)
print("Total documents stored:", collection.count())
print(chroma_client.list_collections())