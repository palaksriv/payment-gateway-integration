Payment Gateway Integration Service

Production-ready backend payment integration service built with FastAPI that demonstrates REST API integration, payment lifecycle management, signed webhooks, HMAC-SHA256 verification, idempotent event processing, SQLite persistence, automated testing, and Postman API testing.

Note: This project uses a locally implemented mock payment gateway for educational and portfolio purposes. It does not process real payments.

Overview

A robust backend service demonstrating how modern applications integrate with upstream financial APIs and process asynchronous webhook callbacks securely.

The system coordinates payment creation, verifies cryptographic webhook signatures, prevents duplicate transaction processing through idempotency checks, and maintains an auditable payment state.

Architecture

Client / Postman
       |
       | HTTP / REST
       v
Payment Integration Service
FastAPI :8000
       |
       | HTTP / REST
       | HTTPX
       v
Mock Payment Gateway
FastAPI :8001
       |
       | Signed Webhook
       | HMAC-SHA256
       v
Webhook Handler
       |
       v
SQLite Database
SQLAlchemy

Project Structure

payment-gateway-integration/
│
├── integration_service/
│   └── ...
│
├── mock_gateway/
│   └── ...
│
├── postman/
│   └── ...
│
├── tests/
│   ├── __init__.py
│   └── ...
│
├── .gitignore
├── README.md
└── requirements.txt

Tech Stack

Technology

Purpose

Python

Backend development

FastAPI

REST API services

HTTPX

Service-to-service HTTP requests

SQLAlchemy

Database ORM

SQLite

Local persistence

Pydantic

Request and response validation

HMAC-SHA256

Webhook signature verification

Pytest

Automated testing

pytest-asyncio

Async API testing

Postman

API testing

Git / GitHub

Version control

Features

Payment Integration

REST API communication between services

Payment/order creation

Payment retrieval

Payment status tracking

Successful payment simulation

Failed payment simulation

Webhooks

Webhook-based payment status updates

HMAC-SHA256 signature generation

HMAC-SHA256 signature verification

Missing signature rejection

Invalid signature rejection

Idempotency

Webhook events contain a unique event_id.

Processed event IDs are stored in the database so duplicate webhook deliveries do not process the same event multiple times.

Example response for an already processed event:

{
  "status": "already_processed"
}

Database

The project uses:

SQLite

SQLAlchemy

Payment records and processed webhook event IDs are persisted locally.

Testing

The project includes automated API tests using:

Pytest

pytest-asyncio

The test suite covers health checks, payment operations, input validation, webhook security, and error handling.

Postman API Collection

A Postman collection is included in the postman/ directory for manually testing the payment workflow.

Setup

Prerequisites

Make sure the following are installed:

Python 3.10+

Git

Postman

Check Python:

python --version

Check Git:

git --version

Clone the Repository

git clone https://github.com/palaksriv/payment-gateway-integration.git
cd payment-gateway-integration

Create a Virtual Environment

On Windows PowerShell:

python -m venv .venv

Activate the virtual environment:

.\.venv\Scripts\Activate.ps1

If PowerShell blocks activation, run:

Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

Then activate again:

.\.venv\Scripts\Activate.ps1

Install Dependencies

pip install -r requirements.txt

Environment Variables

Create a local .env file in the project root if required by the project configuration.

notepad .env

Example:

WEBHOOK_SECRET=your_shared_hmac_secret_key
DATABASE_URL=sqlite:///./payments.db
GATEWAY_BASE_URL=http://127.0.0.1:8001

Keep .env local. Never commit secrets or API keys to GitHub.

Running the Application

The project contains two FastAPI services:

Service

Port

Payment Integration Service

8000

Mock Payment Gateway

8001

Run the services in two separate PowerShell terminals.

Terminal 1 — Mock Payment Gateway

Activate the virtual environment:

.\.venv\Scripts\Activate.ps1

Start the mock gateway:

uvicorn mock_gateway.main:app --host 127.0.0.1 --port 8001 --reload

The mock gateway will be available at:

http://127.0.0.1:8001

Swagger documentation:

http://127.0.0.1:8001/docs

Terminal 2 — Payment Integration Service

Open a second PowerShell terminal.

Navigate to the project:

cd payment-gateway-integration

Activate the virtual environment:

.\.venv\Scripts\Activate.ps1

Start the integration service:

uvicorn integration_service.main:app --host 127.0.0.1 --port 8000 --reload

The integration service will be available at:

http://127.0.0.1:8000

Swagger documentation:

http://127.0.0.1:8000/docs

API Workflow

The complete simulated payment flow is:

1. Client / Postman
        |
        | Create payment
        v
2. Payment Integration Service
        |
        | HTTP request
        v
3. Mock Payment Gateway
        |
        | Creates payment/order
        v
4. Integration Service
        |
        | Stores payment
        v
5. SQLite Database
        |
        | Payment event
        v
6. Mock Payment Gateway
        |
        | HMAC-SHA256 signed webhook
        v
7. Webhook Handler
        |
        | Verify signature
        v
8. Check event_id
        |
        | Prevent duplicate processing
        v
9. Update Payment Status

Payment Lifecycle

The simulated payment lifecycle supports:

created
   |
   +----> paid
   |
   +----> failed

Successful payment:

created → paid

Failed payment:

created → failed

Webhook Security

Webhook requests are protected using an HMAC-SHA256 signature.

The webhook request contains:

X-Webhook-Signature

The receiving service calculates the expected signature using the shared webhook secret and compares it with the received signature.

Missing Signature

Requests without a webhook signature are rejected:

401 Unauthorized

Invalid Signature

Requests with an invalid signature are rejected:

401 Unauthorized

This demonstrates a common pattern for verifying webhook authenticity.

Webhook Idempotency

Webhook providers can retry event delivery.

Without idempotency, the same payment event could potentially be processed multiple times.

This project prevents duplicate processing by storing each processed event_id.

When the same event is received again, the service recognizes it as already processed and does not mutate the payment state again.

Example:

{
  "status": "already_processed"
}

Example Payment Request

A payment can be created through the integration service API.

Example request:

POST /payments
Content-Type: application/json

{
  "amount": 499.00,
  "currency": "INR",
  "customer_id": "customer_001"
}

The integration service communicates with the mock gateway and persists the resulting payment information.

Example Webhook Event

A simulated payment event can look like:

{
  "event_id": "evt_001",
  "payment_id": "pay_001",
  "status": "paid"
}

The mock gateway signs the webhook using HMAC-SHA256 before sending it to the integration service.

The integration service then:

Receives the webhook.

Reads the X-Webhook-Signature.

Calculates the expected HMAC-SHA256 signature.

Verifies the signature.

Checks whether the event_id has already been processed.

Stores the event if it is new.

Updates the payment status.

Postman Testing

The included Postman collection can be used to test the complete payment workflow.

Typical scenarios include:

Health check

Create payment

Retrieve payment

Simulate successful payment

Retrieve updated payment

Simulate failed payment

Test duplicate webhook delivery

Test missing webhook signature

Test invalid webhook signature

Test nonexistent payment

Automated Testing

Run the test suite from the project root:

pytest -v

The tests cover:

Health check availability

Payment creation

Payment persistence

Payment retrieval

Invalid payment amount handling

Missing webhook signature

Invalid webhook signature

Nonexistent payment handling

Webhook idempotency behavior

API Documentation

FastAPI automatically provides interactive Swagger documentation.

Integration Service

http://127.0.0.1:8000/docs

Mock Gateway

http://127.0.0.1:8001/docs

You can use the Swagger interface to inspect endpoints and send test requests directly from the browser.

Error Handling

The service demonstrates standard HTTP error handling.

Scenario

Response

Successful request

200 OK / 201 Created

Invalid input

400 Bad Request / 422 Unprocessable Entity

Missing webhook signature

401 Unauthorized

Invalid webhook signature

401 Unauthorized

Payment not found

404 Not Found

Duplicate webhook event

already_processed response

Security

The project demonstrates several backend security practices:

HMAC-SHA256 webhook verification

Environment-based secret configuration

Duplicate event protection

Input validation through Pydantic

HTTP status code based error handling

Secrets excluded from Git using .gitignore

Never commit the real .env file or production secrets to GitHub.

What This Project Demonstrates

Backend Development

FastAPI REST API development

Request and response validation

Error handling

Service-to-service communication

API Integration

HTTPX asynchronous HTTP clients

REST API integration

Upstream API coordination

Payment lifecycle management

Webhooks

Asynchronous event processing

HMAC-SHA256 signature verification

Webhook authentication

Idempotent event processing

Database

SQLAlchemy ORM

SQLite persistence

Payment state management

Webhook event tracking

Testing

Pytest

pytest-asyncio

API integration tests

Security validation tests

Postman testing

Disclaimer

This project uses an isolated local mock payment gateway for educational and portfolio purposes.

It does not process real financial transactions and does not connect to a production payment provider.

The project demonstrates payment integration concepts including REST APIs, webhooks, HMAC-SHA256 verification, idempotency, database persistence, automated testing, and error handling.

Author

Palak Srivastava

GitHub
