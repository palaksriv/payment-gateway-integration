\# Payment Gateway Integration Service



\## Overview



Backend payment integration service built with FastAPI that demonstrates REST API communication, payment lifecycle management, webhook processing, HMAC-SHA256 signature verification, idempotent event handling, SQLite persistence, automated testing, and Postman API testing.



This project uses a \*\*locally implemented mock payment gateway\*\* for educational and portfolio purposes. It does not process real payments.



\## Architecture



```text

Client / Postman

&#x20;      |

&#x20;      | HTTP / REST

&#x20;      v

Payment Integration Service

FastAPI :8000

&#x20;      |

&#x20;      | HTTP / REST

&#x20;      | HTTPX

&#x20;      v

Mock Payment Gateway

FastAPI :8001

&#x20;      |

&#x20;      | Signed Webhook

&#x20;      | HMAC-SHA256

&#x20;      v

Webhook Handler

&#x20;      |

&#x20;      v

SQLite Database

SQLAlchemy

```



\## Features



\- Create and manage payment records.

\- Communicate with a mock payment gateway through REST APIs.

\- Track payment status from creation through success or failure.

\- Process payment webhooks.

\- Verify webhook signatures using HMAC-SHA256.

\- Reject missing or invalid webhook signatures.

\- Prevent duplicate webhook processing using event IDs.

\- Persist payment and webhook data using SQLite and SQLAlchemy.

\- Simulate successful and failed payments.

\- Test APIs using Postman.

\- Run automated API tests using Pytest and pytest-asyncio.

\- Handle invalid requests and nonexistent payments.



\## Tech Stack



\- Python

\- FastAPI

\- HTTPX

\- SQLAlchemy

\- SQLite

\- Pydantic

\- Pytest

\- pytest-asyncio

\- Postman

\- HMAC-SHA256

\- Git / GitHub



\## Project Structure



```text

payment-gateway-integration/

│

├── integration\_service/

│   └── ...

│

├── mock\_gateway/

│   └── ...

│

├── tests/

│   ├── \_\_init\_\_.py

│   └── ...

│

├── .gitignore

├── README.md

└── requirements.txt

```



Local `.env` files, virtual environments, database files, caches, and logs are excluded from version control.



\## Setup



\### Prerequisites



\- Python 3.10+

\- Git

\- Postman



Check Python:



```powershell

python --version

```



Check Git:



```powershell

git --version

```



\### Clone Repository



```powershell

git clone https://github.com/palaksriv/payment-gateway-integration.git

cd payment-gateway-integration

```



\### Create Virtual Environment



```powershell

python -m venv .venv

```



Activate it:



```powershell

.\\.venv\\Scripts\\Activate.ps1

```



If PowerShell blocks activation:



```powershell

Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

```



Then:



```powershell

.\\.venv\\Scripts\\Activate.ps1

```



\### Install Dependencies



```powershell

pip install -r requirements.txt

```



\## Environment Variables



Create a local `.env` file if required by the project configuration:



```powershell

notepad .env

```



Example:



```env

WEBHOOK\_SECRET=your-local-webhook-secret

```



Keep secrets local. The `.env` file is excluded from Git.



\## Running the Application



The project uses two FastAPI services.



| Service | Port |

|---|---:|

| Payment Integration Service | 8000 |

| Mock Payment Gateway | 8001 |



\### Start the Mock Payment Gateway



In one PowerShell terminal:



```powershell

.\\.venv\\Scripts\\Activate.ps1

uvicorn mock\_gateway.main:app --reload --port 8001

```



The service runs at:



```text

http://127.0.0.1:8001

```



Swagger documentation:



```text

http://127.0.0.1:8001/docs

```



\### Start the Payment Integration Service



In a second PowerShell terminal:



```powershell

.\\.venv\\Scripts\\Activate.ps1

uvicorn integration\_service.main:app --reload --port 8000

```



The service runs at:



```text

http://127.0.0.1:8000

```



Swagger documentation:



```text

http://127.0.0.1:8000/docs

```



\## API Workflow



The main payment workflow is:



1\. Client sends a payment request.

2\. Payment Integration Service receives the request.

3\. Integration Service calls the Mock Payment Gateway.

4\. Mock Gateway creates the payment/order.

5\. Integration Service stores the payment in SQLite.

6\. Mock Gateway simulates a payment event.

7\. Mock Gateway sends a signed webhook.

8\. Integration Service verifies the webhook signature.

9\. The webhook event ID is checked for duplicates.

10\. Payment status is updated.



\## Payment States



The project supports the following payment lifecycle:



```text

created

&#x20;  |

&#x20;  +----> paid

&#x20;  |

&#x20;  +----> failed

```



Successful payment:



```text

created → paid

```



Failed payment:



```text

created → failed

```



\## Webhook Security



Webhook requests use HMAC-SHA256 signatures to verify their authenticity.



The webhook includes:



```text

X-Webhook-Signature

```



The Integration Service calculates the expected signature using the configured webhook secret and compares it with the received signature.



Invalid requests are rejected.



\### Missing Signature



```text

401 Unauthorized

```



\### Invalid Signature



```text

401 Unauthorized

```



\## Webhook Idempotency



Webhook providers can retry events, so the same event may be delivered more than once.



This project uses a unique `event\_id` to prevent duplicate processing.



Processed event IDs are stored in the database.



If an already processed event is received again:



```json

{

&#x20; "status": "already\_processed"

}

```



This prevents duplicate payment status updates and demonstrates idempotent webhook processing.



\## Example Payment Request



```http

POST /payments

Content-Type: application/json

```



```json

{

&#x20; "amount": 499.00,

&#x20; "currency": "INR",

&#x20; "customer\_id": "customer\_001"

}

```



\## Example Webhook Event



```json

{

&#x20; "event\_id": "evt\_001",

&#x20; "payment\_id": "pay\_001",

&#x20; "status": "paid"

}

```



The Mock Payment Gateway signs the webhook using HMAC-SHA256 before sending it to the Integration Service.



The Integration Service then:



1\. Receives the webhook.

2\. Reads the signature.

3\. Calculates the expected signature.

4\. Verifies the signature.

5\. Checks the `event\_id`.

6\. Rejects the event if it was already processed.

7\. Stores the new event.

8\. Updates the payment status.



\## Postman Testing



The Postman workflow covers the complete payment lifecycle.



Tested scenarios include:



1\. Health check

2\. Create payment

3\. Get payment

4\. Simulate successful payment

5\. Get updated payment

6\. Simulate failed payment

7\. Test duplicate webhook event

8\. Test nonexistent payment



\## Automated Testing



Run the test suite with:



```powershell

pytest

```



Current test result:



```text

7 passed

```



Tests cover:



\- Health check

\- Payment creation

\- Payment retrieval

\- Invalid payment amount

\- Missing webhook signature

\- Invalid webhook signature

\- Nonexistent payment handling



\## What This Project Demonstrates



\### Backend Development



\- FastAPI REST APIs

\- Request validation

\- Error handling

\- Service-to-service communication



\### API Integration



\- REST API consumption using HTTPX

\- Backend integration patterns

\- External API response handling

\- Payment lifecycle management



\### Webhooks



\- Asynchronous event processing

\- HMAC-SHA256 verification

\- Webhook security

\- Idempotent event handling



\### Database



\- SQLAlchemy ORM

\- SQLite persistence

\- Payment state management

\- Processed webhook event tracking



\### Testing



\- Pytest

\- pytest-asyncio

\- Automated API testing

\- Postman API testing



\## Security



The project uses `.gitignore` to exclude local and generated files such as:



```text

.venv/

.env

.env.\*

\*.db

\*.sqlite

\*.sqlite3

\_\_pycache\_\_/

\*.py\[cod]

.pytest\_cache/

logs/

```



Secrets and local configuration should never be committed to GitHub.



\## Disclaimer



This is a \*\*local mock payment gateway integration built for educational and portfolio purposes\*\*.



It does not connect to or process payments through a real payment provider.



The project demonstrates payment integration concepts including REST APIs, webhooks, HMAC-SHA256 verification, idempotency, database persistence, API testing, and error handling.



\## Author



\*\*Palak Srivastava\*\*



\[GitHub](https://github.com/palaksriv)

