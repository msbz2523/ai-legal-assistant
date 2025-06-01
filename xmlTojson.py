import os
import json
import xml.etree.ElementTree as ET

xml_folder = "xml_laws"
output_folder = "static/sample_laws"
os.makedirs(output_folder, exist_ok=True)

law_mapping = {
    "BJNR024820988": "SGB V (Krankenversicherung)",
    "BJNR101500994": "SGB XI (Pflegeversicherung)",
    "BJNR001950896": "Bürgerliches Gesetzbuch (BGB)"
}

def parse_xml_to_json(xml_path, gesetz_name):
    tree = ET.parse(xml_path)
    root = tree.getroot()

    result = []
    for norm in root.findall(".//norm"):
        paragraph = norm.find(".//enbez")
        titel = norm.find(".//titel")
        
        paragraphs = [p.text.strip() for p in norm.findall(".//textdaten/text/Content/P") if p.text]
        full_text = " ".join(paragraphs) if paragraphs else ""

        paragraph_text = paragraph.text.strip() if paragraph is not None else ""

        # Filter: Nur echte Paragraphen mit § und echtem Text
        if paragraph_text.startswith("§") and full_text:
            result.append({
                "gesetz": gesetz_name,
                "paragraph": paragraph_text,
                "titel": titel.text.strip() if titel is not None else "",
                "text": full_text
            })

    return result

def convert_all():
    for filename in os.listdir(xml_folder):
        if filename.endswith(".xml"):
            file_path = os.path.join(xml_folder, filename)
            file_base = filename.replace(".xml", "")

            gesetz_name = law_mapping.get(file_base, "Unbekanntes Gesetz")
            json_data = parse_xml_to_json(file_path, gesetz_name)

            output_filename = file_base + ".json"
            output_path = os.path.join(output_folder, output_filename)

            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(json_data, f, ensure_ascii=False, indent=2)

            print(f"✅ Umgewandelt: {output_filename}")

if __name__ == "__main__":
    convert_all()