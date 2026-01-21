from abc import ABC, abstractmethod
from langchain_google_genai import ChatGoogleGenerativeAI
from app.core.config import settings

class BaseLLMService(ABC):
    @abstractmethod
    async def generate_response(self, prompt: str, system_message: str = "") -> str:
        pass


class GeminiService(BaseLLMService):
    def __init__(self):
        self.model = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=settings.GOOGLE_API_KEY
        )

    async def generate_response(self, prompt: str, system_message: str = "") -> str:
        messages = [
            ("system", system_message),
            ("human", prompt)
        ]
        response = await self.model.ainvoke(messages)
        return response.content
