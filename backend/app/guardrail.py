import logging
from openai import OpenAI
from app.config import settings

logger = logging.getLogger(__name__)

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=settings.openrouter_api_key,
)

LLAMA_GUARD_MODEL = "meta-llama/llama-guard-4-12b"

SAFETY_CATEGORIES = """
O1: Violence and Hate
O2: Sexual Content
O3: Criminal Planning
O4: Guns and Illegal Weapons
O5: Regulated Substances
O6: Self-Harm
O7: Financial Crime / Fraud
"""


def moderate(message: str) -> dict:
    """
    Run Llama Guard on user input to check for unsafe content.
    Returns {"safe": True/False, "category": str | None}.
    """
    try:
        response = client.chat.completions.create(
            model=LLAMA_GUARD_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": f"Check if the following message is safe. Categories:\n{SAFETY_CATEGORIES}",
                },
                {"role": "user", "content": message},
            ],
            max_tokens=50,
        )

        result = response.choices[0].message.content.strip().lower()

        if result.startswith("safe"):
            return {"safe": True, "category": None}

        # Llama Guard returns "unsafe\nO1" format
        category = None
        if "\n" in result:
            category = result.split("\n")[1].strip()

        return {"safe": False, "category": category}

    except Exception as e:
        logger.warning(f"Llama Guard moderation failed, allowing through: {e}")
        return {"safe": True, "category": None}
