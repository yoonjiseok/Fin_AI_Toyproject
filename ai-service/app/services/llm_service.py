from abc import ABC, abstractmethod
from langchain_openai import ChatOpenAI
from app.core.config import settings

class BaseLLMService(ABC):
    @abstractmethod
    async def generate_response(self, prompt: str, system_message: str = "") -> str:
        pass

class OpenAIService(BaseLLMService):
    def __init__(self):
        self.model = ChatOpenAI(
            model=settings.OPENAI_MODEL,
            api_key=settings.OPENAI_API_KEY,
            temperature=settings.TEMPERATURE
        )

    async def generate_response(self, prompt: str, system_message: str = "") -> str:

        messages = [
            ("system", system_message),
            ("human", prompt)
        ]
        response = await self.model.ainvoke(messages)
        return response.content
