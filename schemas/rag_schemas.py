from pydantic import BaseModel

class RAGRequest(BaseModel):
    message: str
    context_file: str

class RAGResponse(BaseModel):
    response: str