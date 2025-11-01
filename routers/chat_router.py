from fastapi import APIRouter
from schemas.chat_shemas import InputMensage
from services import chat_service

router = APIRouter()

@router.post("/ai-chat")
def ai_chat(data_in: InputMensage):

    response = chat_service.get_chat_response(data_in)

    return {"response": response}