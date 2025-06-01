import os
import json
from llama_index.core import VectorStoreIndex, Document, Settings
from llama_index.embeddings.ollama import OllamaEmbedding

Settings.embed_model = OllamaEmbedding(model_name="nomic-embed-text")

def load_laws_as_documents(folder="static/sample_laws"):
    documents = []
    for filename in os.listdir(folder):
        if filename.endswith(".json"):
            with open(os.path.join(folder, filename), encoding="utf-8") as f:
                laws = json.load(f)
                for law in laws:
                    content = f"{law['gesetz']} {law['paragraph']} – {law['titel']}\n{law['text']}"
                    documents.append(Document(text=content))
    return documents

docs = load_laws_as_documents()
index = VectorStoreIndex.from_documents(docs)
index.storage_context.persist("index_store")
print("RAG-Index erfolgreich erstellt und gespeichert.")