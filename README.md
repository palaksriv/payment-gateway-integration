\# Payment Gateway Integration Service



A backend integration project that simulates a real-world payment gateway workflow using REST APIs, webhooks, HMAC signature verification, idempotency, SQLite persistence, Postman, and automated testing.



\## Overview



This project demonstrates how a backend application can integrate with an external payment provider.



A locally implemented mock payment gateway exposes REST APIs for creating orders and simulating payment events. The integration service consumes those APIs, stores payment information in SQLite, and processes signed webhook events.



\## Architecture



```text

Client / Postman

&#x20;      |

&#x20;      v

Payment Integration Service

FastAPI :8000

&#x20;      |

&#x20;      | HTTP / REST

&#x20;      v

Mock Payment Gateway

FastAPI :8001

&#x20;      |

&#x20;      | Signed Webhook

&#x20;      v

Payment Integration Service

&#x20;      |

&#x20;      v

SQLite Database



Features

REST API integration using HTTPX

Payment/order creation

SQLite persistence using SQLAlchemy

Payment status tracking

Webhook processing

HMAC-SHA256 webhook signature verification

Idempotent webhook event processing

Successful and failed payment simulation

HTTP error handling

Postman API collection

Automated API tests using pytest

Tech Stack

Python

FastAPI

HTTPX

SQLAlchemy

SQLite

Pydantic

Pytest

Postman

HMAC-SHA256

Project Structure

payment-gateway-integration/

│

├── integration\_service/

│   ├── main.py

│   ├── database.py

│   ├── models.py

│   ├── schemas.py

│   ├── gateway\_client.py

│   └── routes/

│       ├── payments.py

│       └── webhooks.py

│

├── mock\_gateway/

│   ├── main.py

│   ├── schemas.py

│   └── routes/

│       ├── orders.py

│       └── payments.py

│

├── tests/

│   └── test\_payments.py

│

├── postman/

│   └── Payment-Gateway-Integration.postman\_collection.json

│

├── .gitignore

├── requirements.txt

└── README.md

Setup

1\. Clone the repository

git clone <repository-url>

cd payment-gateway-integration

2\. Create a virtual environment



Windows:



python -m venv .venv

3\. Activate the virtual environment

.\\.venv\\Scripts\\Activate.ps1

4\. Install dependencies

pip install -r requirements.txt

Environment Variables



Create a .env file locally:



MOCK\_GATEWAY\_URL=http://127.0.0.1:8001

WEBHOOK\_SECRET=dev\_webhook\_secret\_123



Do not commit .env or real secrets to GitHub.



Running the Services

Terminal 1 — Mock Payment Gateway

python -m uvicorn mock\_gateway.main:app --reload --port 8001



The mock gateway runs at:



http://127.0.0.1:8001



Swagger documentation:



http://127.0.0.1:8001/docs

Terminal 2 — Integration Service

python -m uvicorn integration\_service.main:app --reload --port 8000



The integration service runs at:



http://127.0.0.1:8000



Swagger documentation:



http://127.0.0.1:8000/docs

API Endpoints

Integration Service

Method	Endpoint	Purpose

GET	/api/health	Health check

POST	/api/payments/create	Create a payment/order

GET	/api/payments/{order\_id}	Retrieve payment status

POST	/api/webhooks/payment	Process payment webhook

Mock Gateway

Method	Endpoint	Purpose

GET	/api/health	Health check

POST	/api/orders	Create mock gateway order

POST	/api/payments/simulate	Simulate payment event

Payment Flow

1\. Client sends payment request

&#x20;       |

&#x20;       v

2\. Integration service calls mock gateway

&#x20;       |

&#x20;       v

3\. Mock gateway creates an order

&#x20;       |

&#x20;       v

4\. Integration service stores payment in SQLite

&#x20;       |

&#x20;       v

5\. Gateway simulates payment event

&#x20;       |

&#x20;       v

6\. Gateway signs webhook using HMAC-SHA256

&#x20;       |

&#x20;       v

7\. Integration service verifies signature

&#x20;       |

&#x20;       v

8\. Payment status is updated

Webhook Security



Webhook payloads are signed using HMAC-SHA256.



The integration service:



Receives the raw webhook payload.

Generates the expected HMAC signature.

Compares it with the supplied signature.

Rejects requests with missing or invalid signatures.



Invalid signatures return:



401 Unauthorized

Idempotency



Webhook events contain a unique event ID.



Processed event IDs are stored in the database.



If the same event is received again, the service returns:



{

&#x20; "status": "already\_processed"

}



This prevents duplicate webhook deliveries from applying the same payment state transition multiple times.



Testing



Run:



pytest -v



The test suite covers:



Health check

Payment creation

Payment retrieval

Invalid payment amount

Missing webhook signature

Invalid webhook signature

Nonexistent payment handling

Postman



The repository includes:



postman/Payment-Gateway-Integration.postman\_collection.json



The collection demonstrates:



Health check

Payment creation

Payment retrieval

Successful payment webhook

Failed payment webhook

Duplicate webhook handling

Nonexistent payment handling



Import the collection into Postman and run the requests against the locally running services.



Disclaimer



This project uses a locally implemented mock payment gateway for educational and portfolio purposes. It does not process real payments or connect to a real payment provider.

