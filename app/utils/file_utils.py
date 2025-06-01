from fastapi import UploadFile

async def read_upload_file(upload_file: UploadFile) -> bytes:
    """
    Liest den Dateiinhalt vollständig in den Speicher (RAM),
    ohne ihn dauerhaft zu speichern – DSGVO-konform.
    """
    return await upload_file.read()