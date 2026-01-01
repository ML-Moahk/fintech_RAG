#Guardrails (Non-Negotiable)Your system must enforce:
#Answer only from provided context,If context is insufficient → say so,
#No hallucination,No external knowledgeThese guardrails matter for fintech, 
#compliance, audits, and real jobs.

from core.get_openai_key import get_openai_client
openai_client = get_openai_client()

def generate_answer(
        query: str,
        retrieved_chunks: list[dict]
) -> str:
    """ Generate answer strictly on retrieved context"""
    if not retrieved_chunks:
        return "I could nto find relevant information in the provided documents"
    
     # 1. Build context string
    context = "\n\n".join(
        f"Source {i+1}:\n{chunk['text']}"
        for i, chunk in enumerate(retrieved_chunks)
    )
     
     # 2. System instruction (this is critical)
    system_prompt = (
        "You are a financial document assistant.\n"
        "Answer the user's question using ONLY the information provided in the context.\n"
        "If the answer is not contained in the context, say you do not know.\n"
        "Do NOT guess or add external information."
    )
      # 3. User prompt
    user_prompt = (
        f"Context:\n{context}\n\n"
        f"Question:\n{query}"
    )
     # 4. Generate Answer
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system",
            "content": system_prompt},
            {"role": "user",
             "content":user_prompt}
        ],
        temperature= 0
    )
    answer_text = response.choices[0].message.content.strip()

    # 5. Add document source to answer. 
    #5.1 Extract unique sources from metadata
    sources = sorted({
        chunk["metadata"]["document_name"]
        for chunk in retrieved_chunks
        if "document_name" in chunk["metadata"]
    })

    # 5.2. Append citations
    if sources:
        sources_text = "\n".join(f"- {src}" for src in sources)
        answer_text += f"\n\nSources:\n{sources_text}"

    return answer_text

