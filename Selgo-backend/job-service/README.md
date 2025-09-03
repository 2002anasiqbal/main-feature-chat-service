# File: job-service/README.md

# Job Service

The Job Service is a comprehensive microservice for the Selgo marketplace that handles job management, CV building, profile management, salary comparison, and article content.

## Features

### 🔥 Core Job Features (8 Main Components)

1. **Complete Resume Builder** - Multi-step CV creation with PDF generation
2. **Find Jobs from Pool of Jobs** - Advanced job search with filtering and pagination
3. **Last Viewed Jobs** - Track and display user's recently viewed jobs
4. **Recommendation of Jobs** - Personalized job recommendations
5. **Salary Comparison** - Anonymous salary data collection and comparison
6. **Useful Articles** - Job-related articles and content management
7. **Download Profile as CV / Add a CV** - CV generation and file upload
8. **Job Description Pages** - Detailed job information and company details

### 🛠️ Technical Features

- **FastAPI** with automatic OpenAPI documentation
- **PostgreSQL** with SQLAlchemy ORM
- **JWT Authentication** integration with auth service
- **File Upload & Management** for CVs and documents
- **PDF Generation** with WeasyPrint and Jinja2 templates
- **Redis Caching** for improved performance
- **Full-text Search** capabilities
- **Geolocation Support** for location-based job filtering
- **RESTful API** design with comprehensive error handling

## Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL 14+
- Redis 7+
- Docker & Docker Compose

### Installation

1. **Clone and setup**:
```bash
cd selgo-backend/job-service
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. **Environment setup**:
```bash
cp .env.example .env
# Edit .env with your database credentials
```

3. **Database setup**:
```bash
# Initialize Alembic
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

4. **Run the service**:
```bash
python main.py
```

### Using Docker

```bash
# From the root selgo-backend directory
docker-compose up job-service
```

## API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8002/docs
- **ReDoc**: http://localhost:8002/redoc

## API Endpoints

### Jobs
- `GET /api/v1/jobs/search` - Search jobs with filters
- `GET /api/v1/jobs/featured` - Get featured jobs
- `GET /api/v1/jobs/recent` - Get recent jobs
- `GET /api/v1/jobs/recommendations` - Get personalized recommendations
- `GET /api/v1/jobs/viewed` - Get last viewed jobs
- `GET /api/v1/jobs/{id}` - Get job details
- `POST /api/v1/jobs/{id}/save` - Save job

### Profile Management
- `GET /api/v1/profile` - Get job profile
- `PUT /api/v1/profile` - Update profile
- `POST /api/v1/profile/experience` - Add work experience
- `POST /api/v1/profile/education` - Add education
- `POST /api/v1/profile/skills` - Add skills
- `POST /api/v1/profile/languages` - Add languages

### CV Builder
- `POST /api/v1/cv/build` - Build CV from data
- `POST /api/v1/cv/generate-from-profile` - Generate from profile
- `POST /api/v1/cv/upload` - Upload CV file
- `GET /api/v1/cv/{id}/download` - Download CV

### Salary Comparison
- `POST /api/v1/salary/compare` - Compare salaries
- `POST /api/v1/salary/add` - Add salary data
- `GET /api/v1/salary/insights/{job_title}` - Get insights

### Articles
- `GET /api/v1/articles` - Get articles
- `GET /api/v1/articles/featured` - Featured articles
- `GET /api/v1/articles/search` - Search articles
- `GET /api/v1/articles/popular-searches` - Popular searches

## Database Schema

### Core Tables
- `jobs` - Job postings with full details
- `companies` - Company information
- `job_categories` - Job categorization
- `job_profiles` - User job profiles
- `work_experiences` - Work history
- `educations` - Educational background
- `skills` & `user_skills` - Skills management
- `languages` & `user_languages` - Language proficiency
- `cvs` - Generated CVs
- `uploaded_cvs` - User uploaded CVs
- `articles` - Job-related articles
- `salary_entries` - Anonymous salary data

## Configuration

Key environment variables:

```env
# Database
DB_USER=postgres
DB_PASSWORD=12345
DB_HOST=localhost
DB_PORT=5432
DB_NAME=selgo_job

# API
API_HOST=0.0.0.0
API_PORT=8002

# Auth Service
AUTH_SERVICE_URL=http://auth-service:8001

# Redis
REDIS_URL=redis://redis:6379

# File Uploads
MAX_FILE_SIZE=10485760  # 10MB
ALLOWED_FILE_TYPES=[".pdf", ".doc", ".docx", ".jpg", ".jpeg", ".png"]
```

## Development

### Running Tests
```bash
pytest tests/
```

### Code Style
```bash
black src/
flake8 src/
```

### Database Migrations
```bash
# Create migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

## Frontend Integration

The service is designed to work seamlessly with the Next.js frontend. Key integration points:

### Job Search Integration
```javascript
// Frontend usage example
const searchJobs = async (params) => {
  const response = await fetch('/api/v1/jobs/search', {
    method: 'POST',
    body: JSON.stringify(params)
  });
  return response.json();
};
```

### CV Builder Integration
```javascript
// Complete CV builder flow
const buildCV = async (cvData) => {
  const response = await fetch('/api/v1/cv/build', {
    method: 'POST',
    headers: { 'Authorization': `Bearer ${token}` },
    body: JSON.stringify(cvData)
  });
  return response.json();
};
```

## Performance

- **Caching**: Redis caching for frequently accessed data
- **Database Indexing**: Optimized indexes for search performance
- **Pagination**: All list endpoints support pagination
- **File Storage**: Efficient file handling with size limits
- **Search Optimization**: Full-text search with PostgreSQL

## Security

- **JWT Authentication** with auth service integration
- **Input Validation** with Pydantic models
- **File Upload Security** with type and size validation
- **SQL Injection Protection** via SQLAlchemy ORM
- **CORS Configuration** for cross-origin requests

## Monitoring & Logging

- **Health Check**: `/health` endpoint
- **Structured Logging** with Python logging
- **Error Tracking** with detailed error responses
- **Request/Response Logging** for debugging

## Deployment

### Production Checklist

1. **Environment Variables**: Set all production values
2. **Database**: Run migrations on production DB
3. **File Storage**: Configure persistent volume for uploads
4. **SSL/TLS**: Enable HTTPS in production
5. **Monitoring**: Set up application monitoring
6. **Backup**: Configure database backups

### Docker Deployment
```bash
# Build and run
docker-compose up --build job-service

# Scale if needed
docker-compose up --scale job-service=3
```

## Support

For issues and questions:
1. Check the API documentation at `/docs`
2. Review logs for error details
3. Verify database connections and migrations
4. Ensure auth service is running for protected endpoints

## Contributing

1. Follow the established code structure
2. Add tests for new features
3. Update documentation
4. Follow semantic commit messages
5. Ensure all tests pass before submitting