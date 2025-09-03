# Developer Setup Guide

This guide will help you set up the Selgo Boat Service development environment on your local machine.

## Prerequisites

Before you begin, make sure you have the following installed:

- **Python 3.9+**: https://www.python.org/downloads/
- **PostgreSQL 12+ with PostGIS**: https://www.postgresql.org/download/
- **Docker and Docker Compose** (optional, but recommended): https://docs.docker.com/get-docker/
- **Git**: https://git-scm.com/downloads

## Setup Steps

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/selgo-backend.git
cd selgo-backend
```

### 2. Using Docker (Recommended)

The easiest way to get started is using Docker Compose, which will set up all the required services for you.

```bash
# Start the services
docker-compose up -d

# View the logs
docker-compose logs -f boat-service
```

This will start:
- The Boat service on port 8000
- PostgreSQL with PostGIS on port 5432
- pgAdmin (for database management) on port 5050

Access the services:
- API: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- pgAdmin: http://localhost:5050 (email: admin@selgo.com, password: admin)

### 3. Manual Setup (Without Docker)

If you prefer not to use Docker, follow these steps for a manual setup:

#### 3.1. Set Up a Virtual Environment

```bash
cd boat-service
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### 3.2. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 3.3. Set Up PostgreSQL

First, make sure PostgreSQL is running on your system. Then:

```bash
# Create the database
createdb selgo_boat

# Connect to the database and enable PostGIS
psql -d selgo_boat -c "CREATE EXTENSION postgis;"
```

#### 3.4. Configure Environment Variables

Create a `.env` file in the `boat-service` directory:

```
DB_USER=your_postgres_username
DB_PASSWORD=your_postgres_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=selgo_boat
API_HOST=localhost
API_PORT=8000
DEBUG=True
ENVIRONMENT=development
SECRET_KEY=your-secret-key-for-jwt
UPLOAD_FOLDER=./uploads
```

#### 3.5. Run Database Migrations

```bash
# Initialize Alembic (if not already done)
alembic init alembic

# Run migrations
alembic upgrade head
```

#### 3.6. Seed the Database

```bash
python scripts/seed_db.py
```

#### 3.7. Start the Service

```bash
python main.py
```

The service will be available at http://localhost:8000.

## Development Workflow

### Code Organization

- **Models**: Add new models in `src/models/boat_models.py`
- **Schemas**: Add Pydantic schemas in `src/models/boat_schemas.py`
- **Repositories**: Add data access logic in `src/repositories/repositories.py`
- **Services**: Add business logic in `src/services/services.py`
- **API Routes**: Add API endpoints in `src/api/routes.py`

### Database Migrations

After changing models:

```bash
# Generate a new migration
alembic revision --autogenerate -m "Description of changes"

# Apply the migration
alembic upgrade head
```

### Running Tests

```bash
# Run all tests
pytest tests/

# Run specific tests
pytest tests/test_api.py

# Run with coverage
pytest --cov=src tests/
```

### Linting and Formatting

```bash
# Check code style with flake8
flake8 src/ tests/

# Format code with black
black src/ tests/

# Sort imports with isort
isort src/ tests/
```

## Troubleshooting

### Common Issues

#### Docker Compose Issues

**Problem**: Services fail to start
**Solution**: Check Docker logs with `docker-compose logs -f`

#### PostgreSQL Connection Issues

**Problem**: Cannot connect to PostgreSQL
**Solution**:
- Check that PostgreSQL is running: `pg_isready`
- Verify connection details in `.env` file

#### Migration Issues

**Problem**: Alembic migrations fail
**Solution**:
- Check database connection
- Reset migrations: `alembic downgrade base` then `alembic upgrade head`

#### PostGIS Issues

**Problem**: GeoAlchemy2 errors with "function ST_* does not exist"
**Solution**: Verify PostGIS extension is installed: `psql -d selgo_boat -c "\dx"`

## Getting Help

If you encounter any issues not covered in this guide:

1. Check the project documentation
2. Search for similar issues in the project repository
3. Ask for help from team members

## Next Steps

Once your environment is set up, you can:

1. Familiarize yourself with the codebase
2. Run the service and explore the API using Swagger UI
3. Make your first contribution by:
   - Fixing a bug
   - Adding a new feature
   - Improving documentation
   - Writing tests

Happy coding!