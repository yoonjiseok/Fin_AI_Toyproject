import asyncio
import json
import websockets
from aiokafka import AIOKafkaProducer

KAFKA_BOOTSTRAP_SERVERS = "localhost:19092"
TOPIC_NAME = "market-prices"
UPBIT_WS_URL = "wss://api.upbit.com/websocket/v1"


async def consume_upbit_and_produce_kafka():
    producer = AIOKafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    await producer.start()
    print(f"✅ Connected to Kafka: {KAFKA_BOOTSTRAP_SERVERS}")

    try:
        async with websockets.connect(UPBIT_WS_URL) as websocket:
            subscribe_fmt = [
                {"ticket": "test-uuid"},
                {"type": "trade", "codes": ["KRW-BTC"], "isOnlyRealtime": True},
                {"format": "SIMPLE"}
            ]
            await websocket.send(json.dumps(subscribe_fmt))
            print("✅ Connected to Upbit WebSocket (KRW-BTC)")

            while True:
                data = await websocket.recv()
                trade_data = json.loads(data)

                message = {
                    "symbol": "BTC",
                    "price": trade_data['tp'],
                    "volume": trade_data['tv'],
                    "timestamp": trade_data['ttms'],
                    "change": trade_data['c']
                }

                await producer.send_and_wait(TOPIC_NAME, message)
                print(f"Produced: {message}")

    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        await producer.stop()


if __name__ == "__main__":
    asyncio.run(consume_upbit_and_produce_kafka())