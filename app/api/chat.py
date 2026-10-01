from fastapi import APIRouter
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import ChatService

router = APIRouter(
    prefix="/api/chat",
    tags=["Chat"],
)


@router.get("/hello")
def hello():
    return {
        "message": "Trade Finance AI Assistant is running"
    }

chat_service = ChatService()

@router.post("", response_model=ChatResponse)
def chat(request: ChatRequest):

    answer = chat_service.process_message(
        request.message
    )

    return ChatResponse(
        answer=answer
    )