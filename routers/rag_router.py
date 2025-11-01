from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Depends
from schemas.rag_schemas import RAGResponse
from services.rag_service import RAGService
from services.clients import get_openai_client
from openai import OpenAI

router = APIRouter(prefix="/rag", tags=["RAG"])

# La instancia del servicio ya no necesita crear un cliente
rag_service = RAGService()

@router.post("/chat", response_model=RAGResponse)
async def rag_chat(
    message: str = Form(...),
    context_file: UploadFile | None = File(None),
    client: OpenAI = Depends(get_openai_client)
):
    """
    Endpoint principal para procesar una consulta RAG.
    Si se envía un archivo, se usará como contexto adicional.
    """
    try:
        response = await rag_service.process_rag_query(message, context_file, client)
        return RAGResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error procesando la consulta: {str(e)}")
