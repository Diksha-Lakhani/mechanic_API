# Mini Mechanic Service API

A backend API for a mechanic-service platform where users can view mechanics and create service requests. Built with Django REST Framework and PostgreSQL.

## Features

- Full CRUD for mechanics (list, retrieve, create, update, delete)
- Service request creation with validation against a mechanic's offered services
- Field-level and cross-field validation (phone numbers, vehicle numbers, service availability, mechanic existence)
- Django admin panel for data management
- Automated tests covering core success and error paths

## Tech Stack

- Python, Django, Django REST Framework
- PostgreSQL
- python-decouple (environment-based configuration)

## Project Structure

    mechanic-service-api/
    ├── mechanic_service/     # Project settings, root URL config
    ├── mechanics/            # App: models, serializers, views, tests
    ├── requirements.txt
    ├── .env                  # Not committed — see setup below
    └── manage.py

## Data Model

**Mechanic**: id, name, phone, location, rating, is_open, services (comma-separated list)

**ServiceRequest**: id, customer_name, customer_phone, vehicle_number, mechanic (foreign key), service, problem_description, status (default `PENDING`), created_at

One mechanic can have many service requests (one-to-many, enforced via a foreign key with `on_delete=CASCADE`).

**Design note:** `services` on Mechanic is a comma-separated text field rather than a separate `Service` model/table. This keeps the schema appropriately scoped for this assignment; a normalized `Service` table would be the better choice at larger scale.

## Setup Instructions

1. Clone the repository and navigate into it:

       git clone <your-repo-url>
       cd mechanic-service-api

2. Create and activate a virtual environment:

       python -m venv venv
       venv\Scripts\activate        # Windows
       source venv/bin/activate     # macOS/Linux

3. Install dependencies:

       pip install -r requirements.txt

4. Create a PostgreSQL database:

       CREATE DATABASE mechanic_service_db;

5. Create a `.env` file in the project root with:

       DB_NAME=mechanic_service_db
       DB_USER=postgres
       DB_PASSWORD=your_password
       DB_HOST=localhost
       DB_PORT=5432
       SECRET_KEY=your_secret_key

6. Run migrations:

       python manage.py migrate

7. (Optional) Create an admin user:

       python manage.py createsuperuser

8. Run the development server:

       python manage.py runserver

The API is now available at `http://127.0.0.1:8000/api/`.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | /api/mechanics/ | List all mechanics |
| POST | /api/mechanics/ | Add a new mechanic |
| GET | /api/mechanics/{id}/ | Get a mechanic by ID |
| PUT/PATCH | /api/mechanics/{id}/ | Update a mechanic |
| DELETE | /api/mechanics/{id}/ | Delete a mechanic |
| GET | /api/service-requests/ | List all service requests |
| POST | /api/service-requests/ | Create a service request |
| GET | /api/service-requests/{id}/ | Get a service request by ID |
| PUT/PATCH | /api/service-requests/{id}/ | Update a service request |
| DELETE | /api/service-requests/{id}/ | Delete a service request |

## Sample Requests

### Create a mechanic

    POST /api/mechanics/
    Content-Type: application/json

    {
      "name": "Bob's Garage",
      "phone": "9876543210",
      "location": "Pune",
      "rating": 4.5,
      "is_open": true,
      "services": "Oil Change, Tire Repair"
    }

**Response `201 Created`:**

    {
      "id": 1,
      "name": "Bob's Garage",
      "phone": "9876543210",
      "location": "Pune",
      "rating": "4.5",
      "is_open": true,
      "services": "Oil Change, Tire Repair"
    }

### Create a service request

    POST /api/service-requests/
    Content-Type: application/json

    {
      "customer_name": "Alice",
      "customer_phone": "9988776655",
      "vehicle_number": "MH12AB1234",
      "mechanic": 1,
      "service": "Oil Change",
      "problem_description": "Engine making noise"
    }

**Response `201 Created`:**

    {
      "id": 1,
      "customer_name": "Alice",
      "customer_phone": "9988776655",
      "vehicle_number": "MH12AB1234",
      "mechanic": 1,
      "service": "Oil Change",
      "problem_description": "Engine making noise",
      "status": "PENDING",
      "created_at": "2026-09-03T10:00:00Z"
    }

### Error example — invalid phone number

    POST /api/mechanics/
    { "name": "Test", "phone": "123", "location": "Pune", "services": "Oil Change" }

**Response `400 Bad Request`:**

    { "phone": ["Phone number must be exactly 10 digits."] }

### Error example — service not offered by mechanic

    POST /api/service-requests/
    { ..., "mechanic": 1, "service": "Wheel Alignment" }

**Response `400 Bad Request`:**

    { "service": "'Wheel Alignment' is not offered by this mechanic. Available services: Oil Change, Tire Repair" }

## Running Tests

    python manage.py test

Covers: mechanic CRUD, required-field validation, phone number validation, service-request creation, invalid mechanic reference, and invalid service validation.

## Admin Panel

Visit `http://127.0.0.1:8000/admin/` and log in with your superuser credentials to view/manage data through Django's built-in admin interface.