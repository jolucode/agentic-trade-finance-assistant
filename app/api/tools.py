from fastapi import APIRouter

from app.tools.banking_tools import get_letter_of_credit_status


router = APIRouter(
    prefix="/api/tools",
    tags=["Tools"]
)


@router.get("/letter-of-credit/{lc_id}")
def get_lc_status(lc_id: str):

    return get_letter_of_credit_status(
        lc_id
    )