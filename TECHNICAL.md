# Technical Documentation

![Architecture Concept](arch-diagram.jpeg)

*High-level architecture concept showing the flow from request to persistence.*

---

## System Design & Decisions

This architecture wasn't just "thrown together"; every layer exists to solve a specific problem. Here is the thought process behind the design:

### 1. **The "Three-Layer" Cake (Application → Service → Model)**
**Decision:** I separated the code into three distinct layers.
*   **Why?** If we put everything in one file, it becomes a nightmare to test or change later.
*   **How it works:**
    *   **Application Layer**: Handles the HTTP "doors". It validates what comes in (JSON) but knows *nothing* about business rules.
    *   **Service Layer**: The "brain". This is where logic lives (e.g., "You can't delete a seashell if it's already deleted"). It doesn't care about HTTP status codes.
    *   **Model Layer**: The "vault". It strictly defines what our data looks like in the database.

### 2. **Docker Containers (Isolation)**
**Decision:** I placed the API and the Database in separate containers.
*   **Why?**
    *   **Independence**: I can upgrade the API (Python) without touching the Database (PostgreSQL).
    *   **Safety**: If the API crashes, the Database stays alive.
    *   **Scalability**: In the future, I could run 5 API containers talking to 1 Database.

### 3. **The "Middleware" Guard**
**Decision:** I added a custom Middleware layer that sits before the Application Layer.
*   **Why?** We need to know *what* is happening.
*   **Benefit**: Every single request is logged with its duration. If the API feels slow, I check the logs and see "POST /seashells took 2.5s" immediately.

### 4. **Flexible Database Strategy (Environment Driven)**
**Decision:** The system connects to the database purely via the `DATABASE_URL` environment variable.
*   **Why?** This decouples the code from the infrastructure, allowing it to run anywhere.
    *   **Docker Compose**: Automatically connects to the internal `db` container (Zero config).
    *   **Custom / Remote**: Can connect to *any* PostgreSQL instance (Localhost, Render, AWS) just by changing the variable in the local .env file (or environment variables).

### 5. **Quality Gate (CI/CD)**
**Decision:** I built a GitHub Actions pipeline that runs on every push.
*   **Why?** Humans forget. Machines don't.
*   **The Check**: Before any code is accepted, it must pass 1) Linting (Ruff) and 2) Tests (Pytest). This guarantees the "Main" branch is always clean and deployable.

---

## Challenge Requirements & Engineering Decisions

I designed the system to specifically address the constraints mentioned in the challenge description:

### **Requirement: "Extensive collection of seashells"**
*   **Design Consideration**: An "extensive" list can mean thousands or millions of records. Loading them all at once would crash the frontend or slow the DB.
*   **Solution**: **Offset Pagination**.
    *   The API defaults to 10 items per page (`limit=10`).
    *   This ensures the app remains fast whether James has 50 shells or 50,000.

### **Requirement: "Add a new seashell (Name, Species, Description, etc.)"**
*   **Design Consideration**: The "etc." implies that data requirements might change (e.g., adding `location_found` or `size` later).
*   **Solution**: **Alembic Migrations**.
    *   I did not just create a static database script.
    *   I set up `Alembic` so we can easy add new columns (`alembic revision`) without deleting the database. The schema is evolvable.

### **Requirement: "Hard time tracking the seashells"**
*   **Design Consideration**: "Hard time tracking" implies data is precious. Accidental deletion would be a disaster.
*   **Solution**: **Soft Deletes**.
    *   When James hits "Delete", the record isn't removed. We just set `deleted=true`.
    *   The API automatically filters these out, but the data remains in Postgres if we ever need to recover it.

### **Requirement: "Persist data using a database of your choice"**
*   **Design Consideration**: We need something reliable for structured data.
*   **Solution**: **PostgreSQL** (vs. SQLite).
    *   SQLite is fine for a toy app, but Postgres is the industry standard for production.
    *   It supports concurrent writes (James and Anna editing at the same time) and strong data integrity.

### **Requirement: "Easy to consume API documentation"**
*   **Design Consideration**: The frontend developer needs to know exactly what JSON to send.
*   **Solution**: **Swagger UI & ReDoc**.
    *   I didn't just write a README.
    *   The API auto-generates interactive docs at `/docs`. You can test endpoints directly in the browser - no guessing required.

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

## CI/CD Pipeline

**GitHub Actions** (`.github/workflows/test.yml`) automates testing on every push/PR.

**Workflow:**
1.  **Trigger**: Push to `main`
2.  **Linting**: Enforces strict code style with **Ruff** (fails on unused imports, bad formatting)
3.  **Environment**: Ubuntu latest + Python 3.12
3.  **Service**: Spins up a **real PostgreSQL container** (integration test ready)
4.  **Action**: Installs dependencies and runs `pytest`
5.  **Result**: Blocks merge if tests fail

---

Built for the Seashell Collection Backend Challenge
