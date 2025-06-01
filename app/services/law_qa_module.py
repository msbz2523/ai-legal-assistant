from llama_index.core import Settings, StorageContext, load_index_from_storage
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama

def handle_legal_query_with_index(text: str) -> dict:
    Settings.embed_model = OllamaEmbedding(model_name="nomic-embed-text")

    prompt = (
        "Systemrolle: Du bist ein spezialisierter Fachanwalt für Zivilrecht in Deutschland.\n"
        "Deine Aufgabe ist es, rechtliche Probleme verständlich, sachlich und auf Grundlage aktueller Gesetze zu analysieren.\n"
        "Antworte auf Deutsch, vermeide juristische Fachsprache ohne Erklärung und gib konkrete Empfehlungen.\n"
        "Zitiere keine Paragraphen wörtlich, aber gib den zugehörigen Paragraph oder das Gesetz klar an.\n"
        "Vermeide Wiederholungen, allgemeine Definitionen oder hypothetische Beispiele.\n"
        "Nutze ausschließlich die folgenden Gesetzestexte als Grundlage.\n"
        f"\nProblem:\n{text}\n\n"
        "Was sollte die Person tun? Welche Rechte oder Möglichkeiten bestehen?"
    )

    storage_context = StorageContext.from_defaults(persist_dir="index_store")
    index = load_index_from_storage(storage_context)
    llm = Ollama(
        model="llama3",
        request_timeout=1200,
        temperature=0.3
    )
    query_engine = index.as_query_engine(llm=llm, similarity_top_k=5)
    response = query_engine.query(prompt)

    used_paragraphs = [node.node.text for node in response.source_nodes]

    return {
        "recommendation": str(response),
        "used_paragraphs": used_paragraphs
    }