import uuid

from fastapi import APIRouter

from mock_gateway.schemas import OrderCreateRequest, OrderResponse

router = APIRouter(prefix="/api/orders", tags=["Orders"])


@router.post("", response_model=OrderResponse, status_code=201)
def create_order(request: OrderCreateRequest):
    order_id = f"order_{uuid.uuid4().hex[:12]}"

    return OrderResponse(
        order_id=order_id,
        amount=request.amount,
        currency=request.currency.upper(),
        customer_id=request.customer_id,
        status="created",
    )