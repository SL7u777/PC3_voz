from abc import ABC, abstractmethod

class ProposalComponent(ABC):
    @abstractmethod
    def get_info(self) -> dict:
        pass

class ProposalLeaf(ProposalComponent):
    def __init__(self, tipo: str, contenido: str):
        self.tipo = tipo
        self.contenido = contenido

    def get_info(self) -> dict:
        return {"tipo": self.tipo, "contenido": self.contenido}

class ProposalComposite(ProposalComponent):
    def __init__(self, titulo: str, descripcion: str):
        self.titulo = titulo
        self.descripcion = descripcion
        self._children: list[ProposalComponent] = []

    def agregar(self, componente: ProposalComponent):
        self._children.append(componente)

    def eliminar(self, componente: ProposalComponent):
        self._children.remove(componente)

    def contar_elementos(self) -> int:
        total = 1
        for child in self._children:
            if isinstance(child, ProposalComposite):
                total += child.contar_elementos()
            else:
                total += 1
        return total

    def get_info(self) -> dict:
        return {
            "titulo": self.titulo,
            "descripcion": self.descripcion,
            "total_elementos": self.contar_elementos(),
            "elementos": [child.get_info() for child in self._children]
        }
