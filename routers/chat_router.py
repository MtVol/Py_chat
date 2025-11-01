from fastapi import APIRouter, Depends
from schemas.chat_shemas import InputMensage
from services import chat_service
from services.clients import get_openai_client
from openai import OpenAI

router = APIRouter()

@router.post("/ai-chat")
def ai_chat(
    data_in: InputMensage,
    client: OpenAI = Depends(get_openai_client)
):
    response = chat_service.get_chat_response(data_in, client)

    return {"response": response}