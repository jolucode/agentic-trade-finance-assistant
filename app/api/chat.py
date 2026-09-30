from fastapi import APIRouter


router = APIRouter(
    prefix="/api/chat",
    tags=["Chat"],
)


@router.get("/hello")
def hello():
    return {
        "message": "Trade Finance AI Assistant is running"
    }
