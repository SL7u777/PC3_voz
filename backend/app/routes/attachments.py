import os
import shutil
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.proposal import Proposal
from app.models.attachment import Attachment
from app.patterns.proxy import DocumentoProxy

router = APIRouter(prefix="/proposals", tags=["adjuntos"])

UPLOAD_DIR = "uploads"
ALLOWED_TYPES = {
    "image/jpeg", "image/png", "application/pdf",
    "video/mp4", "audio/mpeg", "audio/mp3"
}

@router.post("/{propuesta_id}/adjuntos")
def subir_adjunto(propuesta_id: int, archivo: UploadFile = File(...), db: Session = Depends(get_db)):
    propuesta = db.query(Proposal).filter(Proposal.id == propuesta_id).first()
    if not propuesta:
        raise HTTPException(status_code=404, detail="Propuesta no encontrada")

    proxy = DocumentoProxy({"status": propuesta.status})
    try:
        proxy.modificar({"accion": "adjuntar"})
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))

    if archivo.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="Tipo de archivo no permitido. Use: jpg, png, pdf, mp4, mp3.")

    carpeta = os.path.join(UPLOAD_DIR, str(propuesta_id))
    os.makedirs(carpeta, exist_ok=True)
    ruta = os.path.join(carpeta, archivo.filename)

    with open(ruta, "wb") as f:
        shutil.copyfileobj(archivo.file, f)

    adjunto = Attachment(
        proposal_id=propuesta_id,
        filename=archivo.filename,
        file_type=archivo.content_type,
        file_path=ruta
    )
    db.add(adjunto)
    db.commit()
    db.refresh(adjunto)
    return {"mensaje": "Adjunto subido exitosamente", "id": adjunto.id, "filename": adjunto.filename}

@router.get("/{propuesta_id}/adjuntos")
def listar_adjuntos(propuesta_id: int, db: Session = Depends(get_db)):
    propuesta = db.query(Proposal).filter(Proposal.id == propuesta_id).first()
    if not propuesta:
        raise HTTPException(status_code=404, detail="Propuesta no encontrada")
    adjuntos = db.query(Attachment).filter(Attachment.proposal_id == propuesta_id).all()
    return [{"id": a.id, "filename": a.filename, "file_type": a.file_type, "uploaded_at": a.uploaded_at} for a in adjuntos]
