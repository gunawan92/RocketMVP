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
- Full `rocketpy.Flight` is not wired yet because the MVP input does not yet include complete RocketPy motor curve and geometry fields.
- Trajectory output currently uses an analytical placeholder inside the RocketPy adapter boundary.
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

1. Expand RocketPy adapter to full `RocketPy Flight` once motor curve and geometry inputs are modeled.
2. Start frontend MVP against the stable backend API.

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
