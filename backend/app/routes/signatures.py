from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.proposal import Proposal
from app.models.signature import Signature
from app.patterns.proxy import DocumentoProxy
from app.patterns.facade import CongresoFacade, LIMITE_FIRMAS
from app.schemas import SignatureCreate

router = APIRouter(prefix="/proposals", tags=["firmas"])

@router.post("/{propuesta_id}/firmas")
def firmar_propuesta(propuesta_id: int, data: SignatureCreate, db: Session = Depends(get_db)):
    propuesta = db.query(Proposal).filter(Proposal.id == propuesta_id).first()
    if not propuesta:
        raise HTTPException(status_code=404, detail="Propuesta no encontrada")

    proxy = DocumentoProxy({"status": propuesta.status})
    try:
        proxy.modificar({"accion": "firmar"})
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))

    firma_existente = db.query(Signature).filter(
        Signature.proposal_id == propuesta_id,
        Signature.citizen_id == data.citizen_id
    ).first()
    if firma_existente:
        raise HTTPException(status_code=400, detail="Este ciudadano ya firmó esta propuesta.")

    firma = Signature(
        proposal_id=propuesta_id,
        citizen_name=data.citizen_name,
        citizen_id=data.citizen_id
    )
    db.add(firma)
    propuesta.signature_count += 1
    db.commit()

    if propuesta.signature_count >= LIMITE_FIRMAS:
        facade = CongresoFacade(db)
        propuesta = facade.procesar_congelamiento(propuesta)

    db.refresh(propuesta)
    return {
        "mensaje": "Firma registrada exitosamente",
        "total_firmas": propuesta.signature_count,
        "estado": propuesta.status
    }

@router.get("/{propuesta_id}/firmas")
def listar_firmas(propuesta_id: int, db: Session = Depends(get_db)):
    propuesta = db.query(Proposal).filter(Proposal.id == propuesta_id).first()
    if not propuesta:
        raise HTTPException(status_code=404, detail="Propuesta no encontrada")
    firmas = db.query(Signature).filter(Signature.proposal_id == propuesta_id).all()
    return [{"id": f.id, "citizen_name": f.citizen_name, "signed_at": f.signed_at} for f in firmas]
