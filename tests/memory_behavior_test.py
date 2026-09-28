from app.agent.reviewer import CodeReviewer


def print_review(title, review):
    print(f"\n{'=' * 55}")
    print(f"{title:^55}")
    print(f"{'=' * 55}\n")

    memory_enabled = getattr(review, "_memory_enabled", False)
    memories = getattr(review, "_memory_used", [])

    print(f"🧠 Memory enabled: {'YES' if memory_enabled else 'NO'}")

    if memories:
        print("\n📌 Relevant project memory:")
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

    code = """
import requests

def get_user(user_id):
    response = requests.get(
        f"https://api.example.com/users/{user_id}"
    )
    return response.json()
"""

    memoryless_review = reviewer.review(
        code,
        use_memory=False,
    )

    memory_aware_review = reviewer.review(
        code,
        use_memory=True,
    )

    print_review(
        "MEMORY OFF — GENERIC REVIEW",
        memoryless_review,
    )

    print_review(
        "MEMORY ON — PROJECT-AWARE REVIEW",
        memory_aware_review,
    )


if __name__ == "__main__":
    main()