# TECHNICAL SPECIFICATION (TECH_SPEC)

## Project Name

Rocket Mission Planner

## Version

1.0 (MVP)

## Status

Draft

## Document Owner

Gunawan WP

## Last Updated

June 2026

---

# 1. Overview

Rocket Mission Planner adalah aplikasi web berbasis FastAPI yang digunakan untuk menghitung performa roket, menjalankan simulasi menggunakan RocketPy, menyimpan konfigurasi misi, dan menampilkan hasil simulasi dalam bentuk visualisasi.

Sistem menggunakan pendekatan **API-First Architecture** sehingga frontend web, mobile app, CLI tool, atau integrasi pihak ketiga dapat menggunakan API yang sama.

MVP berfokus pada:

- Rocket calculator
- Mission management
- Rocket configuration
- RocketPy simulation integration
- Simulation result storage
- Visualization-ready API response

MVP tidak berfokus pada authentication, multi-user collaboration, orbital transfer, atau interplanetary mission planning.

---

# 2. Architecture Principles

## 2.1 API-First

Semua fitur utama harus tersedia melalui REST API sebelum dikonsumsi oleh frontend.

Tujuan:

- Frontend tidak bergantung pada logic lokal.
- Mobile app atau CLI dapat dibuat di masa depan.
- Testing backend lebih mudah dilakukan.

## 2.2 Modular Monolith

Untuk MVP, sistem menggunakan pendekatan **modular monolith**.

Artinya:

- Satu backend FastAPI application.
- Module dipisahkan berdasarkan domain.
- Setiap module memiliki router, schema, model, dan service sendiri.
- Belum menggunakan microservices.

Alasan:

- Lebih sederhana untuk MVP.
- Deployment lebih mudah.
- Debugging lebih cepat.
- Masih bisa dikembangkan menjadi service terpisah di masa depan.

## 2.3 Service Layer Separation

Business logic tidak boleh ditulis langsung di router.

Router hanya bertugas untuk:

- Menerima request
- Melakukan dependency injection
- Memanggil service
- Mengembalikan response

Service bertugas untuk:

- Menjalankan business logic
- Melakukan kalkulasi
- Mengakses repository/database
- Menjalankan RocketPy simulation

---

# 3. High Level Architecture

```text
Client Layer
│
├── React Frontend
├── Future Mobile App
└── Future CLI Client

↓

API Layer
│
└── FastAPI REST API

↓

Business Layer
│
├── Mission Service
├── Rocket Service
├── Calculator Service
└── Simulation Service

↓

Simulation Engine
│
└── RocketPy

↓

Persistence Layer
│
└── PostgreSQL

↓

Infrastructure Layer
│
├── Docker
├── Nginx
└── Linux VPS
```

---

# 4. Technology Stack

## 4.1 Backend

| Component | Technology |
|---|---|
| Language | Python 3.12+ |
| Framework | FastAPI |
| ASGI Server | Uvicorn |
| Validation | Pydantic |
| ORM | SQLAlchemy |
| Migration | Alembic |
| Testing | Pytest |
| HTTP Client Testing | HTTPX |
| Environment Config | Pydantic Settings |

## 4.2 Simulation Engine

| Component | Technology |
|---|---|
| Simulation Library | RocketPy |
| Numerical Computing | NumPy |
| Scientific Computing | SciPy |
| Data Processing | Pandas |

Purpose:

- Flight simulation
- Apogee calculation
- Velocity profile
- Acceleration profile
- Flight duration estimation

## 4.3 Database

| Component | Technology |
|---|---|
| Database Engine | PostgreSQL 16+ |
| Migration Tool | Alembic |
| Connection Driver | psycopg / asyncpg |

Purpose:

- Mission storage
- Rocket configuration storage
- Simulation result history
- Calculation result storage

## 4.4 Frontend

| Component | Technology |
|---|---|
| Framework | React |
| Styling | TailwindCSS |
| Charts | Plotly |
| Data Fetching | React Query |
| Form Handling | React Hook Form |
| Validation | Zod |

## 4.5 Infrastructure

| Component | Technology |
|---|---|
| Containerization | Docker |
| Reverse Proxy | Nginx |
| OS | Linux VPS |
| Process Runtime | Docker Compose |
| Logs | File logs + container logs |

---

# 5. System Modules

## 5.1 Mission Management Module

Responsibilities:

- Create mission
- Update mission
- Delete mission
- View mission detail
- List missions
- Attach rocket configuration to mission
- Attach simulation result to mission

Main Entities:

- Mission
- MissionStatus

Output:

- Mission record
- Mission list
- Mission detail with related rocket and simulation result

---

## 5.2 Rocket Configuration Module

Responsibilities:

- Configure rocket
- Configure payload
- Configure engine
- Validate mass data
- Validate engine data

Main Entities:

- RocketConfiguration
- EngineConfiguration
- PayloadConfiguration

Output:

- Rocket configuration record
- Validated configuration object for calculation and simulation

---

## 5.3 Rocket Calculator Module

Responsibilities:

- Calculate Delta-V
- Calculate TWR
- Calculate payload fraction
- Calculate mass ratio
- Calculate propellant mass
- Calculate burn time
- Calculate mass flow rate
- Calculate initial acceleration

Output:

- Calculation result
- Unit metadata
- Interpretation text
- Validation errors when input is invalid

---

## 5.4 Simulation Engine Module

Responsibilities:

- Convert mission and rocket configuration into RocketPy input
- Generate simulation environment
- Run flight simulation
- Capture result
- Normalize output into API-friendly JSON
- Store simulation result

Output:

- Apogee
- Max velocity
- Max acceleration
- Flight duration
- Altitude time-series
- Velocity time-series
- Acceleration time-series

---

## 5.5 Visualization Module

Responsibilities:

- Provide chart-ready data to frontend
- Format time-series response
- Support altitude, velocity, and acceleration graphs

Output:

- Plotly-compatible data structure
- Simulation chart payload

Note:

Visualization rendering dilakukan di frontend. Backend hanya menyediakan data.

---

# 6. Backend Folder Structure

Recommended structure:

```text
app/
│
├── main.py
├── api/
│   └── v1/
│       ├── routers/
│       │   ├── mission_router.py
│       │   ├── rocket_router.py
│       │   ├── calculator_router.py
│       │   └── simulation_router.py
│       │
│       └── api.py
│
├── core/
│   ├── config.py
│   ├── constants.py
│   ├── exceptions.py
│   └── logging.py
│
├── database/
│   ├── session.py
│   ├── base.py
│   └── init_db.py
│
├── models/
│   ├── mission_model.py
│   ├── rocket_model.py
│   ├── engine_model.py
│   └── simulation_model.py
│
├── schemas/
│   ├── mission_schema.py
│   ├── rocket_schema.py
│   ├── calculator_schema.py
│   └── simulation_schema.py
│
├── services/
│   ├── mission_service.py
│   ├── rocket_service.py
│   ├── calculator_service.py
│   └── simulation_service.py
│
├── repositories/
│   ├── mission_repository.py
│   ├── rocket_repository.py
│   └── simulation_repository.py
│
├── simulation/
│   ├── rocketpy_adapter.py
│   ├── environment_builder.py
│   ├── rocket_builder.py
│   └── result_parser.py
│
├── utils/
│   ├── math_utils.py
│   └── unit_converter.py
│
└── tests/
    ├── unit/
    ├── integration/
    └── fixtures/
```

---

# 7. Request Flow

```text
Client Request
↓
API Router
↓
Pydantic Schema Validation
↓
Service Layer
↓
Repository / RocketPy Adapter
↓
Database / Simulation Engine
↓
Response Schema
↓
Client Response
```

Example:

```text
POST /api/v1/calculators/delta-v
↓
Validate input using DeltaVRequest schema
↓
Call CalculatorService.calculate_delta_v()
↓
Return DeltaVResponse
```

---

# 8. Simulation Flow

```text
User Input
│
├── Payload Mass
├── Wet Mass
├── Dry Mass
├── Engine Data
├── Drag Data
└── Environment Data

↓

Mission Service
↓
Rocket Configuration Validation
↓
Simulation Service
↓
RocketPy Adapter
↓
RocketPy Flight Simulation
↓
Result Parser
↓
Store Simulation Result
↓
Return API Response
```

Simulation must be deterministic when the same input is used.

---

# 9. API Specification Draft

Base URL:

```text
/api/v1
```

## 9.1 Health Check

### GET `/health`

Purpose:

Check API health status.

Response:

```json
{
  "status": "ok",
  "service": "Rocket Mission Planner API",
  "version": "1.0.0"
}
```

---

## 9.2 Mission API

### GET `/missions`

Purpose:

Get all missions.

Response:

```json
{
  "data": [
    {
      "id": "uuid",
      "name": "Test Mission 1",
      "description": "Single stage test rocket",
      "status": "draft",
      "created_at": "2026-06-01T10:00:00Z"
    }
  ]
}
```

### POST `/missions`

Purpose:

Create new mission.

Request:

```json
{
  "name": "Test Mission 1",
  "description": "Single stage rocket simulation"
}
```

### GET `/missions/{mission_id}`

Purpose:

Get mission detail.

### PATCH `/missions/{mission_id}`

Purpose:

Update mission.

### DELETE `/missions/{mission_id}`

Purpose:

Delete mission.

---

## 9.3 Rocket Configuration API

### POST `/missions/{mission_id}/rocket-configurations`

Purpose:

Create rocket configuration for a mission.

Request:

```json
{
  "rocket_name": "Single Stage Demo Rocket",
  "wet_mass_kg": 50,
  "dry_mass_kg": 20,
  "payload_mass_kg": 5,
  "engine": {
    "name": "Demo Engine",
    "thrust_n": 1500,
    "specific_impulse_s": 220,
    "burn_time_s": 3.5
  }
}
```

Response:

```json
{
  "data": {
    "id": "uuid",
    "mission_id": "uuid",
    "rocket_name": "Single Stage Demo Rocket",
    "wet_mass_kg": 50,
    "dry_mass_kg": 20,
    "payload_mass_kg": 5,
    "engine": {
      "name": "Demo Engine",
      "thrust_n": 1500,
      "specific_impulse_s": 220,
      "burn_time_s": 3.5
    }
  }
}
```

### GET `/missions/{mission_id}/rocket-configurations`

Purpose:

Get rocket configurations for a mission.

---

## 9.4 Calculator API

### POST `/calculators/delta-v`

Request:

```json
{
  "specific_impulse_s": 220,
  "wet_mass_kg": 50,
  "dry_mass_kg": 20
}
```

Response:

```json
{
  "data": {
    "value": 1975.51,
    "unit": "m/s",
    "formula": "delta_v = isp * g0 * ln(wet_mass / dry_mass)",
    "interpretation": "Estimated ideal Delta-V before atmospheric and drag losses."
  }
}
```

### POST `/calculators/twr`

Request:

```json
{
  "thrust_n": 1500,
  "mass_kg": 50
}
```

Response:

```json
{
  "data": {
    "value": 3.06,
    "unit": "ratio",
    "formula": "twr = thrust / (mass * g0)",
    "interpretation": "Rocket can ascend because TWR is greater than 1."
  }
}
```

### POST `/calculators/payload-fraction`

Purpose:

Calculate payload fraction.

### POST `/calculators/mass-ratio`

Purpose:

Calculate wet mass to dry mass ratio.

---

## 9.5 Simulation API

### POST `/missions/{mission_id}/simulations`

Purpose:

Run simulation for a mission.

Request:

```json
{
  "rocket_configuration_id": "uuid",
  "environment": {
    "latitude": 0,
    "longitude": 0,
    "elevation_m": 0,
    "date": "2026-06-01"
  }
}
```

Response:

```json
{
  "data": {
    "id": "uuid",
    "mission_id": "uuid",
    "rocket_configuration_id": "uuid",
    "status": "completed",
    "summary": {
      "apogee_m": 1200.5,
      "max_velocity_mps": 320.2,
      "max_acceleration_mps2": 45.8,
      "flight_duration_s": 62.4
    },
    "series": {
      "altitude": [
        { "time_s": 0, "value_m": 0 },
        { "time_s": 1, "value_m": 42 }
      ],
      "velocity": [
        { "time_s": 0, "value_mps": 0 },
        { "time_s": 1, "value_mps": 80 }
      ],
      "acceleration": [
        { "time_s": 0, "value_mps2": 0 },
        { "time_s": 1, "value_mps2": 32 }
      ]
    }
  }
}
```

### GET `/missions/{mission_id}/simulations`

Purpose:

Get simulation history for a mission.

### GET `/simulations/{simulation_id}`

Purpose:

Get simulation detail.

---

# 10. Database Design Draft

## 10.1 missions

| Column | Type | Notes |
|---|---|---|
| id | UUID | Primary key |
| name | VARCHAR(255) | Required |
| description | TEXT | Nullable |
| status | VARCHAR(50) | draft, simulated, archived |
| created_at | TIMESTAMP | Required |
| updated_at | TIMESTAMP | Required |

## 10.2 rocket_configurations

| Column | Type | Notes |
|---|---|---|
| id | UUID | Primary key |
| mission_id | UUID | Foreign key to missions.id |
| rocket_name | VARCHAR(255) | Required |
| wet_mass_kg | NUMERIC | Required, must be > 0 |
| dry_mass_kg | NUMERIC | Required, must be > 0 |
| payload_mass_kg | NUMERIC | Required, must be >= 0 |
| created_at | TIMESTAMP | Required |
| updated_at | TIMESTAMP | Required |

## 10.3 engine_configurations

| Column | Type | Notes |
|---|---|---|
| id | UUID | Primary key |
| rocket_configuration_id | UUID | Foreign key to rocket_configurations.id |
| name | VARCHAR(255) | Required |
| thrust_n | NUMERIC | Required, must be > 0 |
| specific_impulse_s | NUMERIC | Required, must be > 0 |
| burn_time_s | NUMERIC | Required, must be > 0 |
| created_at | TIMESTAMP | Required |
| updated_at | TIMESTAMP | Required |

## 10.4 simulation_results

| Column | Type | Notes |
|---|---|---|
| id | UUID | Primary key |
| mission_id | UUID | Foreign key to missions.id |
| rocket_configuration_id | UUID | Foreign key to rocket_configurations.id |
| status | VARCHAR(50) | pending, running, completed, failed |
| apogee_m | NUMERIC | Nullable until completed |
| max_velocity_mps | NUMERIC | Nullable until completed |
| max_acceleration_mps2 | NUMERIC | Nullable until completed |
| flight_duration_s | NUMERIC | Nullable until completed |
| error_message | TEXT | Nullable |
| created_at | TIMESTAMP | Required |
| updated_at | TIMESTAMP | Required |

## 10.5 simulation_series

| Column | Type | Notes |
|---|---|---|
| id | UUID | Primary key |
| simulation_result_id | UUID | Foreign key to simulation_results.id |
| series_type | VARCHAR(50) | altitude, velocity, acceleration |
| time_s | NUMERIC | Required |
| value | NUMERIC | Required |
| unit | VARCHAR(50) | m, m/s, m/s² |

Alternative for MVP:

`simulation_series` can be stored as JSONB inside `simulation_results` to reduce table complexity.

Recommended MVP approach:

- Store summary fields as columns.
- Store time-series as JSONB.

---

# 11. Data Validation Rules

## 11.1 General Rules

- All mass values must be non-negative.
- Wet mass must be greater than dry mass.
- Dry mass must be greater than or equal to payload mass.
- Thrust must be greater than zero.
- Specific impulse must be greater than zero.
- Burn time must be greater than zero.
- Latitude must be between -90 and 90.
- Longitude must be between -180 and 180.

## 11.2 Calculator Validation

Delta-V:

- `specific_impulse_s > 0`
- `wet_mass_kg > 0`
- `dry_mass_kg > 0`
- `wet_mass_kg > dry_mass_kg`

TWR:

- `thrust_n > 0`
- `mass_kg > 0`

Payload Fraction:

- `payload_mass_kg >= 0`
- `total_mass_kg > 0`
- `payload_mass_kg <= total_mass_kg`

Mass Ratio:

- `wet_mass_kg > 0`
- `dry_mass_kg > 0`
- `wet_mass_kg >= dry_mass_kg`

---

# 12. Error Handling

## 12.1 Error Response Format

All error responses should use a consistent format.

```json
{
  "error": {
    "code": "INVALID_MASS_VALUE",
    "message": "Wet mass must be greater than dry mass.",
    "details": {
      "wet_mass_kg": 20,
      "dry_mass_kg": 50
    }
  }
}
```

## 12.2 Error Types

| Error Type | HTTP Status | Example |
|---|---:|---|
| Validation Error | 422 | Negative mass, invalid type |
| Business Error | 400 | Dry mass greater than wet mass |
| Not Found Error | 404 | Mission not found |
| Conflict Error | 409 | Simulation already running |
| System Error | 500 | Database failure, simulation crash |

## 12.3 Error Code Examples

- `MISSION_NOT_FOUND`
- `ROCKET_CONFIGURATION_NOT_FOUND`
- `SIMULATION_NOT_FOUND`
- `INVALID_MASS_VALUE`
- `INVALID_ENGINE_VALUE`
- `INVALID_ENVIRONMENT_VALUE`
- `SIMULATION_FAILED`
- `DATABASE_ERROR`

---

# 13. Security

## 13.1 MVP Security

MVP does not include authentication and authorization.

Security requirements for MVP:

- Validate all user inputs.
- Reject negative or impossible physical values.
- Use environment variables for secrets.
- Do not expose stack traces in production.
- Enable CORS only for allowed frontend domains.
- Use HTTPS in production.

## 13.2 Future Security

Future versions may include:

- JWT authentication
- User accounts
- Role-based access control
- API rate limiting
- Request audit logging
- Private mission storage

---

# 14. Logging

## 14.1 Log Types

| Log Type | Purpose |
|---|---|
| Application Log | API activity and service flow |
| Simulation Log | RocketPy execution and result summary |
| Error Log | Exceptions and failed requests |
| Access Log | HTTP request metadata |

## 14.2 Log Location

For local development:

```text
logs/
├── app.log
├── simulation.log
└── error.log
```

For production:

- Container stdout/stderr
- Optional file-based log volume

## 14.3 Required Log Fields

- timestamp
- level
- request_id
- module
- message
- error_code
- duration_ms

Example:

```json
{
  "timestamp": "2026-06-01T10:00:00Z",
  "level": "INFO",
  "request_id": "req_123",
  "module": "simulation_service",
  "message": "Simulation completed",
  "duration_ms": 8420
}
```

---

# 15. Environment Variables

| Variable | Required | Example | Description |
|---|---|---|---|
| APP_NAME | Yes | Rocket Mission Planner | Application name |
| APP_ENV | Yes | development | development, staging, production |
| APP_DEBUG | Yes | true | Enable debug mode |
| API_PREFIX | Yes | /api/v1 | API base prefix |
| DATABASE_URL | Yes | postgresql://user:pass@db:5432/rocket | Database connection |
| SECRET_KEY | Yes | change-me | Secret key for future auth/session use |
| LOG_LEVEL | Yes | INFO | Logging level |
| CORS_ORIGINS | Yes | http://localhost:5173 | Allowed origins |
| SIMULATION_TIMEOUT_SECONDS | Yes | 10 | Simulation timeout |

---

# 16. Performance Targets

| Component | Target |
|---|---:|
| Health check response | < 100 ms |
| Calculator response | < 100 ms |
| Mission list response | < 500 ms |
| Mission detail response | < 500 ms |
| Database query | < 300 ms |
| Basic RocketPy simulation | < 10 seconds |
| Frontend dashboard load | < 3 seconds |

Notes:

- Simulation may exceed target for complex configuration.
- MVP should enforce timeout to avoid long-running requests blocking API workers.
- Heavy simulations can be moved to background jobs in future versions.

---

# 17. Testing Strategy

## 17.1 Unit Tests

Required unit tests:

- Delta-V calculation
- TWR calculation
- Payload fraction calculation
- Mass ratio calculation
- Input validation
- Error handling

## 17.2 Integration Tests

Required integration tests:

- Create mission
- Update mission
- Delete mission
- Create rocket configuration
- Run calculator endpoint
- Run simulation endpoint with fixture data
- Store simulation result

## 17.3 Simulation Tests

Required simulation tests:

- RocketPy adapter receives valid input
- Simulation returns expected output keys
- Failed simulation returns controlled error
- Timeout is handled correctly

## 17.4 API Tests

Required API tests:

- `GET /health`
- `GET /missions`
- `POST /missions`
- `POST /calculators/delta-v`
- `POST /calculators/twr`
- `POST /missions/{mission_id}/simulations`

---

# 18. Deployment Architecture

```text
Internet
↓
Nginx
↓
FastAPI Container
↓
RocketPy Runtime
↓
PostgreSQL Container / Managed Database
↓
Persistent Storage
```

Recommended MVP deployment:

- 1 Linux VPS
- Docker Compose
- Nginx reverse proxy
- FastAPI backend container
- PostgreSQL container or managed PostgreSQL
- Frontend served via Nginx or separate static hosting

---

# 19. Docker Compose Services

Recommended services:

```text
services:
  backend:
    FastAPI + Uvicorn

  postgres:
    PostgreSQL database

  nginx:
    Reverse proxy

  frontend:
    React build output, optional for MVP
```

Future services:

```text
  redis:
    Queue broker and cache

  worker:
    Background simulation worker
```

---

# 20. Background Job Consideration

For MVP, simulation can run synchronously if it completes under 10 seconds.

Future architecture should use background workers when:

- Simulation exceeds 10 seconds.
- Multiple users run simulations concurrently.
- Simulation complexity increases.
- Orbit or multi-stage simulation is introduced.

Recommended future stack:

- Redis
- Celery / Dramatiq / RQ
- Worker container
- Simulation status polling endpoint

---

# 21. Acceptance Criteria

MVP technical implementation is considered successful when:

- API can start using FastAPI and Uvicorn.
- Database migration can be executed using Alembic.
- User can create, update, delete, and view missions.
- User can create rocket configuration for a mission.
- Calculator endpoints return correct results.
- Invalid physical values return controlled errors.
- Simulation endpoint can run basic RocketPy simulation.
- Simulation result is stored in PostgreSQL.
- Simulation result can be returned as JSON.
- Frontend can render altitude, velocity, and acceleration charts from API response.
- All required unit tests pass.
- All required integration tests pass.

---

# 22. Risks and Mitigations

## 22.1 Technical Risks

| Risk | Impact | Mitigation |
|---|---|---|
| RocketPy integration is more complex than expected | Simulation delayed | Build RocketPy adapter early |
| Simulation too slow | Poor user experience | Add timeout and future background worker |
| Invalid physical input causes crash | API instability | Strict Pydantic validation |
| Time-series data too large | Slow database and API response | Limit sample size or store JSONB |
| Formula mismatch | Incorrect result | Add formula tests and reference examples |

## 22.2 Product Risks

| Risk | Impact | Mitigation |
|---|---|---|
| Scope too large | MVP delayed | Keep orbital and multi-stage out of MVP |
| Aerospace complexity too high | User confusion | Add interpretation text and documentation |
| Lack of validation data | Lower confidence | Start with educational simulation positioning |

---

# 23. Future Architecture

## V2

- Authentication
- User accounts
- Mission sharing
- Engine library
- Rocket templates
- Background simulation worker

## V3

- Multi-stage rocket
- Orbit simulation
- Satellite deployment
- Transfer orbit analysis

## V4

- Moon mission planner
- Mars mission planner
- Interplanetary mission planner
- Advanced mission timeline planning

---

# 24. Development Notes

Recommended implementation order:

1. Project setup
2. Database setup
3. Mission CRUD
4. Rocket configuration CRUD
5. Calculator service
6. Calculator API endpoints
7. RocketPy adapter prototype
8. Simulation service
9. Simulation result storage
10. Chart-ready API response
11. Frontend dashboard integration
12. Testing and deployment

Recommended first backend milestone:

- FastAPI project boots successfully.
- PostgreSQL connection works.
- Alembic migration works.
- `GET /health` works.
- `POST /calculators/delta-v` works.

---

# 25. Summary

Rocket Mission Planner MVP should be built as a modular monolith using FastAPI, PostgreSQL, and RocketPy.

The most important technical decisions are:

- Keep the MVP simple.
- Separate router, service, repository, and simulation adapter.
- Validate physical input strictly.
- Store simulation summaries in database columns.
- Store time-series data as JSONB for MVP simplicity.
- Return frontend-ready visualization data.
- Move heavy simulations to background workers only in future versions.
