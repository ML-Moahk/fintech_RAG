import pdfplumber
import os

pdf_path = "finance_data/finance.pdf"
#define a function to extract text from pdf 
def extract_text_from_pdf(pdf_path: str) -> str: 
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        metadata = {
            "document_name" : os.path.basename(pdf_path),
            "source_type" : "pdf"
        }
    return{
        "text": text,
        "metadata": metadata
    }

    
extracted = extract_text_from_pdf(pdf_path)
print("pdf extracted successfully")

text = extracted['text']
metada = extracted['metadata']
print(f'this is the lenth of text: {len(text)}')

#Now we add the code for chunking the text

def chunk_text(
        text:str,
        chunk_size: int=1000,
        chunk_overlap: int=200
):
    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be smaller than chunk_size")
    chunks = []
    start = 0
    text_length = len(text)
    while start < text_length:
        end = start + chunk_size
        chunks.append (text[start:end])
        start = end - chunk_overlap
    return chunks 


chunks = chunk_text(text)
print (f"chunking successful.Total chunk is {len(chunks)} ")







