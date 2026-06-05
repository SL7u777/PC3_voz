from datetime import datetime

class FormatoInterno:
    def __init__(self, propuesta: dict):
        self.id = propuesta.get("id")
        self.title = propuesta.get("title")
        self.description = propuesta.get("description")
        self.creator_name = propuesta.get("creator_name")
        self.signature_count = propuesta.get("signature_count", 0)
        self.frozen_hash = propuesta.get("frozen_hash")
        self.created_at = propuesta.get("created_at")

class FormatoCongreso:
    def __init__(self):
        self.numero_iniciativa: str = ""
        self.denominacion: str = ""
        self.exposicion_motivos: str = ""
        self.proponente: str = ""
        self.firmas_validadas: int = 0
        self.codigo_integridad: str = ""
        self.fecha_presentacion: str = ""
        self.comision_asignada: str = ""

class CongresoAdapter:
    def __init__(self, fuente: FormatoInterno):
        self._fuente = fuente

    def _asignar_comision(self, titulo: str) -> str:
        t = titulo.lower()
        if any(k in t for k in ["agua", "ambiente", "ecolog", "natural", "climat"]):
            return "Comisión de Pueblos, Ambiente y Ecología"
        if any(k in t for k in ["educac", "escuela", "universid", "enseñ"]):
            return "Comisión de Educación, Juventud y Deporte"
        if any(k in t for k in ["salud", "hospital", "médic", "sanidad"]):
            return "Comisión de Salud y Población"
        if any(k in t for k in ["transport", "vial", "carretera", "infraestructur"]):
            return "Comisión de Transportes y Comunicaciones"
        if any(k in t for k in ["trabajo", "laboral", "empleo", "sindic"]):
            return "Comisión de Trabajo y Seguridad Social"
        if any(k in t for k in ["seguridad", "policial", "orden público"]):
            return "Comisión de Defensa Nacional y Orden Interno"
        return "Comisión de Constitución y Reglamento"

    def adaptar(self) -> FormatoCongreso:
        doc = FormatoCongreso()
        doc.numero_iniciativa = f"ILC-{self._fuente.id:05d}"
        doc.denominacion = self._fuente.title
        doc.exposicion_motivos = self._fuente.description
        doc.proponente = self._fuente.creator_name
        doc.firmas_validadas = self._fuente.signature_count
        doc.codigo_integridad = self._fuente.frozen_hash or ""
        doc.fecha_presentacion = (
            self._fuente.created_at.isoformat()
            if isinstance(self._fuente.created_at, datetime)
            else str(self._fuente.created_at)
        )
        doc.comision_asignada = self._asignar_comision(self._fuente.title)
        return doc

    def adaptar_a_dict(self) -> dict:
        doc = self.adaptar()
        return {
            "numero_iniciativa": doc.numero_iniciativa,
            "denominacion": doc.denominacion,
            "exposicion_motivos": doc.exposicion_motivos,
            "proponente": doc.proponente,
            "firmas_validadas": doc.firmas_validadas,
            "codigo_integridad": doc.codigo_integridad,
            "fecha_presentacion": doc.fecha_presentacion,
            "comision_asignada": doc.comision_asignada,
        }
