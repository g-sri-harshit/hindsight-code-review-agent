from app.memory.hindsight import HindsightMemory


def test_hindsight_connection():
    memory = HindsightMemory()

    result = memory.recall_context(
        "What HTTP library convention does this project follow?"
    )

    assert result is not None