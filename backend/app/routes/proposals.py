from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.proposal import Proposal
from app.models.comment import Comment
from app.models.attachment import Attachment
from app.patterns.composite import ProposalComposite, ProposalLeaf
from app.patterns.facade import CongresoFacade
from app.schemas import ProposalCreate

router = APIRouter(prefix="/proposals", tags=["propuestas"])

@router.post("/")
def crear_propuesta(data: ProposalCreate, db: Session = Depends(get_db)):
    propuesta = Proposal(
        title=data.title,
        description=data.description,
        creator_name=data.creator_name
    )
    db.add(propuesta)
    db.commit()
    db.refresh(propuesta)
    facade = CongresoFacade(db)
    return facade.obtener_propuesta_decorada(propuesta)

@router.get("/")
def listar_propuestas(db: Session = Depends(get_db)):
    propuestas = db.query(Proposal).all()
    facade = CongresoFacade(db)
    return [facade.obtener_propuesta_decorada(p) for p in propuestas]

@router.get("/{propuesta_id}")
def obtener_propuesta(propuesta_id: int, db: Session = Depends(get_db)):
    propuesta = db.query(Proposal).filter(Proposal.id == propuesta_id).first()
    if not propuesta:
        raise HTTPException(status_code=404, detail="Propuesta no encontrada")

    comentarios = db.query(Comment).filter(Comment.proposal_id == propuesta_id).all()
    adjuntos = db.query(Attachment).filter(Attachment.proposal_id == propuesta_id).all()

    comp = ProposalComposite(propuesta.title, propuesta.description)
    for c in comentarios:
        comp.agregar(ProposalLeaf("comentario", c.content))
    for a in adjuntos:
        comp.agregar(ProposalLeaf("adjunto", a.filename))

    facade = CongresoFacade(db)
    resultado = facade.obtener_propuesta_decorada(propuesta)
    resultado["estructura"] = comp.get_info()
    return resultado

@router.post("/{propuesta_id}/congelar")
def congelar_propuesta(propuesta_id: int, db: Session = Depends(get_db)):
    propuesta = db.query(Proposal).filter(Proposal.id == propuesta_id).first()
    if not propuesta:
        raise HTTPException(status_code=404, detail="Propuesta no encontrada")
    try:
        facade = CongresoFacade(db)
        propuesta = facade.procesar_congelamiento(propuesta)
        return facade.obtener_propuesta_decorada(propuesta)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{propuesta_id}/congreso")
def obtener_formato_congreso(propuesta_id: int, db: Session = Depends(get_db)):
    propuesta = db.query(Proposal).filter(Proposal.id == propuesta_id).first()
    if not propuesta:
        raise HTTPException(status_code=404, detail="Propuesta no encontrada")
    try:
        facade = CongresoFacade(db)
        return facade.enviar_al_congreso(propuesta)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
