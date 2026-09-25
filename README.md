\# Payment Gateway Integration Service



Production-ready backend payment integration service built with \*\*FastAPI\*\*, \*\*SQLite persistence\*\*, \*\*HMAC-SHA256 signed webhooks\*\*, \*\*idempotent event handling\*\*, and \*\*automated pytest verification\*\*.



\## Overview



A robust backend service demonstrating how modern web applications integrate with upstream financial APIs and process asynchronous webhook callbacks securely.



The system coordinates order creation, verifies cryptographic webhook signatures, prevents duplicate transaction processing via idempotency checks, and maintains an auditable state machine.



> \*\*Note:\*\* Integrates with an isolated local mock gateway built for portfolio demonstration; no real transactions are processed.



\## Architecture



\### Integration Service



`integration\_service/` — Port `8000`



FastAPI application handling:



\* Client checkout requests

\* Database persistence via SQLAlchemy

\* Upstream API coordination via HTTPX

\* Signed webhook intake



\### Mock Gateway



`mock\_gateway/` — Port `8001`



FastAPI mock service simulating third-party payment gateway behavior, including:



\* Order generation

\* Payment outcomes

\* HMAC-SHA256 signed event dispatch



\### Database



`database/`



SQLite instance tracking:



\* Payment state lifecycles

\* Historical `event\_id` records for idempotency guarantees



\## Setup \& Running



\### 1. Environment \& Dependencies



Create and activate a Python virtual environment:



```powershell

python -m venv .venv

.\\.venv\\Scripts\\Activate.ps1

pip install -r requirements.txt

```



\### 2. Configuration



Create a `.env` file in the root directory:



```env

WEBHOOK\_SECRET=your\_shared\_hmac\_secret\_key

DATABASE\_URL=sqlite:///./payments.db

GATEWAY\_BASE\_URL=http://127.0.0.1:8001

```



> Keep `.env` local and do not commit secrets to GitHub.



\### 3. Launch Services



Run both services in separate PowerShell windows.



\#### Terminal 1 — Integration Service



```powershell

uvicorn integration\_service.main:app --host 127.0.0.1 --port 8000 --reload

```



\#### Terminal 2 — Mock Gateway



```powershell

uvicorn mock\_gateway.main:app --host 127.0.0.1 --port 8001 --reload

```



\### Interactive Documentation



\*\*Integration Service\*\*



http://127.0.0.1:8000/docs



\*\*Mock Gateway\*\*



http://127.0.0.1:8001/docs



\## Key Features



\### REST API Integration



Upstream gateway communication using asynchronous HTTPX client calls.



\### Payment Lifecycle



Deterministic payment state transitions:



```text

created → paid

created → failed

```



\### Cryptographic Security



Webhook payloads are validated against the `X-Webhook-Signature` header using HMAC-SHA256 digests.



Tampered or unsigned requests return:



```text

401 Unauthorized

```



\### Idempotency Guarantee



Atomic validation on unique `event\_id` values ensures replayed or duplicate webhook events return:



```json

{

&#x20; "status": "already\_processed"

}

```



without mutating payment state.



\### Automated Test Suite



Full unit and integration coverage using:



\* `pytest`

\* `pytest-asyncio`



\### Postman API Collection



Pre-configured collection validating:



\* Happy paths

\* Payment failures

\* Duplicate deliveries

\* Signature validation failures



\## Testing



Run the test suite using PowerShell:



```powershell

pytest -v

```



\### Test Scenarios Covered



\* Health check availability

\* Payment creation and relational database persistence

\* Status retrieval by payment ID

\* Input validation and rejection of non-positive payment amounts

\* Missing webhook signature validation

\* Forged webhook signature validation

\* `401 Unauthorized` responses for invalid webhook signatures

\* Missing entity lookups

\* `404 Not Found` responses for missing entities



\## Security



The payment integration service uses \*\*HMAC-SHA256\*\* to verify webhook authenticity.



The webhook flow validates:



1\. The incoming `X-Webhook-Signature`

2\. The expected HMAC-SHA256 digest

3\. The uniqueness of the webhook `event\_id`



This protects the service against forged webhook requests and duplicate event processing.



\## Payment State Machine



```text

&#x20;                 ┌──────────┐

&#x20;                 │  created │

&#x20;                 └────┬─────┘

&#x20;                      │

&#x20;             ┌────────┴────────┐

&#x20;             │                 │

&#x20;             ▼                 ▼

&#x20;        ┌─────────┐       ┌─────────┐

&#x20;        │  paid   │       │ failed  │

&#x20;        └─────────┘       └─────────┘

```



\## What This Project Demonstrates



\* Backend development with FastAPI

\* REST API integration

\* Asynchronous HTTP communication

\* Third-party API integration patterns

\* Payment lifecycle management

\* Webhook processing

\* HMAC-SHA256 signature verification

\* Idempotent event handling

\* SQLAlchemy database persistence

\* SQLite database management

\* Automated API testing

\* Postman API testing

\* Secure environment-based configuration



\## Disclaimer



This project uses an \*\*isolated local mock payment gateway\*\* for portfolio and educational purposes.



It does \*\*not\*\* process real financial transactions or connect to a production payment provider.



