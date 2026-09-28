from app.agent.reviewer import CodeReviewer


def print_review(title, review):
    print("\n" + "=" * 70)
    print(f"{title:^70}")
    print("=" * 70)

    memory_enabled = getattr(review, "_memory_enabled", False)
    memories = getattr(review, "_memory_used", [])

    print(
        f"\n🧠 Memory enabled: "
        f"{'YES' if memory_enabled else 'NO'}"
    )

    if memories:
        print("\n📌 Recalled project knowledge:")

        for memory in memories:
            print(f"   • {memory}")

    print("\nSUMMARY:")
    print(review.summary)

    print("\nISSUES:")

    if not review.issues:
        print("   No meaningful issues found.")
        return

    for issue in review.issues:
        print(f"\n[{issue.severity.value.upper()}]")
        print(f"Category: {issue.category.value}")
        print(f"Title: {issue.title}")
        print(f"Suggestion: {issue.suggestion}")


def main():
    reviewer = CodeReviewer()

    # ---------------------------------------------------------
    # STEP 1 — Teach the agent a specific project decision
    # ---------------------------------------------------------

    developer_decision = (
        "Architectural decision for this project: keep synchronous "
        "HTTP operations on the requests library. Do not recommend "
        "switching from requests to httpx or another asynchronous "
        "HTTP library unless the code has a concrete requirement "
        "for asynchronous execution."
    )

    print("\n" + "=" * 70)
    print("STEP 1 — TEACH THE AGENT")
    print("=" * 70)

    print("\nDeveloper decision:")
    print(developer_decision)

    reviewer.retain_feedback(
        feedback=developer_decision,
        context="Explicit architectural decision from developer",
    )

    print("\n✅ Developer decision stored in Hindsight.")


    # ---------------------------------------------------------
    # STEP 2 — Code with an actual opportunity for an
    # asynchronous-library recommendation
    # ---------------------------------------------------------

    code = """
import requests


def fetch_users(user_ids):
    results = []

    for user_id in user_ids:
        response = requests.get(
            f"https://api.example.com/users/{user_id}"
        )
        response.raise_for_status()
        results.append(response.json())

    return results
"""


    # ---------------------------------------------------------
    # STEP 3 — Generic reviewer
    # ---------------------------------------------------------

    print("\n" + "=" * 70)
    print("STEP 2 — GENERIC REVIEW")
    print("=" * 70)

    memoryless_review = reviewer.review(
        code,
        use_memory=False,
    )

    print_review(
        "MEMORY OFF — GENERIC REVIEW",
        memoryless_review,
    )


    # ---------------------------------------------------------
    # STEP 4 — Project-aware reviewer
    # ---------------------------------------------------------

    print("\n" + "=" * 70)
    print("STEP 3 — PROJECT-AWARE REVIEW")
    print("=" * 70)

    memory_review = reviewer.review(
        code,
        use_memory=True,
    )

    print_review(
        "MEMORY ON — PROJECT-AWARE REVIEW",
        memory_review,
    )


    # ---------------------------------------------------------
    # STEP 5 — Explain the learning loop
    # ---------------------------------------------------------

    print("\n" + "=" * 70)
    print("LEARNING RESULT")
    print("=" * 70)

    print(
        "\nThe developer first taught the agent an architectural "
        "decision."
    )

    print(
        "\nHindsight stored that decision as persistent project memory."
    )

    print(
        "\nThe same code was then reviewed with and without memory."
    )

    print(
        "\nThe memory-aware reviewer received the previous decision "
        "before generating its review."
    )

    print(
        "\n🎯 Goal:"
        "\nThe agent should preserve the developer's project decision "
        "instead of repeatedly suggesting a dependency change."
    )


if __name__ == "__main__":
    main()