from fastapi import FastAPI

from mock_gateway.routes.orders import router as orders_router
from mock_gateway.routes.payments import router as payments_router

app = FastAPI(
    title="Mock Payment Gateway",
    version="1.0.0",
)

app.include_router(orders_router)
app.include_router(payments_router)


@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": "mock-payment-gateway",
    }