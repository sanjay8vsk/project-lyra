import ollama # type: ignore
import chromadb # type: ignore

client = chromadb.Client()

collection = client.get_or_create_collection(
    name="lyra_notes"
)

def store_chunks(chunks):

    ids = [f"chunk_{i}" for i in range(len(chunks))]

    embeddings = []

    for chunk in chunks:

        response = ollama.embed(
            model="nomic-embed-text",
            input=chunk
        )

        embeddings.append(response["embeddings"][0])

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings
    )

    return True