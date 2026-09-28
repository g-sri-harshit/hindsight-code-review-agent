from app.agent.reviewer import CodeReviewer


def main():
    reviewer = CodeReviewer()

    code = """
def get_user(user_id):
    query = "SELECT * FROM users WHERE id = " + user_id
    return database.execute(query)
"""

    print("\n========== MEMORYLESS REVIEW ==========\n")

    memoryless_review = reviewer.review(
        code,
        use_memory=False,
    )

    print("SUMMARY:")
    print(memoryless_review.summary)

    for issue in memoryless_review.issues:
        print(f"\n[{issue.severity.value.upper()}]")
        print(f"Category: {issue.category.value}")
        print(f"Title: {issue.title}")
        print(f"Suggestion: {issue.suggestion}")

    print("\n========== MEMORY-AWARE REVIEW ==========\n")

    memory_review = reviewer.review(
        code,
        use_memory=True,
    )

    print("SUMMARY:")
    print(memory_review.summary)

    for issue in memory_review.issues:
        print(f"\n[{issue.severity.value.upper()}]")
        print(f"Category: {issue.category.value}")
        print(f"Title: {issue.title}")
        print(f"Suggestion: {issue.suggestion}")


if __name__ == "__main__":
    main()