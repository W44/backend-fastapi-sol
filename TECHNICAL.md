# Technical Documentation

Backend implementation details, architecture, and deployment guide for the Seashell Collection API.

---

## Technologies Used

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Framework** | FastAPI | Modern, fast API framework |
| **Database** | PostgreSQL | Production-grade SQL database |
| **ORM** | SQLModel | Type-safe database models |
| **Validation** | Pydantic | Request/response validation |
| **Server** | Uvicorn | ASGI web server |
| **Migrations** | Alembic | Database schema versioning |
| **Testing** | Pytest | Unit and integration tests |
| **Container** | Docker | Containerization |

---

## Architecture Overview

### Layered Design

```
API Layer (app/api/)         - Routes, HTTP handling
Service Layer (app/services/) - Business logic
Model Layer (app/models/)     - Database ORM
```

---

## Database Schema

```sql
CREATE TABLE seashell (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    species VARCHAR NOT NULL,
    description VARCHAR,
    deleted BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
```

### Migrations

```bash
# View current status
alembic current

# Apply migrations
alembic upgrade head

# Create new migration
alembic revision --autogenerate -m "Description"
```

---

## Logging & Monitoring

### Configuration

```bash
# Configure log level in .env
LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR, CRITICAL
```

### What's Logged

- All API requests/responses with timing
- CRUD operations with IDs
- Errors with stack traces
- Application lifecycle events

### Example Output

```
2026-02-08 18:15:32 - app.main - INFO - Starting up Seashell API
2026-02-08 18:15:33 - app.main - INFO - Incoming request: POST /seashells/
2026-02-08 18:15:33 - app.services.seashell_service - INFO - Creating: Queen Conch
2026-02-08 18:15:33 - app.main - INFO - Request completed: POST /seashells/ - Status: 201 - Time: 0.045s
```

### Health Check

```http
GET /health

Response: {"status": "ok"}
```

---

## Docker Build Strategy

I used a **multi-stage build** (Stage 1: Validation, Stage 2: Runtime).

**Decision:**
Run tests during image build to enforce a strict quality gate. If tests fail, no image is created.

**Benefits:**
1.  **Zero Broken Code**: Prevents deploying failing code.
2.  **CI/CD Standard**: Automates validation on every build.

```bash
# Manual verification
docker-compose run --rm api pytest tests/ -v
```

---

## Docker Deployment

### Build & Push

```bash
# Build image
docker build -t seashell-api .

# Tag for Docker Hub
docker tag seashell-api username/seashell-api:latest

# Push
docker push username/seashell-api:latest
```

### Run with External Database

```bash
docker run -d \
  -p 8000:8000 \
  -e DATABASE_URL="postgresql://user:pass@host:5432/db" \
  -e LOG_LEVEL="INFO" \
  --name seashell-api \
  username/seashell-api:latest
```

> [!IMPORTANT]
> The Docker image does NOT include a database. Use docker-compose for local development, or provide a remote DATABASE_URL for production.

---

## Testing

### Run Tests

```bash
# Run test suite
python -m pytest tests/ -v

# With coverage
python -m pytest tests/ --cov=app --cov-report=term-missing
```

### Test Structure

- `tests/conftest.py` - Test fixtures and database setup
- `tests/test_seashells.py` - API endpoint tests

---

Built for the Seashell Collection Backend Challenge
