# ai-service/app/api/v1/endpoints.py
from fastapi import APIRouter
from app.services.rag_service import RAGService
from app.models.predict import PredictRequest, PredictResponse

router = APIRouter()

rag_service = RAGService()


@router.post("/analyze", response_model=PredictResponse)
async def analyze_finance_rag(request: PredictRequest):
    result = await rag_service.answer_question(request.query)

    return PredictResponse(
        answer=result["answer"]
    )