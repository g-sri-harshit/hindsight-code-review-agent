import os

from dotenv import load_dotenv
from hindsight_client import Hindsight


load_dotenv()


class HindsightMemory:
    """Small application-level wrapper around Hindsight."""

    def __init__(self):
        self.api_url = os.getenv("HINDSIGHT_API_URL")
        self.api_key = os.getenv("HINDSIGHT_API_KEY")
        self.bank_id = os.getenv("HINDSIGHT_BANK_ID")

        if not self.api_url:
            raise RuntimeError("HINDSIGHT_API_URL is missing")

        if not self.api_key:
            raise RuntimeError("HINDSIGHT_API_KEY is missing")

        if not self.bank_id:
            raise RuntimeError("HINDSIGHT_BANK_ID is missing")

        self.client = Hindsight(
            base_url=self.api_url,
            api_key=self.api_key,
        )

    def retain_knowledge(
        self,
        content: str,
        context: str | None = None,
        tags: list[str] | None = None,
    ):
        """Store useful project knowledge in Hindsight."""

        return self.client.retain(
            bank_id=self.bank_id,
            content=content,
            context=context,
            tags=tags,
        )

    def recall_context(
        self,
        query: str,
        tags: list[str] | None = None,
    ):
        """Retrieve relevant project knowledge from Hindsight."""

        return self.client.recall(
            bank_id=self.bank_id,
            query=query,
            tags=tags,
        )