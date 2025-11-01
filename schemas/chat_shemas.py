from pydantic import BaseModel

class InputMensage(BaseModel):
    message: str