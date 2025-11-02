# Python (FastAPI) Backend for the Digital Health Backend Practical 


Note: Implemented in Python/FastAPI for faster delivery and clarity. Fully compatible with the original Java/Spring Boot spec.


The Original Exercise is designed for a Java (Spring Boot ) . This repository provides a FastAPI implementation of the same requirements using **Python (FastAPI)** with PostgreSQL,
preserving the same REST API design, validation rules and persistence model.

---

### Features 
- FeaturesFull CRUD: Patients & Encounters  
- Search: family, given, identifier, birthDate (partial match)  
- PostgreSQL + SQLAlchemy + Alembic  
- Validation + clean error responses  
- OpenAPI docs: http://localhost:8000/docs  
- Tests + Docker



### Run locally
```bash
docker-compose up --build
```

## Requirements
- Docker & docker-compose (recommended)
- Or Python 3.11+ and Postgres (local)

## Quick start with docker-compose (recommended)
1. Copy `.env.example` to `.env` and edit if needed:
   ```bash
   cp .env.example .env


Build and run:

docker-compose up --build


The API will be available at: http://localhost:8000

OpenAPI UI: http://localhost:8000/docs

This composes file exposes Postgres on 5432 and the web API on 8000. On start the web service runs alembic upgrade head then uvicorn.

Running locally without Docker

Create a Python venv and install deps:

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt


Ensure Postgres is running and reachable. Set env var DATABASE_URL or use .env.

Run migrations:

alembic upgrade head

Start the app:

uvicorn app.main:app --reload

Run tests

Tests assume a Postgres instance is available and the DB schema is migrated.

Using docker-compose:

Start just the db:

docker-compose up -d db


Run migrations:

docker-compose run --rm web alembic upgrade head


Run pytest locally (after installing requirements):

pytest -v
   #Design decisions
- FastAPI for high performance async API framework.
- SQLAlchemy ORM for database interactions.
- Pydantic models for data validation and serialization.
- Alembic for database migrations.
- Docker for containerization and easy setup.
- Pytest for testing framework.
- OpenAPI/Swagger for API documentation.
- Modular project structure for maintainability.
- Environment variables for configuration management.
- Logging for observability.
- Error handling with consistent responses.
- Pagination for list endpoints.
- CORS middleware for cross-origin requests.
- Dependency injection for better testability.
- Type hints for better code quality.
- GitHub Actions for CI/CD (if applicable).
- README documentation for setup and usage instructions.
- .env.example for environment variable template.
- Dockerfile for containerizing the application.
- docker-compose.yml for orchestrating services.
- .gitignore to exclude unnecessary files from version control.
- tests/ directory for unit and integration tests.
- app/ directory for application code.
- migrations/ directory for Alembic migration scripts.
- requirements.txt for Python dependencies.
- alembic.ini for Alembic configuration.
- app/main.py as the application entry point.
- app/models/ for SQLAlchemy models.
- app/schemas/ for Pydantic models.
- app/crud/ for CRUD operations.
- app/api/ for API route definitions.
- app/core/ for configuration and settings.
- app/db/ for database session management.
- app/services/ for business logic.
- app/utils/ for utility functions.
- tests/unit/ for unit tests.
- tests/integration/ for integration tests.
- CI/CD workflows for automated testing and deployment.
- Logging configuration for monitoring application behavior.
- Error handling middleware for consistent error responses.
- Pagination logic for list endpoints.
- Type hints for better code quality.


