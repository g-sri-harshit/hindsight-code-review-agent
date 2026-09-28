from app.agent.reviewer import CodeReviewer


def print_review(title, review):
    print(f"\n{'=' * 60}")
    print(f"{title:^60}")
    print(f"{'=' * 60}\n")

    print(f"🧠 Memory enabled: {'YES' if getattr(review, '_memory_enabled', False) else 'NO'}")

    memories = getattr(review, "_memory_used", [])

    if memories:
        print("\n📌 Memory influencing this review:")
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
    # STEP 1: Developer teaches the agent a project preference
    # ---------------------------------------------------------

    developer_decision = (
        "Project review policy: Do not recommend replacing a "
        "synchronous dependency with an asynchronous alternative "
        "unless the code has a concrete asynchronous requirement. "
        "For normal synchronous HTTP calls, keep using requests."
    )

    print("\n" + "=" * 60)
    print("STEP 1 — DEVELOPER TEACHES THE AGENT")
    print("=" * 60)

    print("\nDeveloper decision:")
    print(developer_decision)

    reviewer.retain_feedback(
        feedback=developer_decision,
        context="Explicit developer architectural decision"
    )

    print("\n✅ Decision stored in Hindsight.")


    # ---------------------------------------------------------
    # STEP 2: Review code WITHOUT memory
    # ---------------------------------------------------------

    code = """
import requests

def get_user(user_id):
    response = requests.get(
        f"https://api.example.com/users/{user_id}"
    )
    return response.json()
"""

    print("\n" + "=" * 60)
    print("STEP 2 — REVIEW WITHOUT MEMORY")
    print("=" * 60)

    memoryless_review = reviewer.review(
        code,
        use_memory=False
    )

    print_review(
        "MEMORY OFF — GENERIC REVIEW",
        memoryless_review
    )


    # ---------------------------------------------------------
    # STEP 3: Review same code WITH learned memory
    # ---------------------------------------------------------

    print("\n" + "=" * 60)
    print("STEP 3 — REVIEW WITH LEARNED MEMORY")
    print("=" * 60)

    memory_aware_review = reviewer.review(
        code,
        use_memory=True
    )

    print_review(
        "MEMORY ON — LEARNED PROJECT REVIEW",
        memory_aware_review
    )


    # ---------------------------------------------------------
    # STEP 4: Demo conclusion
    # ---------------------------------------------------------

    print("\n" + "=" * 60)
    print("LEARNING RESULT")
    print("=" * 60)

    print(
        "\nThe agent was given a developer decision, "
        "stored it in Hindsight, and recalled project context "
        "during the later review."
    )

    print(
        "\nThis demonstrates:\n"
        "Developer feedback → Hindsight RETAIN → "
        "future Hindsight RECALL → project-aware review"
    )


if __name__ == "__main__":
    main()