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
            아래 제공된 [문서 내용]만을 근거로 삼아 [질문]에 대해 답변하세요. 
            만약 문서 내용에 답이 없다면 "해당 정보는 문서에 없습니다"라고 답하세요.

            [문서 내용]
            {context}

            [질문]
            {query}
            """

            answer = await self.llm.generate_response(prompt, "금융 분석 에이전트입니다.")
            return {"answer": answer, "context_used": context}

        finally:
            db.close()