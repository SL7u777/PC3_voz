import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.database import engine
from app.database import Base
from app.models import Proposal, Signature, Comment, Attachment, Modification
from app.routes import proposals, signatures, comments, attachments, modifications

Base.metadata.create_all(bind=engine)
os.makedirs("uploads", exist_ok=True)

app = FastAPI(title="Voz del Ciudadano", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(proposals.router)
app.include_router(signatures.router)
app.include_router(comments.router)
app.include_router(attachments.router)
app.include_router(modifications.router)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

@app.get("/")
def health_check():
    return {"estado": "activo", "sistema": "Voz del Ciudadano"}
