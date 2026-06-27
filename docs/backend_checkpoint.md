# Backend Checkpoint

Last updated: 2026-06-27

## Current Status

The project is still backend-only. Frontend work has not started.

Completed backend foundation:

- FastAPI app with `/api/v1` prefix.
- Standard success and error response format.
- Global exception handlers.
- Neon PostgreSQL connection through `DATABASE_URL`.
- SQLAlchemy base/session and Alembic migration setup.
- Initial migration applied for core MVP tables.

Core tables:

- `missions`
- `engines`
- `rockets`
- `calculator_results`
- `simulation_results`

Implemented API modules:

- Health check and database health check.
- Mission CRUD.
- Engine CRUD.
- Rocket configuration CRUD.
- Engine motor curve storage.
- Rocket geometry storage.
- Calculator endpoints for Delta-V, TWR, payload fraction, and mass ratio.
- Optional calculator result storage in `calculator_results`.
- Simulation result API with storage.
- Simulation comparison API.
- Dashboard summary API.
- Formal pytest suite for the backend MVP flow.

## Simulation Status

Simulation endpoint:

```text
POST /api/v1/simulations/run
GET  /api/v1/missions/{mission_id}/simulations
GET  /api/v1/simulations/{simulation_id}
DELETE /api/v1/simulations/{simulation_id}
```

Current simulation engine state:

- `RocketPyAdapter` initializes a real `rocketpy.Environment`.
- Engine input now supports `motor_curve` points for thrust-vs-time data.
- Rocket input now supports geometry fields for nose cone, fins, center of mass, motor position, diameter, length, and drag coefficient.
- Trajectory output currently uses an analytical placeholder inside the RocketPy adapter boundary, but it now derives burn time, average thrust, max thrust, and total impulse from `motor_curve` when provided.
- API response and database storage contract are stable, so replacing the placeholder with full RocketPy Flight later should not affect frontend contracts.

Stored simulation output includes:

- `apogee`
- `max_velocity`
- `max_acceleration`
- `flight_duration`
- `summary`
- `time_series`
- `raw_result`

## Manual Backend E2E Flow

Expected working flow:

```text
create mission
-> create engine
-> create rocket
-> run simulation
-> list simulation results by mission
-> get simulation detail
-> delete simulation result
```

## Verified Smoke Tests

Validated against Neon PostgreSQL:

- Mission CRUD.
- Engine CRUD.
- Rocket CRUD.
- Simulation run, list, detail, and delete.
- Invalid UUID returns `422 VALIDATION_ERROR`.
- Missing resources return `404 RESOURCE_NOT_FOUND`.
- Business rule violations return `400 BUSINESS_RULE_ERROR`.

## Next Backend Steps

Recommended next work:

1. Expand RocketPy adapter from analytical placeholder to full `RocketPy Flight` using the stored motor curve and geometry fields.
2. Start frontend MVP against the stable backend API.

## PRD V2 Gap Notes

These items are not blockers for the current backend MVP, but should be tracked before claiming PRD V2 completeness.

| PRD V2 Area | Status | Notes |
|---|---|---|
| Rocket Sandbox | Not started | Needs free experiment mode outside mission CRUD flow. |
| Mission Challenge | Partial | Mission CRUD exists, but target, reward, and level data are not modeled yet. |
| Classroom Mode | Not started | Future scope, not required for initial MVP. |
| Adjustable Parameters game version | Partial | Geometry exists, but not simplified into student-facing controls like height, diameter, fin size, nose cone, and payload preset. |
| Engine A/B/C/D | Not started | Current engine model is technical; student-facing preset engines are not modeled yet. |
| Fuel System single/two/three stage | Not started | Multi-stage rocket and fuel stage model are not implemented yet. |
| Weather System | Not started | Needs weather presets such as clear, cloudy, windy, and storm. |
| Failure Engine | Not started | Important for educational outcomes and failure explanation. |
| Scoring System | Not started | Needs score calculation and star rating. |
| Learning feedback | Not started | Needs educational feedback messages after simulation. |
| Result screen data | Partial | Numeric result data exists, but mission/game result status is not modeled yet. |
| Real RocketPy Flight | Not fully complete | Current simulation still uses analytical placeholder inside RocketPy adapter boundary. |

## Test Suite

Run backend tests:

```powershell
.\venv\Scripts\pytest.exe
```

The tests use an in-memory SQLite database through FastAPI dependency override, so they do not mutate the Neon database.

## Frontend Status

Frontend is not started yet.

Recommended frontend start point after backend API stabilizes:

```text
Mission list -> Mission detail -> Engine form -> Rocket form -> Run simulation -> Simulation result charts
```
