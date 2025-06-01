from llama_index.core import Settings, StorageContext, load_index_from_storage
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama

def handle_legal_query_with_index(text: str) -> dict:
    Settings.embed_model = OllamaEmbedding(model_name="nomic-embed-text")

    # Prompt für strikte Nutzung des Indexes
    prompt = (
        "Du bist ein juristischer Assistent in Deutschland."
        " Die folgende Person hat ein konkretes rechtliches Problem und bittet um eine rechtliche Einschätzung."
        " Deine Antwort muss ausschließlich auf DEUTSCH erfolgen."
        " Verwende ausschließlich die bereitgestellten Gesetzestexte aus dem Index."
        " Verwende keine eigenen Kenntnisse oder Vorwissen."
        " Wenn die Antwort nicht aus dem bereitgestellten Gesetzestext abgeleitet werden kann, schreibe: 'Nicht im Index vorhanden'."
        " Verwende keine juristischen Fachbegriffe ohne Erklärung."
        " Gib am Ende die verwendeten Paragraphen oder Gesetze an, aber ohne vollständige Zitate."
        f"\n\nProblem:\n{text}\n\n"
        "Was sollte die Person tun? Welche Rechte oder Möglichkeiten bestehen?"
    )

    # Lade gespeicherten Gesetzesindex
    storage_context = StorageContext.from_defaults(persist_dir="index_store")
    index = load_index_from_storage(storage_context)

    llm = Ollama(model="llama3", request_timeout=1200)

    # Query Engine mit strikten Einstellungen für reines RAG
    query_engine = index.as_query_engine(
        llm=llm,
        similarity_top_k=5,
        response_mode="compact",       # Nur komprimierte Antwort aus relevanten Texten
        node_postprocessors=[]         # Keine Rekombination oder Umsortierung
    )

    # Führe die Abfrage durch
    response = query_engine.query(prompt)

    # Liste der tatsächlich genutzten Gesetzesabschnitte (source documents)
    used_paragraphs = [node.node.text for node in response.source_nodes]

    return {
        "recommendation": str(response),
        "used_paragraphs": used_paragraphs
    }