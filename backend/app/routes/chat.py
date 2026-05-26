from fastapi import APIRouter # type: ignore
import chromadb # type: ignore
import ollama # type: ignore

router = APIRouter()

client = chromadb.Client()

collection = client.get_or_create_collection(
    name="lyra_notes"
)

@router.post("/ask")
async def ask_question(question: str):

    response = ollama.embed(
        model="nomic-embed-text",
        input=question
    )

    query_embedding = response["embeddings"][0]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=2
    )

    context = "\n".join(results["documents"][0])

    prompt = f"""
    You are an AI resume assistant.
    Answer only from the provided resume context.
    If answer is not found, say:
    "I could not find that information in the resume."

    Context:
    {context}

    Question:
    {question}

    Provide a short and professional and concise answer.
    """

    answer = ollama.chat(
        model="llama3",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return {
        "question": question,
        "retrieved_chunks": results["documents"][0],
        "answer": answer["message"]["content"]
    }