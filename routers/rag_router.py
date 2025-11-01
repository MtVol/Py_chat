from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from schemas.rag_schemas import RAGResponse
from services.rag_service import RAGService

router = APIRouter()
rag_service = RAGService()

@router.post("/rag-chat", response_model=RAGResponse)
async def rag_chat(message: str = Form(...), context_file: UploadFile = File(...)):
    try:
        response = await rag_service.process_rag_query(message, context_file)
        return RAGResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))