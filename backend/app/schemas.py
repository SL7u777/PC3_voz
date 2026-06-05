from pydantic import BaseModel

class ProposalCreate(BaseModel):
    title: str
    description: str
    creator_name: str

class SignatureCreate(BaseModel):
    citizen_name: str
    citizen_id: str

class CommentCreate(BaseModel):
    author_name: str
    content: str
