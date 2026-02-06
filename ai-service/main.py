import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.v1.endpoints import router as api_router
from app.services.market_consumer import market_consumer

@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(market_consumer.start())
    yield
    market_consumer.running = False
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass

app = FastAPI(title="Financial AI Agent Service", lifespan=lifespan)

app.include_router(api_router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)