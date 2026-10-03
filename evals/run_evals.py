import json
from pathlib import Path

from app.agents.router import route_message
from app.tools.banking_tools import get_letter_of_credit_status
from app.rag.retriever import Retriever
from app.services.chat_service import ChatService


EVAL_FILE = Path("evals/eval_cases.json")

retriever = Retriever()
chat_service = ChatService()


def load_cases():
    return json.loads(
        EVAL_FILE.read_text(encoding="utf-8")
    )


def run_routing_evals(cases):

    passed = 0

    print("\n=== ROUTING EVALS ===")

    for case in cases:

        actual = route_message(
            case["question"]
        )

        expected = case["expected_route"]

        ok = actual == expected

        print(
            f"{'PASS' if ok else 'FAIL'} | "
            f"question={case['question']} | "
            f"expected={expected} | "
            f"actual={actual}"
        )

        if ok:
            passed += 1

    return passed, len(cases)


def run_tool_evals(cases):

    passed = 0

    print("\n=== TOOL EVALS ===")

    for case in cases:

        result = get_letter_of_credit_status(
            case["expected_lc_id"]
        )

        ok = (
            result.get("lc_id") == case["expected_lc_id"]
            and
            result.get("status") == case["expected_status"]
        )

        print(
            f"{'PASS' if ok else 'FAIL'} | "
            f"lc_id={case['expected_lc_id']} | "
            f"expected_status={case['expected_status']} | "
            f"actual_status={result.get('status')}"
        )

        if ok:
            passed += 1

    return passed, len(cases)


def run_rag_evals(cases):

    passed = 0

    print("\n=== RAG EVALS ===")

    for case in cases:

        results = retriever.search(
            query=case["question"],
            top_k=3
        )

        combined_text = " ".join(
            result["text"].lower()
            for result in results
        )

        keywords = case["expected_keywords"]

        ok = all(
            keyword.lower() in combined_text
            for keyword in keywords
        )

        print(
            f"{'PASS' if ok else 'FAIL'} | "
            f"question={case['question']} | "
            f"expected_keywords={keywords}"
        )

        if ok:
            passed += 1

    return passed, len(cases)


def run_memory_evals(cases):

    passed = 0

    print("\n=== MEMORY EVALS ===")

    for case in cases:

        thread_id = case["thread_id"]

        chat_service.process_message(
            message=case["first_question"],
            thread_id=thread_id
        )

        answer = chat_service.process_message(
            message=case["second_question"],
            thread_id=thread_id
        )

        normalized_answer = (
            answer
            .lower()
            .replace(",", "")
            .replace("$", "")
            .strip()
        )

        ok = all(
            keyword.lower().replace(",", "") in normalized_answer
            for keyword in case["expected_keywords"]
        )

        print(
            f"{'PASS' if ok else 'FAIL'} | "
            f"thread_id={thread_id} | "
            f"answer={answer}"
        )

        if ok:
            passed += 1

    return passed, len(cases)


def main():

    cases = load_cases()

    results = []

    results.append(
        run_routing_evals(
            cases["routing"]
        )
    )

    results.append(
        run_tool_evals(
            cases["tools"]
        )
    )

    results.append(
        run_rag_evals(
            cases["rag"]
        )
    )

    results.append(
        run_memory_evals(
            cases["memory"]
        )
    )

    total_passed = sum(
        passed for passed, total in results
    )

    total_cases = sum(
        total for passed, total in results
    )

    score = (
        total_passed / total_cases * 100
        if total_cases
        else 0
    )

    print("\n=== SUMMARY ===")
    print(
        f"Passed: {total_passed}/{total_cases}"
    )
    print(
        f"Score: {score:.1f}%"
    )


if __name__ == "__main__":
    main()