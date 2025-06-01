import os
import requests
from bs4 import BeautifulSoup

GESETZE = {
    "bgb": "https://www.gesetze-im-internet.de/bgb/",
    "stgb": "https://www.gesetze-im-internet.de/stgb/",
    "sgb_1": "https://www.gesetze-im-internet.de/sgb_1/",
    "sgb_2": "https://www.gesetze-im-internet.de/sgb_2/",
    "sgb_3": "https://www.gesetze-im-internet.de/sgb_3/",
    "sgb_4": "https://www.gesetze-im-internet.de/sgb_4/",
    "sgb_5": "https://www.gesetze-im-internet.de/sgb_5/",
    "sgb_6": "https://www.gesetze-im-internet.de/sgb_6/",
    "sgb_7": "https://www.gesetze-im-internet.de/sgb_7/",
    "sgb_8": "https://www.gesetze-im-internet.de/sgb_8/",
    "sgb_9": "https://www.gesetze-im-internet.de/sgb_ix_2001/",
    "sgb_10": "https://www.gesetze-im-internet.de/sgb_10/",
    "sgb_11": "https://www.gesetze-im-internet.de/sgb_11/",
    "stvg": "https://www.gesetze-im-internet.de/stvg/",
    "stvo": "https://www.gesetze-im-internet.de/stvo_2013/"
}

SAVE_DIR = "deutsche_gesetze"
os.makedirs(SAVE_DIR, exist_ok=True)

def scrape_gesetz(name, url):
    try:
        res = requests.get(url)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")

        content = soup.get_text(separator="\n")
        clean = '\n'.join([line.strip() for line in content.splitlines() if line.strip()])

        filepath = os.path.join(SAVE_DIR, f"{name}.txt")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(clean)

        print(f"{name} gespeichert ({len(clean)} Zeichen)")
    except Exception as e:
        print(f"Fehler bei {name}: {e}")

if __name__ == "__main__":
    for name, url in GESETZE.items():
        scrape_gesetz(name, url)
    print("Alle Gesetzestexte wurden gespeichert.")
