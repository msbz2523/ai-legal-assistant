from llama_index.llms.ollama import Ollama

def summarize_text(text: str) -> str:
    prompt = (
        "Fasse den folgenden Text sachlich, professionell und juristisch relevant zusammen. "
        "Konzentriere dich auf konkrete Inhalte wie: Pflichten, Fristen, Beträge, Forderungen oder Zuständigkeiten. "
        "Lass persönliche Anreden, Floskeln oder Meinungen weg. "
        "Die Antwort soll klar, knapp und auf Deutsch sein – ohne Kommentare oder Einleitungen.\n\n"
        f"{text}"
    )

    llm = Ollama(model="llama3")
    return str(llm.complete(prompt).text)
