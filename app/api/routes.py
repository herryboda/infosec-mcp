from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from app.core.security import get_api_key
from app.services.llm_service import LLMService
from typing import Optional

router = APIRouter()
llm_service = LLMService()

class Question(BaseModel):
    question: str

class Document(BaseModel):
    content: str
    name: str

@router.post("/ask")
async def ask_question(
    question: Question,
    api_key: str = Depends(get_api_key)
):
    try:
        response = await llm_service.answer_question(question.question)
        return {"answer": response}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("/ingest")
async def ingest_document(
    document: Document,
    api_key: str = Depends(get_api_key)
):
    try:
        result = await llm_service.ingest_document(document.content, document.name)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        ) 