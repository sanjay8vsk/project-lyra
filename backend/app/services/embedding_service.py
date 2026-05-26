import ollama # type: ignore
import chromadb # type: ignore

client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_or_create_collection(
    name="lyra_notes"
)

def store_chunks(chunks):

    ids = []

    embeddings = []

    for i, chunk in enumerate(chunks):

        response = ollama.embeddings(
            model="nomic-embed-text",
            prompt=chunk
        )

        embedding = response["embedding"]

        ids.append(f"chunk_{i}")
        embeddings.append(embedding)

    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=chunks
    )

    return True