from fastapi.testclient import TestClient

from integration_service.main import app


client = TestClient(app)


def test_health_check():
    response = client.get("/api/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"


def test_get_nonexistent_payment():
    response = client.get(
        "/api/payments/order_does_not_exist"
    )

    assert response.status_code == 404

    assert response.json()["detail"] == "Payment not found"


def test_webhook_missing_signature():
    payload = {
        "event_id": "evt_test_missing",
        "order_id": "order_test",
        "event": "payment.completed",
        "status": "paid",
    }

    response = client.post(
        "/api/webhooks/payment",
        json=payload,
    )

    assert response.status_code == 401

    assert response.json()["detail"] == "Missing webhook signature"


def test_webhook_invalid_signature():
    payload = {
        "event_id": "evt_test_invalid",
        "order_id": "order_test",
        "event": "payment.completed",
        "status": "paid",
    }

    response = client.post(
        "/api/webhooks/payment",
        json=payload,
        headers={
            "X-Webhook-Signature": "invalid_signature"
        },
    )

    assert response.status_code == 401

    assert response.json()["detail"] == "Invalid webhook signature"


def test_create_payment():
    response = client.post(
        "/api/payments/create",
        json={
            "amount": 15000,
            "currency": "INR",
            "customer_id": "test_customer_001",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["amount"] == 15000
    assert data["currency"] == "INR"
    assert data["customer_id"] == "test_customer_001"
    assert data["status"] == "created"
    assert data["order_id"].startswith("order_")


def test_create_payment_rejects_invalid_amount():
    response = client.post(
        "/api/payments/create",
        json={
            "amount": 0,
            "currency": "INR",
            "customer_id": "test_customer_002",
        },
    )

    assert response.status_code == 422


def test_get_created_payment():
    create_response = client.post(
        "/api/payments/create",
        json={
            "amount": 25000,
            "currency": "INR",
            "customer_id": "test_customer_003",
        },
    )

    assert create_response.status_code == 201

    order_id = create_response.json()["order_id"]

    response = client.get(
        f"/api/payments/{order_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["order_id"] == order_id
    assert data["status"] == "created"