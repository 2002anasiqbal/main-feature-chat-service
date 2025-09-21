# Selgo Chat Service

This is the backend service for the chat module of the Selgo application. It provides APIs for managing chat conversations, messages, and more.

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

- **Conversations**: API for managing chat conversations.
- **Messages**: API for sending, receiving, and managing messages.
- **Real-time Communication**: WebSocket support for real-time messaging.
- **User Presence**: API for tracking user online status.

## Technology Stack

- **Python 3.9+**: Programming language
- **FastAPI**: Web framework for building APIs
- **SQLAlchemy**: ORM for database interactions
- **Pydantic**: Data validation and settings management
- **PostgreSQL**: Database for storing application data
- **Alembic**: Database migration tool
- **Docker**: Containerization
- **WebSockets**: For real-time communication

## Project Structure

```
selgo-backend/
├── chat-service/                 # Chat microservice
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
│   ├── requirements.txt          # Dependencies
│   ├── Dockerfile                # Docker configuration
│   └── .env                      # Environment variables
└── docker-compose.yml            # Docker Compose configuration
```

## Getting Started

### Prerequisites

- Python 3.9+
- PostgreSQL 12+
- Docker and Docker Compose (optional)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/selgo.git
cd selgo
```

2. Set up a virtual environment:
```bash
cd chat-service
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a PostgreSQL database:
```sql
CREATE DATABASE selgo_chat;
```

5. Create a `.env` file with your configuration:
```
DB_USER=postgres
DB_PASSWORD=123
DB_HOST=localhost
DB_PORT=5432
DB_NAME=selgo_chat
API_HOST=localhost
API_PORT=8002
DEBUG=True
ENVIRONMENT=development
```

### Running the Service

1. Apply database migrations:
```bash
alembic upgrade head
```

2. Start the service:
```bash
python main.py
```

The service will be available at http://localhost:8002.

## API Documentation

FastAPI automatically generates API documentation. After starting the service, you can access the documentation at:

- **Swagger UI**: http://localhost:8002/docs
- **ReDoc**: http://localhost:8002/redoc

## Database

The service uses PostgreSQL for storing chat data. The database schema is managed using Alembic migrations.

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

This will start the chat service and PostgreSQL. The service will automatically reload when you make changes to the code.

2. Access pgAdmin at http://localhost:5050 to manage the database.

## Testing

Run tests:

```bash
pytest tests/
```

## Docker

Build the Docker image:

```bash
docker build -t selgo-chat-service .
```

Run the container:

```bash
docker run -p 8002:8002 --env-file .env selgo-chat-service
```

## Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some feature'`)
5. Push to the branch (`git push origin feature/your-feature`)
6. Open a Pull Request

## License



## Chat Module API Endpoints

The chat module provides the following API endpoints:

### Conversations

- **GET /api/v1/chats/conversations** - Get all conversations for the current user.
- **GET /api/v1/chats/conversations/{conversation_id}** - Get a specific conversation.
- **POST /api/v1/chats/conversations** - Create a new conversation.

### Messages

- **GET /api/v1/chats/conversations/{conversation_id}/messages** - Get all messages for a conversation.
- **POST /api/v1/chats/conversations/{conversation_id}/messages** - Send a new message.

### WebSockets

- **WS /api/v1/ws/{user_id}** - WebSocket endpoint for real-time communication.


## Integration with Other Modules

The chat service is designed to be part of a larger microservices architecture. It can be integrated with other modules such as:

- **User Service**: For authentication and user management
- **Notification Service**: For sending notifications about new messages.