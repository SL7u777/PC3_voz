# Voz del Ciudadano

Plataforma digital para la gestión de Iniciativas Legislativas Ciudadanas.

## Descripción

Permite a colectivos civiles crear propuestas normativas y recolectar firmas digitales.
Al alcanzar 25,000 firmas válidas en 90 días, el sistema congela criptográficamente
el documento y lo envía a la Oficina del Congreso.

## Patrones Estructurales utilizados

| Patrón | Rol |
|--------|-----|
| Facade | Orquesta el proceso completo de envío al Congreso |
| Proxy | Controla acceso a propuestas congeladas |
| Decorator | Añade metadatos dinámicos a las propuestas |
| Composite | Estructura jerárquica: propuesta → secciones → adjuntos |
| Adapter | Adapta el formato interno al formato del Congreso |

## Tecnologías

- **Backend:** Python + FastAPI
- **Base de datos:** SQLite + SQLAlchemy
- **Frontend:** HTML + CSS + JavaScript

## Estructura

```
PC3_voz/
├── backend/
│   ├── app/
│   │   ├── models/      ← modelos de base de datos
│   │   ├── patterns/    ← patrones estructurales
│   │   ├── routes/      ← endpoints REST
│   │   └── services/    ← lógica de negocio
│   └── requirements.txt
├── frontend/            ← páginas HTML
└── README.md
```

## Instalación y ejecución

**Backend**
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```
La API queda disponible en `http://localhost:8000`
Documentación interactiva: `http://localhost:8000/docs`

**Frontend**
Abrir directamente los archivos HTML en el navegador o usar un servidor local:
```bash
cd frontend
python3 -m http.server 5500
```
Luego acceder a `http://localhost:5500`
