from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.agent.runtime import run_turn


router = APIRouter()


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1)
    conversation_id: Optional[str] = None


class ChatResponse(BaseModel):
    conversation_id: str
    answer: str
    plan: list[dict] = Field(default_factory=list)


@router.get("/health")
async def health_check():
    return {"status": "ok"}


@router.post(
    "/chat",
    response_model=ChatResponse,
)
async def chat_endpoint(
    payload: ChatRequest,
):

    try:
        result = await run_turn(
            payload.message,
            conversation_id=payload.conversation_id,
        )

        if result.get("error"):
            raise HTTPException(
                status_code=400,
                detail=result["error"],
            )

        return ChatResponse(
            conversation_id=result.get(
                "conversation_id",
                payload.conversation_id or "",
            ),
            answer=result.get(
                "final_answer",
                "",
            ),
            plan=result.get(
                "plan",
                [],
            ),
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )
