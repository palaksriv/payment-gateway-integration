import hashlib
import hmac
import json
import os

import httpx
from fastapi import APIRouter, HTTPException

from mock_gateway.schemas import PaymentEventRequest

router = APIRouter(
    prefix="/api/payments",
    tags=["Payments"],
)

INTEGRATION_WEBHOOK_URL = (
    "http://127.0.0.1:8000/api/webhooks/payment"
)

WEBHOOK_SECRET = os.getenv(
    "WEBHOOK_SECRET",
    "dev_webhook_secret_123",
)


@router.post("/simulate")
async def simulate_payment(
    request: PaymentEventRequest,
):
    payload = {
        "event_id": request.event_id,
        "order_id": request.order_id,
        "event": request.event,
        "status": request.status,
    }

    payload_bytes = json.dumps(
        payload,
        separators=(",", ":"),
    ).encode()

    signature = hmac.new(
        WEBHOOK_SECRET.encode(),
        payload_bytes,
        hashlib.sha256,
    ).hexdigest()

    headers = {
        "Content-Type": "application/json",
        "X-Webhook-Signature": signature,
    }

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.post(
            INTEGRATION_WEBHOOK_URL,
            content=payload_bytes,
            headers=headers,
        )

    if response.status_code >= 400:
        raise HTTPException(
            status_code=response.status_code,
            detail=response.text,
        )

    return {
        "gateway_status": "event_sent",
        "webhook_response": response.json(),
    }