from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from schemas.rag_schemas import RAGResponse
from services.rag_service import RAGService

router = APIRouter(prefix="/rag", tags=["RAG"])

rag_service = RAGService()

@router.post("/chat", response_model=RAGResponse)
async def rag_chat(
    message: str = Form(...),
    context_file: UploadFile | None = File(None)
):
    """
    Endpoint principal para procesar una consulta RAG.
    Si se envía un archivo, se usará como contexto adicional.
    """
    try:
        response = await rag_service.process_rag_query(message, context_file)
        return RAGResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error procesando la consulta: {str(e)}")
