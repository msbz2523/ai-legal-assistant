from llama_index.core import Settings, StorageContext, load_index_from_storage
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama

Settings.embed_model = OllamaEmbedding(model_name="nomic-embed-text")
storage_context = StorageContext.from_defaults(persist_dir="index_store")
index = load_index_from_storage(storage_context)

llm = Ollama(model="llama3", request_timeout=1200)
query_engine = index.as_query_engine(llm=llm, similarity_top_k=5)

with open("frage.txt", "r", encoding="utf-8") as f:
    frage = f.read()

prompt = (
    "Du bist ein juristischer Assistent in Deutschland."
    " Die folgende Person hat ein konkretes rechtliches Problem und bittet um eine klare Einschätzung."
    " Deine Antwort soll ausschließlich auf DEUTSCH erfolgen."
    " Formuliere eine hilfreiche Empfehlung, sachlich, direkt und gut verständlich für juristische Laien."
    " Verwende keine juristischen Fachausdrücke ohne Erklärung."
    " Vermeide allgemeine Definitionen, irrelevante Erklärungen oder fiktive Beispiele."
    " Wiederhole den Sachverhalt NICHT und zitiere KEINE Gesetzesparagraphen wörtlich."
    " Gib aber den passenden Paragraph oder Gesetz an, auf dem deine Antwort beruht."
    " Nutze ausschließlich die folgenden Gesetzestexte als Grundlage für deine Antwort.\n\n"
    f"Problem:\n{frage}\n\n"
    "Was sollte die Person tun? Welche Rechte oder Möglichkeiten bestehen?"
)

response = query_engine.query(prompt)

print("\nAntwort:")
print(response)

print("\nVerwendete Paragraphen:")
for node in response.source_nodes[:3]:
    print(node.node.text[:300])
    print("---")
