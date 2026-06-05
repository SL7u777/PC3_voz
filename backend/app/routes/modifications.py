from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import get_db
from app.models.proposal import Proposal
from app.models.modification import Modification
from app.patterns.proxy import DocumentoProxy

router = APIRouter(prefix="/proposals", tags=["modificaciones"])

class ModificationCreate(BaseModel):
    author_name: str
    section: str
    proposed_change: str

@router.post("/{propuesta_id}/modificaciones")
def agregar_modificacion(propuesta_id: int, data: ModificationCreate, db: Session = Depends(get_db)):
    propuesta = db.query(Proposal).filter(Proposal.id == propuesta_id).first()
    if not propuesta:
        raise HTTPException(status_code=404, detail="Propuesta no encontrada")

    proxy = DocumentoProxy({"status": propuesta.status})
    try:
        proxy.modificar({"accion": "modificar"})
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))

    mod = Modification(
        proposal_id=propuesta_id,
        author_name=data.author_name,
        section=data.section,
        proposed_change=data.proposed_change
    )
    db.add(mod)
    db.commit()
    db.refresh(mod)
    return {"mensaje": "Modificación registrada", "id": mod.id}

@router.get("/{propuesta_id}/modificaciones")
def listar_modificaciones(propuesta_id: int, db: Session = Depends(get_db)):
    propuesta = db.query(Proposal).filter(Proposal.id == propuesta_id).first()
    if not propuesta:
        raise HTTPException(status_code=404, detail="Propuesta no encontrada")
    mods = db.query(Modification).filter(Modification.proposal_id == propuesta_id).all()
    return [{"id": m.id, "author": m.author_name, "section": m.section, "proposed_change": m.proposed_change, "created_at": m.created_at} for m in mods]
