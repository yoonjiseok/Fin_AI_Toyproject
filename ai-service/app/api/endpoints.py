from fastapi import APIRouter, Depends
from app.services.llm_service import OpenAIService, BaseLLMService
from app.models.predict import PredictRequest, PredictResponse

router = APIRouter()


def get_llm_service() -> BaseLLMService:
    return OpenAIService()


@router.post("/analyze", response_model=PredictResponse)
async def analyze_finance(
        request: PredictRequest,
        llm_service: BaseLLMService = Depends(get_llm_service)
):
    system_msg = "당신은 전문 금융 분석가입니다. 제공된 데이터를 기반으로 인사이트를 제공하세요."
    result = await llm_service.generate_response(request.query, system_msg)

    return PredictResponse(answer=result)