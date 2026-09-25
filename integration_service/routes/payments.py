from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from integration_service.database import get_db
from integration_service.gateway_client import create_gateway_order
from integration_service.models import Payment
from integration_service.schemas import (
    PaymentCreateRequest,
    PaymentResponse,
)

router = APIRouter(
    prefix="/api/payments",
    tags=["Payments"],
)


@router.post(
    "/create",
    response_model=PaymentResponse,
    status_code=201,
)
async def create_payment(
    request: PaymentCreateRequest,
    db: Session = Depends(get_db),
):
    try:
        gateway_order = await create_gateway_order(
            amount=request.amount,
            currency=request.currency,
            customer_id=request.customer_id,
        )

        payment = Payment(
            order_id=gateway_order["order_id"],
            customer_id=gateway_order["customer_id"],
            amount=gateway_order["amount"],
            currency=gateway_order["currency"],
            status=gateway_order["status"],
            gateway="mock_gateway",
        )

        db.add(payment)
        db.commit()
        db.refresh(payment)

        return PaymentResponse(
            order_id=payment.order_id,
            amount=payment.amount,
            currency=payment.currency,
            customer_id=payment.customer_id,
            status=payment.status,
        )

    except Exception as exc:
        db.rollback()

        raise HTTPException(
            status_code=502,
            detail=f"Payment gateway error: {str(exc)}",
        )


@router.get(
    "/{order_id}",
    response_model=PaymentResponse,
)
def get_payment(
    order_id: str,
    db: Session = Depends(get_db),
):
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

    return PaymentResponse(
        order_id=payment.order_id,
        amount=payment.amount,
        currency=payment.currency,
        customer_id=payment.customer_id,
        status=payment.status,
    )