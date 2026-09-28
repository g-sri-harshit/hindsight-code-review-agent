import os
import re

from dotenv import load_dotenv
from groq import Groq

from app.memory.hindsight import HindsightMemory
from app.models.review import CodeReview


load_dotenv()


class CodeReviewer:
    """LLM-based code reviewer with project-aware Hindsight memory."""

    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise RuntimeError("GROQ_API_KEY is missing")

        self.client = Groq(api_key=api_key)
        self.model = "openai/gpt-oss-120b"

        self.memory = HindsightMemory()

    @staticmethod
    def _normalize_memory(text: str) -> str:
        """
        Normalize memory text so semantically identical formatting
        variations can be detected more easily.
        """

        text = text.lower()

        text = re.sub(r"\s+", " ", text)

        text = text.replace("'", "")
        text = text.replace('"', "")

        text = text.replace(" | project convention", "")
        text = text.replace(" | constraint for code review recommendations", "")
        text = text.replace(" | architectural decision to maintain simplicity for standard operations", "")
        text = text.replace(" | part of the project review policy", "")

        return text.strip()

    def _recall_relevant_memory(self, query: str) -> list[str]:
        """Recall useful memories and remove obvious duplicates."""

        recalled = self.memory.recall_context(query)

        if not recalled.results:
            return []

        unique_memories = []
        seen_normalized = set()

        for memory in recalled.results:

            text = memory.text.strip()

            if not text:
                continue

            normalized = self._normalize_memory(text)

            if not normalized:
                continue

            if normalized in seen_normalized:
                continue

            seen_normalized.add(normalized)
            unique_memories.append(text)

        # Keep the prompt focused.
        return unique_memories[:5]

    def get_memory_context(self) -> list[str]:
        """
        Retrieve project memories for display in the application UI.
        """

        query = (
            "What project conventions, developer preferences, "
            "architectural decisions, accepted suggestions, "
            "rejected suggestions, and recurring code review "
            "decisions are relevant to this project?"
        )

        return self._recall_relevant_memory(query)

    def review(
        self,
        code: str,
        use_memory: bool = False,
    ) -> CodeReview:

        system_prompt = (
            "You are an expert software code reviewer.\n\n"

            "Review the provided code carefully.\n\n"

            "Identify meaningful issues related to:\n"
            "- bugs\n"
            "- security\n"
            "- performance\n"
            "- maintainability\n"
            "- style\n"
            "- testing\n\n"

            "Do not invent problems.\n"
            "Do not criticize code merely because you would personally "
            "implement it differently.\n\n"

            "For every real issue:\n"
            "- assign an appropriate severity\n"
            "- assign a category\n"
            "- explain why it matters\n"
            "- provide a concrete improvement\n\n"

            "If project memory is provided, use it to make the review "
            "project-specific.\n\n"

            "Memory represents learned project context, not absolute truth.\n"
            "If memory conflicts with clear evidence in the code, "
            "prioritize the actual code.\n\n"

            "If there are no meaningful issues, return an empty issues list.\n\n"

            "Return only the requested structured review."
        )

        memory_context = ""
        used_memories = []

        if use_memory:

            used_memories = self.get_memory_context()

            if used_memories:

                memory_lines = [
                    f"- {memory}"
                    for memory in used_memories
                ]

                memory_context = (
                    "\n\nPROJECT MEMORY FROM HINDSIGHT:\n"
                    + "\n".join(memory_lines)
                    + "\n\n"
                    "Use the project memory when it is relevant to "
                    "the actual code.\n"
                    "Do not blindly follow it.\n"
                    "Do not mention memory unless it affects the review."
                )

        user_prompt = (
            "Review the following code:\n\n"
            "```python\n"
            f"{code}\n"
            "```"
            f"{memory_context}"
        )

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "code_review",
                    "strict": True,
                    "schema": CodeReview.model_json_schema(),
                },
            },
        )

        content = response.choices[0].message.content

        review = CodeReview.model_validate_json(content)

        # Metadata used by the demo/UI.
        review._memory_enabled = use_memory
        review._memory_used = used_memories

        return review

    def retain_feedback(
        self,
        feedback: str,
        context: str = "Developer feedback from code review",
    ):
        """Store meaningful developer feedback in Hindsight."""

        if not feedback.strip():
            raise ValueError("Feedback cannot be empty")

        return self.memory.retain_knowledge(
            content=feedback,
            context=context,
            tags=["developer-feedback"],
        )