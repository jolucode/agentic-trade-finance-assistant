import re


def route_message(message: str) -> str:

    pattern = r"\bLC-\d+\b"

    if re.search(
        pattern,
        message.upper()
    ):
        return "tool"

    return "rag"