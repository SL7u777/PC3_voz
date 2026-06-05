from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine
from app.models import Proposal, Signature, Comment, Attachment
from app.database import Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Voz del Ciudadano", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    return {"estado": "activo", "sistema": "Voz del Ciudadano"}
