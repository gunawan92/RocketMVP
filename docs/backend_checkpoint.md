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
- PRD V2 game/education API layer for challenge presets, engine presets, weather presets, sandbox run, scoring, failure reason, and learning feedback.

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
| Rocket Sandbox | Initial backend done | `POST /api/v1/game/sandbox/run` runs stateless educational sandbox simulation. |
| Mission Challenge | Initial backend done | `GET /api/v1/game/challenges` provides target, reward, and level presets. |
| Classroom Mode | Not started | Future scope, not required for initial MVP. |
| Adjustable Parameters game version | Initial backend done | Sandbox request supports height, diameter, fin size, nose cone, payload, engine, stages, and weather. |
| Engine A/B/C/D | Initial backend done | `GET /api/v1/game/engine-presets` returns student-facing engine presets. |
| Fuel System single/two/three stage | Initial backend done | Sandbox request supports `single`, `two`, and `three` stages in scoring/trajectory approximation. |
| Weather System | Initial backend done | `GET /api/v1/game/weather-presets` returns clear, cloudy, windy, and storm presets. |
| Failure Engine | Initial backend done | Sandbox run returns failure codes such as heavy rocket, unstable flight, strong wind, structural failure, and payload failure. |
| Scoring System | Initial backend done | Sandbox run returns score, stars, and weighted score breakdown. |
| Learning feedback | Initial backend done | Sandbox run returns educational feedback title, message, and suggestions. |
| Result screen data | Initial backend done | Sandbox run returns mission status, score, stars, failures, summary, and selected configuration. |
| Real RocketPy Flight | Not fully complete | Current simulation still uses analytical placeholder inside RocketPy adapter boundary. |

## PRD V2 Game API

Initial stateless endpoints:

```text
GET  /api/v1/game/challenges
GET  /api/v1/game/engine-presets
GET  /api/v1/game/weather-presets
POST /api/v1/game/sandbox/run
```

The game API is intentionally stateless for the first PRD V2 pass. It does not create classroom records or mutate Neon tables yet.

## Test Suite

Run backend tests:

```powershell
.\venv\Scripts\pytest.exe
```

The tests use an in-memory SQLite database through FastAPI dependency override, so they do not mutate the Neon database.

## Frontend Status

Frontend dashboard and first mission flow are available in `C:\xampp\htdocs\sideJob\rocketFe`.

Important frontend integration note:

- The frontend can connect to the real FastAPI backend through `VITE_API_BASE_URL`.
- The frontend still contains a localStorage mock/sandbox fallback through `src/api/mockStore.ts`.
- The sidebar can switch between FastAPI live mode and sandbox mode.
- If the backend is unreachable, the frontend API client can fall back to sandbox mode.
- For real integration testing, make sure sandbox mode is disabled by setting `localStorage.use_demo_backend = "false"` or clearing the browser localStorage.

Current frontend UX checkpoint:

- Engine form now supports visual presets and slider-based numeric controls.
- Rocket form now supports visual presets and slider-based mass controls.
- Advanced rocket geometry now has summary cards and slider controls for body, nose cone, fins, mass placement, and drag settings.
- Numeric input is still available for precision, but users can start from presets and adjust visually.
- PRD V2 frontend game layer is added as a separate route at `/gameV1`, without replacing the existing dashboard or mission panels.
- `/gameV1` consumes the backend `/api/v1/game/*` endpoints for challenge presets, engine presets, weather presets, sandbox/challenge run, score, stars, failures, and learning feedback.
- `/gameV1` now includes a 2.5D Rocket Launch Simulation Screen with builder summary, launch pad, animated rocket, flame/smoke, wind drift, stage separation cue, live telemetry, mission progress, and result/feedback panel.

Recommended frontend start point after backend API stabilizes:

```text
Mission list -> Mission detail -> Engine form -> Rocket form -> Run simulation -> Simulation result charts
```
