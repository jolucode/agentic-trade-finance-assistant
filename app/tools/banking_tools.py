LETTER_OF_CREDITS = {
    "LC-10025": {
        "status": "UNDER_REVIEW",
        "amount": 50000,
        "currency": "USD",
        "beneficiary": "Global Machinery GmbH"
    },
    "LC-20050": {
        "status": "APPROVED",
        "amount": 120000,
        "currency": "EUR",
        "beneficiary": "European Export Ltd"
    },
    "LC-30075": {
        "status": "REJECTED",
        "amount": 25000,
        "currency": "USD",
        "beneficiary": "International Supplies Inc"
    }
}


def get_letter_of_credit_status(lc_id: str) -> dict:

    letter_of_credit = LETTER_OF_CREDITS.get(
        lc_id.upper()
    )

    if not letter_of_credit:
        return {
            "found": False,
            "message": f"Letter of credit {lc_id} was not found."
        }

    return {
        "found": True,
        "lc_id": lc_id.upper(),
        **letter_of_credit
    }