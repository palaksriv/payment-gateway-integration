\# Payment Gateway Integration Service



A backend payment integration project built with \*\*FastAPI\*\* that demonstrates REST API integration, payment lifecycle management, signed webhooks, HMAC-SHA256 verification, idempotent event processing, database persistence, automated testing, and Postman API testing.



> \*\*Note:\*\* This project uses a locally implemented mock payment gateway for educational and portfolio purposes. It does \*\*not\*\* process real payments.



\---



\## Overview



This project simulates a payment integration system where an integration service communicates with a mock payment gateway through REST APIs.



The system demonstrates common backend payment-integration patterns including:



\* Payment/order creation

\* Payment status tracking

\* REST API communication

\* Webhook-based payment updates

\* HMAC-SHA256 webhook signature verification

\* Idempotent webhook processing

\* SQLite database persistence

\* Error handling

\* Automated API testing with Pytest

\* API testing through Postman



The project intentionally focuses on the \*\*backend integration layer\*\* rather than building a frontend UI.



\---



\## Architecture



```text

&#x20;                   Client / Postman

&#x20;                          |

&#x20;                          | HTTP / REST

&#x20;                          v

&#x20;             +--------------------------+

&#x20;             | Payment Integration       |

&#x20;             | Service                  |

&#x20;             | FastAPI :8000            |

&#x20;             +------------+-------------+

&#x20;                          |

&#x20;                          | HTTP / REST

&#x20;                          | HTTPX

&#x20;                          v

&#x20;             +--------------------------+

&#x20;             | Mock Payment Gateway      |

&#x20;             | FastAPI :8001            |

&#x20;             +------------+-------------+

&#x20;                          |

&#x20;                          | Signed Webhook

&#x20;                          | HMAC-SHA256

&#x20;                          v

&#x20;             +--------------------------+

&#x20;             | Webhook Handler           |

&#x20;             | Payment Integration       |

&#x20;             | Service                  |

&#x20;             +------------+-------------+

&#x20;                          |

&#x20;                          v

&#x20;             +--------------------------+

&#x20;             | SQLite Database           |

&#x20;             | SQLAlchemy                |

&#x20;             +--------------------------+

```



\---



\## Key Features



\### Payment Integration



\* REST API communication between services

\* Payment/order creation

\* Payment retrieval

\* Payment status tracking

\* Successful payment simulation

\* Failed payment simulation



\### Webhooks



\* Webhook-based payment status updates

\* HMAC-SHA256 signature generation

\* HMAC-SHA256 signature verification

\* Missing signature rejection

\* Invalid signature rejection



\### Idempotency



Webhook events contain a unique `event\_id`.



Processed event IDs are stored in the database so that duplicate webhook deliveries do not process the same event multiple times.



Example response for an already processed event:



```json

{

&#x20; "status": "already\_processed"

}

```



\### Database



The project uses:



\* SQLite

\* SQLAlchemy



Payment records and processed webhook event IDs are persisted locally.



\### Testing



The project includes automated API tests using:



\* Pytest

\* pytest-asyncio



The current test suite contains \*\*7 passing tests\*\* covering health checks, payment operations, validation, webhook security, and error handling.



\### API Testing



A Postman collection is included for manually testing the API workflow.



\---



\## Tech Stack



| Technology     | Purpose                          |

| -------------- | -------------------------------- |

| Python         | Backend development              |

| FastAPI        | REST API services                |

| HTTPX          | Service-to-service HTTP requests |

| SQLAlchemy     | Database ORM                     |

| SQLite         | Local persistence                |

| Pydantic       | Request/response validation      |

| HMAC-SHA256    | Webhook signature verification   |

| Pytest         | Automated testing                |

| pytest-asyncio | Async API testing                |

| Postman        | API testing                      |

| Git / GitHub   | Version control                  |



\---



\## Project Structure



```text

payment-gateway-integration/

│

├── integration\_service/

│   ├── ...

│   └── ...

│

├── mock\_gateway/

│   ├── ...

│   └── ...

│

├── tests/

│   ├── \_\_init\_\_.py

│   └── ...

│

├── .gitignore

├── README.md

├── requirements.txt

└── ...

```



> The exact Python modules may vary as the project evolves. Local `.env` files and generated database files are intentionally excluded from version control.



\---



\# Getting Started



\## Prerequisites



Make sure the following are installed:



\* Python 3.10+

\* Git

\* Postman



Check your Python installation:



```powershell

python --version

```



Check Git:



```powershell

git --version

```



\---



\## Clone the Repository



```powershell

git clone https://github.com/palaksriv/payment-gateway-integration.git

cd payment-gateway-integration

```



\---



\## Create a Virtual Environment



\### Windows PowerShell



```powershell

python -m venv .venv

```



Activate it:



```powershell

.\\.venv\\Scripts\\Activate.ps1

```



If PowerShell blocks activation, run:



```powershell

Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

```



Then:



```powershell

.\\.venv\\Scripts\\Activate.ps1

```



\---



\## Install Dependencies



```powershell

pip install -r requirements.txt

```



\---



\# Environment Variables



The project can use a local `.env` file for configuration and secrets.



Create it locally:



```powershell

notepad .env

```



Example:



```env

WEBHOOK\_SECRET=your-local-webhook-secret

```



The `.env` file is \*\*not committed to GitHub\*\*.



Sensitive configuration should remain local.



\---



\# Running the Application



The project contains two FastAPI services:



| Service                     |   Port |

| --------------------------- | -----: |

| Payment Integration Service | `8000` |

| Mock Payment Gateway        | `8001` |



Run each service in a separate PowerShell terminal.



\---



\## Terminal 1 — Mock Payment Gateway



Activate the virtual environment:



```powershell

.\\.venv\\Scripts\\Activate.ps1

```



Start the mock gateway:



```powershell

uvicorn mock\_gateway.main:app --reload --port 8001

```



The mock gateway will be available at:



```text

http://127.0.0.1:8001

```



FastAPI documentation:



```text

http://127.0.0.1:8001/docs

```



\---



\## Terminal 2 — Payment Integration Service



Activate the virtual environment:



```powershell

.\\.venv\\Scripts\\Activate.ps1

```



Start the integration service:



```powershell

uvicorn integration\_service.main:app --reload --port 8000

```



The integration service will be available at:



```text

http://127.0.0.1:8000

```



FastAPI documentation:



```text

http://127.0.0.1:8000/docs

```



> If the project's actual entry-point module differs, use the corresponding module path from the repository.



\---



\# API Endpoints



The main workflow includes endpoints for:



| Operation             | Purpose                  |

| --------------------- | ------------------------ |

| `GET /health`         | Service health check     |

| `POST /payments`      | Create a payment         |

| `GET /payments/{id}`  | Retrieve a payment       |

| Webhook endpoint      | Receive payment events   |

| Mock payment endpoint | Simulate payment results |



The exact endpoint paths can also be viewed through the automatically generated FastAPI Swagger documentation:



```text

http://127.0.0.1:8000/docs

```



and



```text

http://127.0.0.1:8001/docs

```



\---



\# Payment Flow



The complete simulated payment flow is:



```text

1\. Client / Postman

&#x20;       |

&#x20;       | Create payment

&#x20;       v

2\. Payment Integration Service

&#x20;       |

&#x20;       | HTTP request

&#x20;       v

3\. Mock Payment Gateway

&#x20;       |

&#x20;       | Creates payment/order

&#x20;       v

4\. Integration Service

&#x20;       |

&#x20;       | Stores payment

&#x20;       v

5\. SQLite Database

&#x20;       |

&#x20;       | Payment event

&#x20;       v

6\. Mock Payment Gateway

&#x20;       |

&#x20;       | HMAC-SHA256 signed webhook

&#x20;       v

7\. Webhook Handler

&#x20;       |

&#x20;       | Verify signature

&#x20;       v

8\. Check event\_id

&#x20;       |

&#x20;       | Prevent duplicate processing

&#x20;       v

9\. Update Payment Status

```



\---



\# Payment States



The simulated payment lifecycle supports:



```text

created

&#x20;  |

&#x20;  +----> paid

&#x20;  |

&#x20;  +----> failed

```



\### Successful Payment



```text

created → paid

```



\### Failed Payment



```text

created → failed

```



\---



\# Webhook Security



Webhook requests are protected using an HMAC-SHA256 signature.



The webhook request contains:



```text

X-Webhook-Signature

```



The receiving service calculates the expected signature using the shared webhook secret and compares it with the received signature.



\### Missing Signature



If the webhook does not contain the required signature:



```text

401 Unauthorized

```



\### Invalid Signature



If the signature does not match:



```text

401 Unauthorized

```



This demonstrates a common pattern used to verify that webhook payloads came from a trusted source.



\---



\# Webhook Idempotency



Webhook providers may retry event delivery.



Without idempotency, the same payment event could potentially be processed multiple times.



This project prevents that by assigning each webhook event a unique:



```text

event\_id

```



Processed event IDs are stored in the database.



When the same event is received again, the service detects the duplicate and returns:



```json

{

&#x20; "status": "already\_processed"

}

```



This prevents duplicate processing of the same payment event.



\---



\# Example Payment Request



Example request:



```http

POST /payments

Content-Type: application/json

```



Example JSON:



```json

{

&#x20; "amount": 499.00,

&#x20; "currency": "INR",

&#x20; "customer\_id": "customer\_001"

}

```



The integration service processes the request and communicates with the mock payment gateway.



\---



\# Example Webhook Event



A simulated webhook event follows the general structure:



```json

{

&#x20; "event\_id": "evt\_001",

&#x20; "payment\_id": "pay\_001",

&#x20; "status": "paid"

}

```



The mock gateway signs the webhook using HMAC-SHA256 before sending it to the integration service.



The integration service:



1\. Receives the webhook

2\. Reads the signature

3\. Calculates the expected HMAC-SHA256 signature

4\. Verifies the signature

5\. Checks whether `event\_id` was already processed

6\. Stores the event if it is new

7\. Updates the payment status



\---



\# Postman Testing



The project includes a Postman workflow for testing the complete payment lifecycle.



The demonstrated scenarios include:



1\. Health check

2\. Create payment

3\. Get payment

4\. Simulate successful payment

5\. Get updated payment

6\. Simulate failed payment

7\. Test duplicate webhook event

8\. Test nonexistent payment



The Postman workflow was successfully tested against the local services.



\---



\# Automated Testing



Run the test suite with:



```powershell

pytest

```



The current test suite contains:



```text

7 passed

```



Tests cover:



\* Health check

\* Payment creation

\* Payment retrieval

\* Invalid payment amount

\* Missing webhook signature

\* Invalid webhook signature

\* Nonexistent payment handling



\---



\# What This Project Demonstrates



This project demonstrates practical backend and API-integration concepts including:



\### Backend Development



\* FastAPI REST services

\* Request validation

\* HTTP error handling

\* Service-to-service communication



\### API Integration



\* Consuming another REST API using HTTPX

\* Designing an integration layer

\* Handling external API responses

\* Payment lifecycle management



\### Webhooks



\* Receiving asynchronous events

\* HMAC-SHA256 signature verification

\* Webhook security

\* Duplicate event handling



\### Database



\* SQLAlchemy ORM

\* SQLite persistence

\* Payment state management

\* Processed-event tracking



\### Testing



\* Automated API testing

\* Pytest

\* Async testing

\* Postman-based API testing



\### Software Engineering



\* Environment-based configuration

\* Git version control

\* `.gitignore` configuration

\* Separation of services

\* API documentation through FastAPI Swagger



\---



\# Security and Configuration



The repository excludes local and sensitive files through `.gitignore`, including:



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



\---



\# Disclaimer



This project is a \*\*locally implemented mock payment gateway integration for educational and portfolio purposes\*\*.



It does not connect to or process payments through a real payment provider.



The payment gateway is simulated locally to demonstrate backend integration patterns such as:



\* REST APIs

\* Webhooks

\* HMAC signature verification

\* Idempotency

\* Payment state management

\* Database persistence

\* API testing



\---



\## Author



\*\*Palak Srivastava\*\*



GitHub:

https://github.com/palaksriv



