from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.models import ChatRequest, ChatResponse
from app.agent import chat

app = FastAPI(
    title="CarDekho Assistant API",
    description="AI-powered car buying advisor for the Indian market",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    messages = [{"role": msg.role, "content": msg.content} for msg in request.messages]
    result = chat(messages)
    return ChatResponse(
        reply=result["reply"],
        cars=result.get("cars"),
        comparison=result.get("comparison"),
    )
