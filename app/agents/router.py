import re


def route_message(
    message: str,
    last_lc_id: str | None = None
) -> str:

    pattern = r"\bLC-\d+\b"

    if re.search(pattern, message.upper()):
        return "tool"

    follow_up_keywords = [
        "status",
        "amount",
        "beneficiary",
        "currency",
        "it",
        "this letter"
    ]

    if last_lc_id and any(
        keyword in message.lower()
        for keyword in follow_up_keywords
    ):
        return "tool"

    return "rag"