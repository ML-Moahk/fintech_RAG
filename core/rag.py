import pdf_ingest
import embeddings
import VectorDB
import retrieval
import answer_generation

from pdf_ingest import extract_text_from_pdf
from embeddings import embed_chunks
from VectorDB import store_in_chroma
from pdf_ingest import chunk_text
from retrieval import retrieve_similar_chunks
from answer_generation import generate_answer

if __name__ == "__main__":
    pdf_path = r"C:\Users\Owner\Downloads\finance.pdf"
    

    #Extract text 
    extracted = extract_text_from_pdf(pdf_path)
    print("extraction succesfull")
    text = extracted['text']
    metadata = extracted ['metadata']
    print(f"length of text: {len(text)}")
    

    #Chunk Extracted Text 
    chunks = chunk_text(text)
    print ("chunk successful. Total chunk is {len(chunks)}")

    #Embed Chunked Text 
    embedded_chunks = embed_chunks(chunks, metadata)
    print ("embedding successful")
    print ("sample metadata:", embedded_chunks[0]['metadata'])

    #Store in DB
    store_in_chroma(embedded_chunks)
    print("Stored in Chroma")

    query = "who is a financial analyst"

    #Retrieve Similar chunks 
    retrieved_chunks = retrieve_similar_chunks(query)

    #Generate Answer 
    answer = generate_answer(query, retrieved_chunks)
    print (answer)



