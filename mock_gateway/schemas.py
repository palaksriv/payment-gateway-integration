from pydantic import BaseModel, Field


class OrderCreateRequest(BaseModel):
    amount: int = Field(gt=0, description="Amount in smallest currency unit")
    currency: str = "INR"
    customer_id: str


class OrderResponse(BaseModel):
    order_id: str
    amount: int
    currency: str
    customer_id: str
    status: str


class PaymentEventRequest(BaseModel):
    order_id: str
    event: str
    status: str
    event_id: str