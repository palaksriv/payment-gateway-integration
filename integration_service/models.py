from sqlalchemy import Column, Integer, String

from integration_service.database import Base


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)

    order_id = Column(String, unique=True, nullable=False, index=True)

    customer_id = Column(String, nullable=False)

    amount = Column(Integer, nullable=False)

    currency = Column(String, nullable=False)

    status = Column(String, nullable=False, default="created")

    gateway = Column(String, nullable=False, default="mock_gateway")


class WebhookEvent(Base):
    __tablename__ = "webhook_events"

    id = Column(Integer, primary_key=True, index=True)

    event_id = Column(String, unique=True, nullable=False, index=True)

    event_type = Column(String, nullable=False)

    order_id = Column(String, nullable=False)