from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.embeddings.ollama import OllamaEmbedding

if __name__ == "__main__":
    Settings.embed_model = OllamaEmbedding(model_name="nomic-embed-text")

    docs_dir = "deutsche_gesetze"

    documents = SimpleDirectoryReader(docs_dir).load_data()

    index = VectorStoreIndex.from_documents(documents)

    index.storage_context.persist(persist_dir="index_store")

    print("Gesetzesindex erfolgreich erstellt und gespeichert.")