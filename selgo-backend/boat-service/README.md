# Selgo Boat Service

This is the backend service for the boat module of the Selgo application. It provides APIs for managing boat listings, categories, features, ratings, and more.

## Table of Contents

- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the Service](#running-the-service)
- [API Documentation](#api-documentation)
- [Database](#database)
- [Development](#development)
- [Testing](#testing)
- [Docker](#docker)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Boat Categories**: API for managing boat categories and subcategories
- **Boat Features**: API for managing boat features
- **Boat Listings**: API for creating, reading, updating, and deleting boat listings
- **Boat Images**: API for managing boat images
- **Boat Ratings**: API for rating boats
- **Fix Done Requests**: API for secure transactions between buyers and sellers
- **Loan Estimation**: API for calculating loan payments for boats
- **Filtering and Searching**: API for filtering and searching boat listings
- **Geospatial Queries**: API for location-based searches

## Technology Stack

- **Python 3.9+**: Programming language
- **FastAPI**: Web framework for building APIs
- **SQLAlchemy**: ORM for database interactions
- **Pydantic**: Data validation and settings management
- **PostgreSQL**: Database for storing application data
- **PostGIS**: Spatial database extension for PostgreSQL
- **GeoAlchemy2**: Geospatial extension for SQLAlchemy
- **Alembic**: Database migration tool
- **Docker**: Containerization

## Project Structure

```
selgo-backend/
├── boat-service/                 # Boat microservice
│   ├── src/
│   │   ├── api/                  # API routes
│   │   ├── config/               # Configuration files
│   │   ├── database/             # Database connection and utilities
│   │   ├── models/               # Database models
│   │   ├── repositories/         # Data access layer
│   │   ├── services/             # Business logic
│   │   ├── utils/                # Utility functions
│   │   ├── app.py                # FastAPI application
│   │   └── main.py               # Entry point
│   ├── alembic/                  # Database migrations
│   ├── scripts/                  # Utility scripts
│   ├── tests/                    # Unit and integration tests
│   ├── uploads/                  # File uploads directory
│   ├── requirements.txt          # Dependencies
│   ├── Dockerfile                # Docker configuration
│   └── .env                      # Environment variables
└── docker-compose.yml            # Docker Compose configuration
```

## Getting Started

### Prerequisites

- Python 3.9+
- PostgreSQL 12+ with PostGIS extension
- Docker and Docker Compose (optional)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/selgo.git
cd selgo
```

2. Set up a virtual environment:
```bash
cd boat-service
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a PostgreSQL database with PostGIS extension:
```sql
CREATE DATABASE selgo_boat;
\c selgo_boat
CREATE EXTENSION postgis;
```

5. Create a `.env` file with your configuration:
```
DB_USER=postgres
DB_PASSWORD=123
DB_HOST=localhost
DB_PORT=5432
DB_NAME=selgo_boat
API_HOST=localhost
API_PORT=8000
DEBUG=True
ENVIRONMENT=development
```

### Running the Service

1. Apply database migrations:
```bash
alembic upgrade head
```

2. Seed the database with initial data:
```bash
python scripts/seed_db.py
```

3. Start the service:
```bash
python main.py
```

The service will be available at http://localhost:8000.

## API Documentation

FastAPI automatically generates API documentation. After starting the service, you can access the documentation at:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Database

The service uses PostgreSQL with the PostGIS extension for geospatial queries. The database schema is managed using Alembic migrations.

To create a new migration after changing the models:

```bash
alembic revision --autogenerate -m "Description of changes"
```

To apply migrations:

```bash
alembic upgrade head
```

## Development

For local development:

1. Start the services using Docker Compose:
```bash
docker-compose up -d
```

This will start the boat service, PostgreSQL, and pgAdmin. The service will automatically reload when you make changes to the code.

2. Access pgAdmin at http://localhost:5050 to manage the database.

## Testing

Run tests:

```bash
pytest tests/
```

## Docker

Build the Docker image:

```bash
docker build -t selgo-boat-service .
```

Run the container:

```bash
docker run -p 8000:8000 --env-file .env selgo-boat-service
```

## Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some feature'`)
5. Push to the branch (`git push origin feature/your-feature`)
6. Open a Pull Request

## License



## Boat Module API Endpoints

The boat module provides the following API endpoints:

### Boat Categories

- **GET /api/v1/boats/categories** - Get all boat categories
- **GET /api/v1/boats/categories/with-counts** - Get all boat categories with counts
- **GET /api/v1/boats/categories/top-level** - Get top-level boat categories
- **GET /api/v1/boats/categories/{category_id}** - Get a specific boat category
- **GET /api/v1/boats/categories/{category_id}/subcategories** - Get subcategories of a category
- **POST /api/v1/boats/categories** - Create a new boat category
- **PUT /api/v1/boats/categories/{category_id}** - Update a boat category
- **DELETE /api/v1/boats/categories/{category_id}** - Delete a boat category

### Boat Features

- **GET /api/v1/boats/features** - Get all boat features
- **GET /api/v1/boats/features/{feature_id}** - Get a specific boat feature
- **POST /api/v1/boats/features** - Create a new boat feature
- **PUT /api/v1/boats/features/{feature_id}** - Update a boat feature
- **DELETE /api/v1/boats/features/{feature_id}** - Delete a boat feature

### Boat Listings

- **GET /api/v1/boats** - Get all boat listings
- **GET /api/v1/boats/{boat_id}** - Get a specific boat listing
- **GET /api/v1/boats/recommended** - Get recommended boat listings
- **POST /api/v1/boats** - Create a new boat listing
- **POST /api/v1/boats/filter** - Filter boat listings
- **PUT /api/v1/boats/{boat_id}** - Update a boat listing
- **DELETE /api/v1/boats/{boat_id}** - Delete a boat listing

### Boat Images

- **GET /api/v1/boats/{boat_id}/images** - Get all images for a boat
- **POST /api/v1/boats/{boat_id}/images** - Add an image to a boat
- **DELETE /api/v1/boats/images/{image_id}** - Delete a boat image
- **POST /api/v1/boats/upload-image** - Upload an image file

### Boat Ratings

- **GET /api/v1/boats/{boat_id}/ratings** - Get ratings for a boat
- **POST /api/v1/boats/{boat_id}/ratings** - Rate a boat
- **DELETE /api/v1/boats/ratings/{rating_id}** - Delete a rating

### Fix Done Requests

- **GET /api/v1/boats/{boat_id}/fix-requests** - Get fix requests for a boat
- **GET /api/v1/boats/fix-requests/buyer** - Get fix requests where the user is the buyer
- **GET /api/v1/boats/fix-requests/seller** - Get fix requests where the user is the seller
- **POST /api/v1/boats/{boat_id}/fix-requests** - Create a fix request
- **PUT /api/v1/boats/fix-requests/{request_id}/status** - Update the status of a fix request

### Loan Estimation

- **POST /api/v1/boats/loan-estimate** - Calculate loan payments for a boat

## Integration with Other Modules

The boat service is designed to be part of a larger microservices architecture. It can be integrated with other modules such as:

- **User Service**: For authentication and user management
- **Notification Service**: For sending notifications about boat listings, fix requests, etc.
- **Payment Service**: For handling payments related to boat purchases and rentals
- **Chat Service**: For communication between buyers and sellers

## Extending for Other Modules

This boat service architecture can be used as a template for other modules in the Selgo application, such as:

- **Jobs Module**: For job listings and applications
- **Car and Caravan Module**: For car and caravan listings
- **Property Module**: For property listings
- **Square Module**: For general marketplace listings

The structure and patterns used in this service can be replicated for these other modules, ensuring consistency across the entire application.