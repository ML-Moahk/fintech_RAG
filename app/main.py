from fastapi import FastAPI

app = FastAPI(title="RAG PDF Assistant")
@app.get("/health")
def health_check():
    return {"status":"ok"}

from fastapi import APIRouter
from pydantic import BaseModel
from core.retrieval import retrieve_similar_chunks
from core.answer_generation import generate_answer

router = APIRouter()
class QuestionRequest(BaseModel):
    question : str 
@router.post("/ask")
def ask_questions (request:QuestionRequest):
    #1. Extract Question 
    question = request.question
    
    #2. Retrieve Relvant Chunks 
    chunks = retrieve_similar_chunks(question)
    
    if not chunks :
        return {
            "answer": "I do not have enough information to answer this question",
            "source": []
        }
    
    #3. Generate Answer
    answer = generate_answer(question, chunks)

    #4. Return Response 
    return{
        "question": question,
        "answer": answer,
        "sources": [c["metadata"] for c in chunks]
    }
app.include_router(router)