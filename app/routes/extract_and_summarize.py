from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from app.services.ocr_service import extract_text_from_image
from app.services.pdf_service import extract_text_from_pdf
from app.services.summarization_service import summarize_text
from app.services.translation_service import translate_to_arabic
from app.utils.text_cleaner import clean_extracted_text
from app.services.law_qa_module import handle_legal_query_with_index
from app.services.validation_service import validate_output

router = APIRouter()

DISCLAIMER = "Diese Einschätzung ersetzt keine anwaltliche Beratung (§ 1 RDG)."

@router.post("/api/extract-summarize")
async def extract_and_summarize(
    file: UploadFile = File(...),
    language: str = Form(...),
    mode: str = Form("summary")
):
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded.")

    if language not in ["de", "ar"]:
        raise HTTPException(status_code=400, detail="Language must be 'de' or 'ar'.")

    try:
        contents = await file.read()

        if file.filename.lower().endswith(".pdf"):
            extracted_text = extract_text_from_pdf(contents)
        else:
            extracted_text = extract_text_from_image(contents)

        if not extracted_text.strip():
            return JSONResponse(content={
                "original_text": "",
                "summary": "Kein Text im Dokument erkannt.",
                "disclaimer": DISCLAIMER
            })

        extracted_text = clean_extracted_text(extracted_text)

        if len(extracted_text) < 20:
            return JSONResponse(content={
                "original_text": extracted_text,
                "summary": "Extrahierter Text ist zu kurz.",
                "disclaimer": DISCLAIMER
            })

        if mode == "summary":
            german_summary = summarize_text(extracted_text)
            if len(german_summary.split()) < 5:
                return JSONResponse(content={
                    "original_text": extracted_text,
                    "summary": "Zusammenfassung zu kurz oder unklar.",
                    "disclaimer": DISCLAIMER
                })
            summary = translate_to_arabic(german_summary) if language == "ar" else german_summary
            return JSONResponse(content={
                "original_text": extracted_text,
                "summary": summary,
                "disclaimer": DISCLAIMER
            })

        elif mode == "legal_advice":
            result = handle_legal_query_with_index(extracted_text)
            recommendation_text = result["recommendation"]

            if not validate_output(recommendation_text):
                raise HTTPException(
                    status_code=500,
                    detail="Antwort enthält riskante Formulierungen und wurde blockiert (RDG-Schutz)."
                )

            if language == "ar":
                recommendation_text = translate_to_arabic(recommendation_text)

            return JSONResponse(content={
                "original_text": extracted_text,
                "legal_recommendation": recommendation_text,
                "used_paragraphs": result["used_paragraphs"],
                "disclaimer": DISCLAIMER
            })

        # Fallback – nur Originaltext
        return JSONResponse(content={
            "original_text": extracted_text,
            "disclaimer": DISCLAIMER
        })

    except Exception as e:
        print(f"Server Fehler: {e}")
        raise HTTPException(status_code=500, detail=f"Extraction or summarization failed: {str(e)}")