from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.proposal import Proposal
from app.models.comment import Comment
from app.patterns.proxy import DocumentoProxy
from app.schemas import CommentCreate

router = APIRouter(prefix="/proposals", tags=["comentarios"])

@router.post("/{propuesta_id}/comentarios")
def agregar_comentario(propuesta_id: int, data: CommentCreate, db: Session = Depends(get_db)):
    propuesta = db.query(Proposal).filter(Proposal.id == propuesta_id).first()
    if not propuesta:
        raise HTTPException(status_code=404, detail="Propuesta no encontrada")

    proxy = DocumentoProxy({"status": propuesta.status})
    try:
        proxy.modificar({"accion": "comentar"})
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))

    comentario = Comment(
        proposal_id=propuesta_id,
        author_name=data.author_name,
        content=data.content
    )
    db.add(comentario)
    db.commit()
    db.refresh(comentario)
    return {"mensaje": "Comentario agregado", "id": comentario.id}

@router.get("/{propuesta_id}/comentarios")
def listar_comentarios(propuesta_id: int, db: Session = Depends(get_db)):
    propuesta = db.query(Proposal).filter(Proposal.id == propuesta_id).first()
    if not propuesta:
        raise HTTPException(status_code=404, detail="Propuesta no encontrada")
    comentarios = db.query(Comment).filter(Comment.proposal_id == propuesta_id).all()
    return [{"id": c.id, "author": c.author_name, "content": c.content, "created_at": c.created_at} for c in comentarios]
