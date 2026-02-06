import asyncio
import json
from aiokafka import AIOKafkaConsumer
from app.services.rag_service import RAGService

KAFKA_BOOTSTRAP_SERVERS = "localhost:19092"
TOPIC_NAME = "market-prices"


class MarketConsumer:
    def __init__(self):
        self.rag_service = RAGService()
        self.last_price = None
        self.running = False

    async def start(self):
        self.running = True
        consumer = AIOKafkaConsumer(
            TOPIC_NAME,
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            group_id="ai-agent-group",
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )

        await consumer.start()
        print("✅ Market Consumer Started! Listening for anomalies...")

        try:
            async for msg in consumer:
                if not self.running: break

                data = msg.value
                current_price = float(data['price'])

                if self.last_price is None:
                    self.last_price = current_price
                    continue

                price_diff = current_price - self.last_price

                if abs(price_diff) >= 5000:
                    print(f" 급변동 감지! 차이: {price_diff}원 (현재가: {current_price})")

                    asyncio.create_task(self.trigger_ai_analysis(current_price, price_diff))

                    self.last_price = current_price

        except Exception as e:
            print(f"Consumer Error: {e}")
        finally:
            await consumer.stop()

    async def trigger_ai_analysis(self, price, diff):
        direction = "상승" if diff > 0 else "하락"
        query = f"현재 비트코인이 {price}원으로 {abs(diff)}원 {direction}했습니다. 이 변동의 원인이 될만한 최근 시장 상황이나 리스크 요인을 알려줘."

        print(f"AI 분석 요청: {query}")

        try:
            result = await self.rag_service.answer_question(query)
            print(f"[AI 분석 결과]: {result['answer']}")
        except Exception as e:
            print(f"AI Analysis Failed: {e}")


market_consumer = MarketConsumer()