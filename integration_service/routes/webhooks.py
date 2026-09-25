import hashlib
import hmac
import json
import os

from fastapi import APIRouter, Depends, Header, HTTPException, Request
from sqlalchemy.orm import Session

from integration_service.database import get_db
from integration_service.models import Payment, WebhookEvent

router = APIRouter(
    prefix="/api/webhooks",
    tags=["Webhooks"],
)

WEBHOOK_SECRET = os.getenv(
    "WEBHOOK_SECRET",
    "dev_webhook_secret_123",
)


def verify_signature(
    payload: bytes,
    signature: str,
) -> bool:
    expected_signature = hmac.new(
        WEBHOOK_SECRET.encode(),
        payload,
        hashlib.sha256,
    ).hexdigest()

    return hmac.compare_digest(
        expected_signature,
        signature,
    )


@router.post("/payment")
async def payment_webhook(
    request: Request,
    x_webhook_signature: str | None = Header(default=None),
    db: Session = Depends(get_db),
):
    if not x_webhook_signature:
        raise HTTPException(
            status_code=401,
            detail="Missing webhook signature",
        )

    payload = await request.body()

    if not verify_signature(
        payload,
        x_webhook_signature,
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid webhook signature",
        )

    try:
        event = json.loads(payload)
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=400,
            detail="Invalid JSON payload",
        )

    event_id = event.get("event_id")
    order_id = event.get("order_id")
    event_type = event.get("event")
    status = event.get("status")

    if not event_id or not order_id or not event_type or not status:
        raise HTTPException(
            status_code=400,
            detail="Missing required event fields",
        )

    existing_event = (
        db.query(WebhookEvent)
        .filter(WebhookEvent.event_id == event_id)
        .first()
    )

    if existing_event:
        return {
            "status": "already_processed",
            "event_id": event_id,
            "order_id": order_id,
        }

    payment = (
        db.query(Payment)
        .filter(Payment.order_id == order_id)
        .first()
    )

    if not payment:
        raise HTTPException(
            status_code=404,
            detail="Payment not found",
        )

    payment.status = status

    webhook_event = WebhookEvent(
        event_id=event_id,
        event_type=event_type,
        order_id=order_id,
    )

    db.add(webhook_event)
    db.commit()

    return {
        "status": "processed",
        "event_id": event_id,
        "order_id": order_id,
        "payment_status": status,
    }