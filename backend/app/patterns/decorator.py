from abc import ABC, abstractmethod
from datetime import datetime

class ProposalBase(ABC):
    @abstractmethod
    def get_data(self) -> dict:
        pass

class ProposalConcreto(ProposalBase):
    def __init__(self, data: dict):
        self._data = data

    def get_data(self) -> dict:
        return self._data

class ProposalDecorator(ProposalBase):
    def __init__(self, propuesta: ProposalBase):
        self._propuesta = propuesta

    def get_data(self) -> dict:
        return self._propuesta.get_data()

class TimestampDecorator(ProposalDecorator):
    def get_data(self) -> dict:
        data = self._propuesta.get_data()
        data["consultado_en"] = datetime.utcnow().isoformat()
        return data

class FirmasDecorator(ProposalDecorator):
    LIMITE_FIRMAS = 25000

    def get_data(self) -> dict:
        data = self._propuesta.get_data()
        count = data.get("signature_count", 0)
        data["progreso_firmas"] = round((count / self.LIMITE_FIRMAS) * 100, 2)
        data["firmas_restantes"] = max(0, self.LIMITE_FIRMAS - count)
        return data

class EstadoDecorator(ProposalDecorator):
    def get_data(self) -> dict:
        data = self._propuesta.get_data()
        data["estado_legible"] = "Congelada - Enviada al Congreso" if data.get("status") == "congelada" else "Activa - Recolectando firmas"
        return data
