import hashlib
import json
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.proposal import Proposal
from app.patterns.proxy import DocumentoProxy
from app.patterns.decorator import ProposalConcreto, TimestampDecorator, FirmasDecorator, EstadoDecorator
from app.patterns.adapter import FormatoInterno, CongresoAdapter

LIMITE_FIRMAS = 25000

class CongresoFacade:
    def __init__(self, db: Session):
        self._db = db

    def obtener_propuesta_decorada(self, propuesta: Proposal) -> dict:
        data = {
            "id": propuesta.id,
            "title": propuesta.title,
            "description": propuesta.description,
            "creator_name": propuesta.creator_name,
            "status": propuesta.status,
            "signature_count": propuesta.signature_count,
            "created_at": propuesta.created_at,
            "deadline": propuesta.deadline,
            "frozen_hash": propuesta.frozen_hash,
        }
        wrapped = ProposalConcreto(data)
        wrapped = TimestampDecorator(wrapped)
        wrapped = FirmasDecorator(wrapped)
        wrapped = EstadoDecorator(wrapped)
        return wrapped.get_data()

    def intentar_modificacion(self, propuesta: Proposal, datos: dict) -> dict:
        data = {"status": propuesta.status}
        proxy = DocumentoProxy(data)
        return proxy.modificar(datos)

    def procesar_congelamiento(self, propuesta: Proposal) -> Proposal:
        if propuesta.signature_count < LIMITE_FIRMAS:
            raise ValueError(f"Se requieren {LIMITE_FIRMAS} firmas. Actuales: {propuesta.signature_count}")
        if propuesta.status == "congelada":
            raise ValueError("La propuesta ya está congelada.")

        contenido = json.dumps({
            "id": propuesta.id,
            "title": propuesta.title,
            "description": propuesta.description,
            "creator_name": propuesta.creator_name,
            "signature_count": propuesta.signature_count,
            "timestamp": datetime.utcnow().isoformat(),
        }, ensure_ascii=False)

        propuesta.frozen_hash = hashlib.sha256(contenido.encode()).hexdigest()
        propuesta.status = "congelada"
        self._db.commit()
        self._db.refresh(propuesta)
        return propuesta

    def enviar_al_congreso(self, propuesta: Proposal) -> dict:
        if propuesta.status != "congelada":
            raise ValueError("Solo se pueden enviar propuestas congeladas.")
        fuente = FormatoInterno({
            "id": propuesta.id,
            "title": propuesta.title,
            "description": propuesta.description,
            "creator_name": propuesta.creator_name,
            "signature_count": propuesta.signature_count,
            "frozen_hash": propuesta.frozen_hash,
            "created_at": propuesta.created_at,
        })
        adapter = CongresoAdapter(fuente)
        return adapter.adaptar_a_dict()
