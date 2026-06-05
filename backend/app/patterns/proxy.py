from abc import ABC, abstractmethod
from datetime import datetime

class DocumentInterface(ABC):
    @abstractmethod
    def leer(self) -> dict:
        pass

    @abstractmethod
    def modificar(self, datos: dict) -> dict:
        pass

class DocumentoReal(DocumentInterface):
    def __init__(self, propuesta_data: dict):
        self._data = propuesta_data

    def leer(self) -> dict:
        return self._data

    def modificar(self, datos: dict) -> dict:
        self._data.update(datos)
        return self._data

class DocumentoProxy(DocumentInterface):
    def __init__(self, propuesta_data: dict):
        self._real = DocumentoReal(propuesta_data)
        self._estado = propuesta_data.get("status", "activa")
        self._intentos_bloqueados: list = []

    def leer(self) -> dict:
        return self._real.leer()

    def modificar(self, datos: dict) -> dict:
        if self._estado == "congelada":
            self._intentos_bloqueados.append({
                "datos_intentados": datos,
                "hora": datetime.utcnow().isoformat()
            })
            raise PermissionError("La propuesta está congelada y no puede modificarse.")
        return self._real.modificar(datos)

    def get_intentos_bloqueados(self) -> list:
        return self._intentos_bloqueados
