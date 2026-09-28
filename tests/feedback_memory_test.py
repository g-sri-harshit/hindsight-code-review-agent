from app.agent.reviewer import CodeReviewer


def main():
    reviewer = CodeReviewer()

    feedback = (
        "This project uses requests for synchronous HTTP calls. "
        "Do not recommend replacing requests with httpx unless "
        "there is a concrete requirement for asynchronous HTTP."
    )

    print("\n========== RETAINING FEEDBACK ==========\n")

    result = reviewer.retain_feedback(feedback)

    print("Hindsight retain result:")
    print(result)

    print("\n========== RECALLING FEEDBACK ==========\n")

    recalled = reviewer.memory.recall_context(
        "What HTTP library convention does this project follow?"
    )

    for memory in recalled.results:
        print(f"[{memory.type}] {memory.text}")

    print("\n=========================================\n")


if __name__ == "__main__":
    main()