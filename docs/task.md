# TASK BREAKDOWN

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

# 1. Purpose

Dokumen ini berisi pembagian task development untuk membangun MVP Rocket Mission Planner.

Tujuan dokumen ini adalah membantu proses implementasi agar pekerjaan lebih terarah, modular, dan mudah dikerjakan secara bertahap.

Dokumen ini mengacu pada:

- PRD.md
- FORMULAS.md
- TECH_SPEC.md
- DATABASE.md
- API_SPEC.md

---

# 2. MVP Development Strategy

MVP dibangun menggunakan pendekatan bertahap:

1. Project foundation
2. Database foundation
3. Core backend API
4. Rocket calculator
5. Mission management
6. Rocket configuration
7. Simulation engine integration
8. Visualization-ready response
9. Frontend dashboard
10. Testing and deployment

Prioritas utama MVP adalah memastikan user dapat:

- Membuat mission
- Mengatur konfigurasi roket
- Menghitung performa dasar roket
- Menjalankan simulasi dasar
- Melihat hasil simulasi
- Menyimpan hasil simulasi

---

# 3. Priority Legend

| Priority | Meaning |
|---|---|
| P0 | Critical for MVP |
| P1 | Important for MVP |
| P2 | Nice to have |
| P3 | Future scope |

---

# 4. Phase 0 - Project Setup

## 4.1 Backend Repository Setup

Priority: P0

Tasks:

- Initialize backend project structure
- Setup Python virtual environment
- Add FastAPI
- Add Uvicorn
- Add Pydantic
- Add SQLAlchemy
- Add Alembic
- Add PostgreSQL driver
- Add Pytest
- Add dotenv/settings management

Deliverables:

- Backend project can run locally
- FastAPI app returns health check response

Acceptance Criteria:

- `uvicorn app.main:app --reload` runs successfully
- `GET /health` returns HTTP 200
- Project has clean folder structure

---

## 4.2 Frontend Repository Setup

Priority: P0

Tasks:

- Initialize React project
- Setup TailwindCSS
- Setup React Query
- Setup routing
- Setup API client wrapper
- Setup base layout

Deliverables:

- Frontend app can run locally
- Basic dashboard shell is available

Acceptance Criteria:

- Frontend runs without error
- App can call backend health endpoint
- Layout has navigation placeholder

---

## 4.3 Docker Development Setup

Priority: P1

Tasks:

- Create Dockerfile for backend
- Create Dockerfile for frontend
- Create docker-compose.yml
- Add PostgreSQL service
- Add environment variables
- Add volume for PostgreSQL data

Deliverables:

- Local development can run using Docker Compose

Acceptance Criteria:

- `docker compose up` starts backend, frontend, and database
- Backend can connect to PostgreSQL

---

# 5. Phase 1 - Database Foundation

## 5.1 Database Connection

Priority: P0

Tasks:

- Create database session module
- Create SQLAlchemy base model
- Create database dependency for FastAPI
- Setup environment-based DATABASE_URL

Deliverables:

- Backend can connect to PostgreSQL

Acceptance Criteria:

- Database connection succeeds on app startup
- Database session can be injected into API routes

---

## 5.2 Alembic Migration Setup

Priority: P0

Tasks:

- Initialize Alembic
- Configure Alembic with SQLAlchemy models
- Create first migration
- Add migration command documentation

Deliverables:

- Migration system is available

Acceptance Criteria:

- `alembic revision --autogenerate` works
- `alembic upgrade head` works

---

## 5.3 Create Core Tables

Priority: P0

Tables:

- missions
- engines
- rockets
- simulation_results
- calculator_results

Tasks:

- Create SQLAlchemy models
- Add UUID primary keys
- Add created_at and updated_at fields
- Add foreign key relationships
- Add JSONB columns where needed
- Add indexes

Deliverables:

- Core MVP schema is available

Acceptance Criteria:

- All tables are created by migration
- Foreign key constraints work
- JSONB fields are supported

---

## 5.4 Seed Data

Priority: P1

Tasks:

- Add sample engines
- Add sample mission
- Add sample rocket configuration
- Add seed script

Deliverables:

- Local development has initial data

Acceptance Criteria:

- Seed script inserts sample data successfully
- Sample data appears in API response

---

# 6. Phase 2 - Backend Core API

## 6.1 Health Check API

Priority: P0

Endpoint:

```http
GET /health
```

Tasks:

- Return app status
- Return app version
- Return environment

Acceptance Criteria:

- Endpoint returns HTTP 200
- Response format is consistent

---

## 6.2 Standard API Response Format

Priority: P0

Tasks:

- Define success response format
- Define error response format
- Add request_id field if possible
- Add timestamp field

Success Example:

```json
{
  "success": true,
  "message": "Request processed successfully",
  "data": {}
}
```

Error Example:

```json
{
  "success": false,
  "message": "Validation error",
  "error": {
    "code": "VALIDATION_ERROR",
    "details": []
  }
}
```

Acceptance Criteria:

- API responses use consistent structure
- Error responses are easy to parse by frontend

---

## 6.3 Global Error Handler

Priority: P0

Tasks:

- Handle validation errors
- Handle business logic errors
- Handle database errors
- Handle simulation errors
- Handle unknown system errors

Acceptance Criteria:

- Validation error returns HTTP 422
- Business error returns HTTP 400
- Not found error returns HTTP 404
- System error returns HTTP 500

---

# 7. Phase 3 - Rocket Calculator Module

## 7.1 Delta-V Calculator

Priority: P0

Endpoint:

```http
POST /api/v1/calculators/delta-v
```

Tasks:

- Create request schema
- Validate ISP > 0
- Validate wet_mass > dry_mass
- Implement Tsiolkovsky rocket equation
- Return Delta-V in m/s
- Add unit information

Acceptance Criteria:

- Valid input returns correct Delta-V
- Invalid mass returns error
- Invalid ISP returns error

---

## 7.2 TWR Calculator

Priority: P0

Endpoint:

```http
POST /api/v1/calculators/twr
```

Tasks:

- Create request schema
- Validate thrust > 0
- Validate mass > 0
- Calculate weight
- Calculate TWR
- Return interpretation

Acceptance Criteria:

- TWR < 1 returns cannot_lift_off interpretation
- TWR = 1 returns hover interpretation
- TWR > 1 returns can_ascend interpretation

---

## 7.3 Payload Fraction Calculator

Priority: P0

Endpoint:

```http
POST /api/v1/calculators/payload-fraction
```

Tasks:

- Create request schema
- Validate payload_mass >= 0
- Validate total_mass > 0
- Validate payload_mass <= total_mass
- Calculate payload fraction
- Return decimal and percentage

Acceptance Criteria:

- Valid input returns decimal and percentage
- Payload greater than total mass returns error

---

## 7.4 Mass Ratio Calculator

Priority: P0

Endpoint:

```http
POST /api/v1/calculators/mass-ratio
```

Tasks:

- Create request schema
- Validate wet_mass > dry_mass
- Calculate wet_mass / dry_mass
- Return dimensionless ratio

Acceptance Criteria:

- Valid input returns correct mass ratio
- Invalid mass relationship returns error

---

## 7.5 Calculator Result Storage

Priority: P1

Tasks:

- Save calculator input into calculator_results
- Save calculator output into calculator_results
- Link result to mission if mission_id exists
- Link result to rocket if rocket_id exists

Acceptance Criteria:

- Calculator result can be stored
- Calculator result can be queried later

---

# 8. Phase 4 - Mission Management Module

## 8.1 Create Mission

Priority: P0

Endpoint:

```http
POST /api/v1/missions
```

Tasks:

- Create mission request schema
- Validate mission name
- Insert mission into database
- Return mission record

Acceptance Criteria:

- User can create mission
- Mission name is required
- Created mission has UUID

---

## 8.2 List Missions

Priority: P0

Endpoint:

```http
GET /api/v1/missions
```

Tasks:

- Return mission list
- Add pagination
- Add sorting by created_at
- Add optional status filter

Acceptance Criteria:

- API returns paginated mission list
- Empty state returns empty array

---

## 8.3 Get Mission Detail

Priority: P0

Endpoint:

```http
GET /api/v1/missions/{mission_id}
```

Tasks:

- Fetch mission by ID
- Include rocket configuration summary
- Include latest simulation result summary

Acceptance Criteria:

- Valid mission ID returns detail
- Invalid mission ID returns HTTP 404

---

## 8.4 Update Mission

Priority: P0

Endpoint:

```http
PUT /api/v1/missions/{mission_id}
```

Tasks:

- Validate mission exists
- Update editable fields
- Update updated_at timestamp

Acceptance Criteria:

- Mission can be updated
- Non-existing mission returns HTTP 404

---

## 8.5 Delete Mission

Priority: P1

Endpoint:

```http
DELETE /api/v1/missions/{mission_id}
```

Tasks:

- Delete mission
- Handle related rocket and simulation records
- Decide hard delete for MVP

Acceptance Criteria:

- Mission can be deleted
- Related records are handled safely

---

# 9. Phase 5 - Engine Module

## 9.1 Create Engine

Priority: P0

Endpoint:

```http
POST /api/v1/engines
```

Tasks:

- Create engine schema
- Validate thrust > 0
- Validate ISP > 0
- Validate burn_time > 0 if provided
- Store engine

Acceptance Criteria:

- Engine can be created
- Invalid numeric values return validation error

---

## 9.2 List Engines

Priority: P0

Endpoint:

```http
GET /api/v1/engines
```

Tasks:

- Return engine list
- Add pagination
- Add search by name

Acceptance Criteria:

- Engine list is available for frontend select input

---

## 9.3 Get Engine Detail

Priority: P1

Endpoint:

```http
GET /api/v1/engines/{engine_id}
```

Tasks:

- Fetch engine by ID
- Return full engine data

Acceptance Criteria:

- Valid engine ID returns detail
- Invalid engine ID returns HTTP 404

---

# 10. Phase 6 - Rocket Configuration Module

## 10.1 Create Rocket Configuration

Priority: P0

Endpoint:

```http
POST /api/v1/rockets
```

Tasks:

- Create rocket schema
- Validate mission exists
- Validate engine exists if engine_id provided
- Validate wet_mass > dry_mass
- Validate payload_mass >= 0
- Store rocket configuration

Acceptance Criteria:

- Rocket configuration can be created
- Invalid mass relationship returns error
- Rocket is linked to mission

---

## 10.2 List Rockets

Priority: P1

Endpoint:

```http
GET /api/v1/rockets
```

Tasks:

- Return rocket list
- Add filter by mission_id
- Add pagination

Acceptance Criteria:

- Rockets can be filtered by mission

---

## 10.3 Get Rocket Detail

Priority: P0

Endpoint:

```http
GET /api/v1/rockets/{rocket_id}
```

Tasks:

- Fetch rocket configuration
- Include engine data
- Include calculated mass ratio if possible

Acceptance Criteria:

- Valid rocket ID returns detail
- Invalid rocket ID returns HTTP 404

---

## 10.4 Update Rocket Configuration

Priority: P1

Endpoint:

```http
PUT /api/v1/rockets/{rocket_id}
```

Tasks:

- Validate rocket exists
- Validate updated values
- Update rocket configuration

Acceptance Criteria:

- Rocket can be updated
- Invalid values are rejected

---

## 10.5 Delete Rocket Configuration

Priority: P2

Endpoint:

```http
DELETE /api/v1/rockets/{rocket_id}
```

Tasks:

- Delete rocket configuration
- Prevent accidental delete if simulation result exists, or allow cascade based on MVP rule

Acceptance Criteria:

- Rocket can be deleted safely

---

# 11. Phase 7 - Simulation Module

## 11.1 Basic RocketPy Integration

Priority: P0

Tasks:

- Install RocketPy
- Create simulation adapter
- Create wrapper function for simulation execution
- Define minimum required inputs
- Handle RocketPy exceptions

Acceptance Criteria:

- Backend can call RocketPy from service layer
- Simulation failure returns controlled error response

---

## 11.2 Run Simulation by Input Payload

Priority: P0

Endpoint:

```http
POST /api/v1/simulations/run
```

Tasks:

- Accept direct simulation input
- Validate rocket parameters
- Validate environment parameters
- Run simulation service
- Return simulation summary
- Return time-series data

Acceptance Criteria:

- Valid payload runs simulation
- Response includes apogee, max_velocity, max_acceleration, and flight_duration
- Response includes chart-ready time-series data

---

## 11.3 Run Simulation by Mission ID

Priority: P0

Endpoint:

```http
POST /api/v1/missions/{mission_id}/simulate
```

Tasks:

- Fetch mission
- Fetch rocket configuration
- Fetch engine data
- Build simulation input
- Run RocketPy simulation
- Store result
- Return simulation result

Acceptance Criteria:

- User can run simulation from saved mission
- Simulation result is stored in database
- Missing rocket configuration returns business error

---

## 11.4 Store Simulation Result

Priority: P0

Tasks:

- Store summary metrics
- Store time_series as JSONB
- Store raw_result as JSONB if available
- Store simulation status
- Store error message if failed

Acceptance Criteria:

- Successful simulation is persisted
- Failed simulation can be tracked

---

## 11.5 List Simulation Results

Priority: P1

Endpoint:

```http
GET /api/v1/simulations
```

Tasks:

- List simulation results
- Filter by mission_id
- Filter by rocket_id
- Sort by created_at

Acceptance Criteria:

- User can see simulation history

---

## 11.6 Get Simulation Result Detail

Priority: P0

Endpoint:

```http
GET /api/v1/simulations/{simulation_id}
```

Tasks:

- Fetch simulation result
- Return summary
- Return chart-ready time series

Acceptance Criteria:

- Simulation detail can be opened from frontend
- Invalid simulation ID returns HTTP 404

---

# 12. Phase 8 - Frontend MVP

## 12.1 Base Layout

Priority: P0

Tasks:

- Create main layout
- Create sidebar/navigation
- Create header
- Create content container
- Create responsive layout

Acceptance Criteria:

- User can navigate between main pages
- Layout works on desktop

---

## 12.2 Mission List Page

Priority: P0

Tasks:

- Fetch missions from API
- Display mission cards/table
- Add create mission button
- Add empty state
- Add loading state
- Add error state

Acceptance Criteria:

- Missions are displayed from backend
- User understands empty state

---

## 12.3 Mission Create/Edit Form

Priority: P0

Tasks:

- Create mission form
- Add validation
- Submit to API
- Show success/error notification

Acceptance Criteria:

- User can create mission from UI
- Invalid input is blocked before submit

---

## 12.4 Mission Detail Page

Priority: P0

Tasks:

- Display mission information
- Display rocket configuration
- Display latest simulation result
- Add simulate button
- Add edit mission button

Acceptance Criteria:

- User can view a mission detail
- User can trigger simulation from mission detail

---

## 12.5 Rocket Configuration Form

Priority: P0

Tasks:

- Create rocket form
- Add wet mass input
- Add dry mass input
- Add payload mass input
- Add engine selector
- Validate mass relationship
- Submit to API

Acceptance Criteria:

- User can create rocket configuration
- Invalid mass values are blocked

---

## 12.6 Engine Management UI

Priority: P1

Tasks:

- Create engine list
- Create engine form
- Add engine selector component

Acceptance Criteria:

- User can select engine while configuring rocket
- User can create basic engine data

---

## 12.7 Calculator Page

Priority: P0

Tasks:

- Create calculator tabs/cards
- Add Delta-V calculator
- Add TWR calculator
- Add Payload Fraction calculator
- Add Mass Ratio calculator
- Display result and interpretation

Acceptance Criteria:

- User can calculate all MVP formulas from UI
- Result units are clear

---

## 12.8 Simulation Result Page

Priority: P0

Tasks:

- Fetch simulation result detail
- Display apogee
- Display max velocity
- Display max acceleration
- Display flight duration
- Display status

Acceptance Criteria:

- User can view simulation output summary

---

## 12.9 Visualization Charts

Priority: P0

Tasks:

- Add Plotly chart component
- Render altitude vs time
- Render velocity vs time
- Render acceleration vs time
- Handle empty chart data

Acceptance Criteria:

- Charts render from backend time-series response
- Chart labels and units are clear

---

# 13. Phase 9 - Testing

## 13.1 Backend Unit Tests

Priority: P0

Tasks:

- Test Delta-V calculation
- Test TWR calculation
- Test payload fraction calculation
- Test mass ratio calculation
- Test validation rules

Acceptance Criteria:

- Formula tests pass
- Edge cases are covered

---

## 13.2 Backend API Tests

Priority: P0

Tasks:

- Test mission CRUD
- Test engine CRUD
- Test rocket configuration CRUD
- Test calculator endpoints
- Test simulation endpoints with mock RocketPy if needed

Acceptance Criteria:

- Critical MVP APIs have tests
- Error responses are tested

---

## 13.3 Database Tests

Priority: P1

Tasks:

- Test model creation
- Test foreign key constraints
- Test JSONB fields
- Test migration execution

Acceptance Criteria:

- Database schema works as expected

---

## 13.4 Frontend Tests

Priority: P2

Tasks:

- Test critical forms
- Test calculator UI
- Test API loading/error states
- Test chart rendering with mock data

Acceptance Criteria:

- Main user flows are covered

---

## 13.5 Manual QA Checklist

Priority: P0

Checklist:

- Create mission
- Create engine
- Create rocket configuration
- Run Delta-V calculator
- Run TWR calculator
- Run simulation
- View simulation result
- View charts
- Refresh page and confirm data persists

Acceptance Criteria:

- All main MVP flows pass manual QA

---

# 14. Phase 10 - Logging and Observability

## 14.1 Application Logging

Priority: P1

Tasks:

- Configure structured logging
- Log API errors
- Log simulation start and finish
- Log simulation failure reason

Acceptance Criteria:

- Logs are available in local development
- Errors are traceable

---

## 14.2 Simulation Logging

Priority: P1

Tasks:

- Log simulation input summary
- Log simulation duration
- Log simulation output summary
- Avoid logging excessive raw data

Acceptance Criteria:

- Simulation issues can be debugged safely

---

# 15. Phase 11 - Deployment

## 15.1 Production Environment Variables

Priority: P0

Tasks:

- Define `.env.example`
- Define production env variables
- Validate required env variables on startup

Acceptance Criteria:

- Missing critical env variable blocks app startup
- `.env.example` is documented

---

## 15.2 Backend Deployment

Priority: P0

Tasks:

- Build backend Docker image
- Configure Uvicorn/Gunicorn if needed
- Configure database connection
- Run migration on deploy

Acceptance Criteria:

- Backend can run in production environment
- API docs are accessible if enabled

---

## 15.3 Frontend Deployment

Priority: P0

Tasks:

- Build frontend assets
- Configure API base URL
- Serve frontend via Nginx or static hosting

Acceptance Criteria:

- Frontend can call production backend

---

## 15.4 Database Backup

Priority: P1

Tasks:

- Create pg_dump command
- Document restore command
- Create backup folder convention

Acceptance Criteria:

- Database backup and restore steps are documented

---

# 16. Recommended Implementation Order

## Week 1 - Foundation

Tasks:

- Backend setup
- Frontend setup
- Docker Compose
- PostgreSQL connection
- Alembic setup
- Health check API

Deliverable:

- App skeleton running locally

---

## Week 2 - Database and Calculator

Tasks:

- Create core database tables
- Create calculator services
- Create calculator endpoints
- Add calculator tests
- Create calculator UI

Deliverable:

- Rocket calculator working end-to-end

---

## Week 3 - Mission and Engine Management

Tasks:

- Mission CRUD API
- Engine CRUD API
- Mission list UI
- Mission form UI
- Engine selector UI

Deliverable:

- User can manage missions and engines

---

## Week 4 - Rocket Configuration

Tasks:

- Rocket CRUD API
- Rocket validation
- Rocket configuration UI
- Mission detail integration

Deliverable:

- User can attach rocket configuration to mission

---

## Week 5 - Simulation Integration

Tasks:

- RocketPy adapter
- Simulation service
- Run simulation endpoint
- Store simulation result
- Simulation error handling

Deliverable:

- User can run simulation from backend

---

## Week 6 - Visualization

Tasks:

- Simulation result API
- Chart-ready time-series response
- Plotly chart components
- Simulation result page

Deliverable:

- User can view simulation summary and charts

---

## Week 7 - QA and Stabilization

Tasks:

- Backend API tests
- Manual QA
- Fix validation gaps
- Improve error messages
- Improve loading states

Deliverable:

- MVP feature-complete and testable

---

## Week 8 - Deployment Preparation

Tasks:

- Production Docker setup
- Nginx config
- Env documentation
- Database backup documentation
- Deployment checklist

Deliverable:

- MVP ready for deployment

---

# 17. MVP Completion Checklist

MVP is considered complete when:

- Backend app runs successfully
- Frontend app runs successfully
- PostgreSQL is connected
- Alembic migrations work
- User can create a mission
- User can create an engine
- User can create rocket configuration
- User can calculate Delta-V
- User can calculate TWR
- User can calculate payload fraction
- User can calculate mass ratio
- User can run RocketPy simulation
- User can view apogee
- User can view max velocity
- User can view max acceleration
- User can view flight duration
- User can view altitude chart
- User can view velocity chart
- User can view acceleration chart
- Simulation result is stored
- Basic error handling works
- Manual QA checklist passes

---

# 18. Codex Prompt Recommendation

Use this prompt when starting implementation:

```text
You are working on Rocket Mission Planner MVP.
Read and follow these documents:

- PRD.md
- FORMULAS.md
- TECH_SPEC.md
- DATABASE.md
- API_SPEC.md
- TASK_BREAKDOWN.md

Implement the project incrementally using the task breakdown.
Start from Phase 0 and Phase 1.
Do not skip database migration, validation, error handling, and tests.
Keep the architecture modular monolith using FastAPI service layers.
```

---

# 19. Out of Scope for MVP

The following tasks must not be implemented in MVP unless explicitly approved:

- User authentication
- Role-based access control
- Multi-user collaboration
- Real-time weather integration
- Multi-stage rocket simulation
- Orbital mechanics
- Satellite deployment
- Moon mission planner
- Mars mission planner
- CFD simulation
- Payment system
- Public marketplace

---

# 20. Notes

This task breakdown intentionally prioritizes a stable MVP over advanced aerospace features.

The first version should prove the product flow:

```text
Mission -> Rocket Configuration -> Calculation -> Simulation -> Visualization -> Storage
```

After this flow is stable, future versions can expand into multi-stage rockets, orbit simulation, and interplanetary mission planning.
