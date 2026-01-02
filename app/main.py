from fastapi import FastAPI, APIRouter
from pydantic import BaseModel

from core.retrieval import retrieve_similar_chunks
from core.answer_generation import generate_answer
from core.ingest_pipeline import ingest_if_needed

# -------------------------
# Create app ONCE
# -------------------------
app = FastAPI(title="RAG PDF Assistant")

# -------------------------
# Startup ingestion
# -------------------------
@app.on_event("startup")
def startup_event():
    ingest_if_needed()

# -------------------------
# Health check
# -------------------------
@app.get("/health")
def health_check():
    return {"status": "ok"}

# -------------------------
# API Router
# -------------------------
router = APIRouter()

class QuestionRequest(BaseModel):
    question: str

@router.post("/ask")
def ask_questions(request: QuestionRequest):
    question = request.question

    # Retrieve chunks
    chunks = retrieve_similar_chunks(question)

    if not chunks:
        return {
            "answer": "I do not have enough information to answer this question",
            "sources": []
        }

    # Generate answer
    answer = generate_answer(question, chunks)

    return {
        "question": question,
        "answer": answer,
        "sources": [c["metadata"] for c in chunks]
    }

# -------------------------
# Register router
# -------------------------
app.include_router(router)
