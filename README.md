# Seashell Collection API

A RESTful backend service for managing seashell collections with persistent storage.

![CI Status](https://github.com/W44/backend-fastapi-sol/actions/workflows/test.yml/badge.svg)

**Features:**
- CRUD operations for seashell records
- Pagination, search, and sorting
- PostgreSQL database persistence
- Auto-generated API documentation (Swagger UI)
- Soft delete pattern
- **Production-Ready**: Multi-stage Docker builds, PostgreSQL persistence
- **Code Quality**: Automated Linting (Ruff) in CI pipeliness design

---

## For Frontend Developers

### Base URL

```
Local: http://localhost:8000
Docker: http://localhost:8000
```

> See [Quick Start](#quick-start-local-setup) for setup instructions.

### Interactive Documentation

Best way to explore the API (After Backend is running):

- **Swagger UI**: http://localhost:8000/docs (Try it live)
- **ReDoc**: http://localhost:8000/redoc (Clean reference)
- **OpenAPI Spec**: http://localhost:8000/openapi.json (Generate client SDKs)

### Quick API Reference

#### 1. Create Seashell

```http
POST /seashells
Content-Type: application/json

{
  "name": "Queen Conch",
  "species": "Strombus gigas",
  "description": "Large tropical shell with pink interior"
}
```

**Response:** `201 Created`

```json
{
  "id": 1,
  "name": "Queen Conch",
  "species": "Strombus gigas",
  "description": "Large tropical shell with pink interior"
}
```

#### 2. List Seashells

```http
GET /seashells?page=1&page_size=10&sort_by=name&order=asc&name=conch
```

**Query Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `page` | integer | 1 | Page number |
| `page_size` | integer | 10 | Items per page (max 100) |
| `sort_by` | string | id | Sort field: `id`, `name`, `species`, `description` |
| `order` | string | asc | `asc` or `desc` |
| `name` | string | - | Search by name (case-insensitive) |
| `species` | string | - | Filter by species (case-insensitive) |

**Response:** `200 OK`

```json
[
  {
    "id": 1,
    "name": "Queen Conch",
    "species": "Strombus gigas",
    "description": "Large tropical shell with pink interior"
  }
]
```

#### 3. Get Single Seashell

```http
GET /seashells/{id}
```

**Response:** `200 OK` or `404 Not Found`

#### 4. Update Seashell

```http
PUT /seashells/{id}
Content-Type: application/json

{
  "description": "Updated description"
}
```

**Note:** All fields optional - only updates what you send

**Response:** `200 OK`

#### 5. Delete Seashell

```http
DELETE /seashells/{id}
```

**Response:** `204 No Content`

**Note:** Soft delete - data preserved with `deleted=true`

### Error Responses

| Status Code | Meaning |
|-------------|---------|
| `200 OK` | Success |
| `201 Created` | Resource created |
| `204 No Content` | Success (no response body) |
| `404 Not Found` | Resource doesn't exist |
| `422 Unprocessable Entity` | Validation error |

---

## Quick Start (Local Setup)

### Option 1: Docker Compose (Recommended)

Easiest way - includes database.

```bash
# Start everything (API + Database)
docker-compose up -d

# Optional: Set custom credentials (ONLY on first run)
# POSTGRES_USER=myuser POSTGRES_PASSWORD=mypass docker-compose up -d
```

### Seed Data (Optional)

Populate database with sample records:

```bash
# Run with default credentials (default: seashell_user/seashell_password)
python utils/seed_data.py

# Run with custom credentials (MUST match docker-compose credentials above)
python utils/seed_data.py --username myuser --password mypass
```

> [!IMPORTANT]
> The seed script credentials **must match** the database credentials used in `docker-compose up`. If you used custom credentials when creating the database, use the same credentials here.

### Manage Container

```bash
# View logs
docker-compose logs -f

# Stop everything
docker-compose down
```

**Access:** http://localhost:8000/docs

### Option 2: Local Development

**Requirements:**
- Python 3.12+
- PostgreSQL database running locally
- `.env` file with required variables

```bash
# 1. Create .env file in project root
cat > .env << EOF
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
LOG_LEVEL=INFO
EOF

# 2. Activate environment
source env/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run server
uvicorn app.main:app --reload
```

**Access:** http://localhost:8000/docs


---

## API Endpoints Summary

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Health check |
| `POST` | `/seashells` | Create seashell |
| `GET` | `/seashells` | List seashells (paginated) |
| `GET` | `/seashells/{id}` | Get single seashell |
| `PUT` | `/seashells/{id}` | Update seashell |
| `DELETE` | `/seashells/{id}` | Delete seashell (soft) |

**All endpoints documented interactively at:** http://localhost:8000/docs

---

## For Backend Developers

See [TECHNICAL.md](TECHNICAL.md) for:
- Architecture details
- Database schema & migrations
- Logging & monitoring
- Docker deployment
- Testing

---

Built for the Seashell Collection Backend Challenge

