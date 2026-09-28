import os

from dotenv import load_dotenv
from hindsight_client import Hindsight


load_dotenv()

API_URL = os.getenv("HINDSIGHT_API_URL")
API_KEY = os.getenv("HINDSIGHT_API_KEY")
BANK_ID = os.getenv("HINDSIGHT_BANK_ID")


if not API_URL:
    raise RuntimeError("HINDSIGHT_API_URL is missing")

if not API_KEY:
    raise RuntimeError("HINDSIGHT_API_KEY is missing")

if not BANK_ID:
    raise RuntimeError("HINDSIGHT_BANK_ID is missing")


client = Hindsight(
    base_url=API_URL,
    api_key=API_KEY,
)

print("Connected to Hindsight.")
print(f"Bank: {BANK_ID}")

print("\n--- RETAIN ---")

response = client.retain(
    bank_id=BANK_ID,
    content=(
        "This project uses requests for HTTP calls. "
        "Do not recommend replacing requests with httpx "
        "unless there is a concrete requirement for async HTTP."
    ),
    context="Code review project convention",
    tags=["project-convention"],
)

print(response)

print("\n--- RECALL ---")

results = client.recall(
    bank_id=BANK_ID,
    query="What HTTP library convention does this project follow?",
)

print(results)

print("\n--- DONE ---")