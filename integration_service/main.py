from fastapi import FastAPI

from integration_service.database import Base, engine
from integration_service.models import Payment
from integration_service.routes.payments import router as payments_router
from integration_service.routes.webhooks import router as webhooks_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Payment Integration Service",
    version="1.0.0",
)

app.include_router(payments_router)
app.include_router(webhooks_router)


@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": "payment-integration-service",
    }