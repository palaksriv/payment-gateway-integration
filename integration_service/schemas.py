from pydantic import BaseModel, Field


class PaymentCreateRequest(BaseModel):
    amount: int = Field(gt=0)
    currency: str = "INR"
    customer_id: str


class PaymentResponse(BaseModel):
    order_id: str
    amount: int
    currency: str
    customer_id: str
    status: str