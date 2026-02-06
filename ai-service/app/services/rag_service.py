from sqlalchemy import text
from app.db.session import SessionLocal
from app.db.vector_db import embeddings
from app.services.llm_service import GeminiService


class RAGService:
    def __init__(self):
        self.llm = GeminiService()

    async def answer_question(self, query: str):
        db = SessionLocal()
        try:
            # 1. 질문을 벡터로 변환 (Gemini Embedding)
            query_vector = embeddings.embed_query(query)

            # 2. pgvector 유사도 검색 (Cosine Similarity)
            # 질문 벡터와 가장 가까운 상위 3개의 조각을 가져옵니다.
            search_query = text("""
                                SELECT content
                                FROM document_chunks
                                ORDER BY embedding <=> :vector 
                LIMIT 3
                                """)

            results = db.execute(search_query, {"vector": str(query_vector)}).fetchall()
            context = "\n".join([r[0] for r in results])

            prompt = f"""
            당신은 금융 분석 에이전트입니다.
            
            1. 우선 아래 [문서 내용]을 참고하여 질문에 답변하세요.
            2. 만약 [문서 내용]에 직접적인 답이 없다면, 당신이 가진 일반적인 금융 지식을 활용하여 
               해당 변동의 '일반적인 원인'(예: 시장 변동성, 기술적 반등 등)을 설명해주세요.
            3. 단, 문서를 참고하지 않았을 때는 "문서에는 없지만, 일반적인 관점에서..."라고 언급해주세요.

            [문서 내용]
            {context}

            [질문]
            {query}
            """

            answer = await self.llm.generate_response(prompt, "금융 분석 에이전트입니다.")
            return {"answer": answer, "context_used": context}

        finally:
            db.close()