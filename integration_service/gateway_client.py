import os

import httpx
from dotenv import load_dotenv

load_dotenv()

GATEWAY_URL = os.getenv(
    "MOCK_GATEWAY_URL",
    "http://127.0.0.1:8001",
)


async def create_gateway_order(
    amount: int,
    currency: str,
    customer_id: str,
):
    payload = {
        "amount": amount,
        "currency": currency,
        "customer_id": customer_id,
    }

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.post(
            f"{GATEWAY_URL}/api/orders",
            json=payload,
        )

    response.raise_for_status()

    return response.json()