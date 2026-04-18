from pydantic import BaseModel, Field
from typing import Optional


class ChatMessage(BaseModel):
    role: str = Field(..., description="Role: 'user' or 'assistant'")
    content: str = Field(..., description="Message content")


class ChatRequest(BaseModel):
    messages: list[ChatMessage] = Field(..., description="Conversation history")
    session_id: Optional[str] = Field(None, description="Optional session identifier")


class ChatResponse(BaseModel):
    reply: str = Field(..., description="Assistant reply")
    cars: Optional[list[dict]] = Field(None, description="Car data if returned by tools")
    comparison: Optional[dict] = Field(None, description="Comparison table if requested")


class CarFilters(BaseModel):
    min_budget: Optional[float] = None
    max_budget: Optional[float] = None
    body_type: Optional[str] = None
    fuel_type: Optional[str] = None
    transmission: Optional[str] = None
    seating_capacity: Optional[int] = None
    min_safety_rating: Optional[int] = None
    use_case: Optional[list[str]] = None
