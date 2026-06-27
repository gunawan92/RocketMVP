# API SPECIFICATION (API_SPEC)

## Project Name

Rocket Mission Planner

## Version

1.0 (MVP)

## Status

Draft

## Last Updated

June 2026

---

# 1. Overview

API Specification ini mendefinisikan kontrak API untuk backend Rocket Mission Planner.

Backend menggunakan FastAPI dengan pendekatan API-first. Semua fitur utama seperti mission management, rocket configuration, rocket calculator, dan simulation engine harus dapat diakses melalui REST API.

Tujuan dokumen ini:

- Menjadi acuan implementasi backend.
- Menjadi acuan integrasi frontend React.
- Menjadi dasar testing API.
- Menjaga response format tetap konsisten.

---

# 2. API Principles

## 2.1 API Style

API menggunakan RESTful JSON API.

Format komunikasi:

```txt
Request Body  : JSON
Response Body : JSON
Content-Type  : application/json
```

## 2.2 Versioning

Semua endpoint MVP menggunakan prefix:

```txt
/api/v1
```

Contoh:

```txt
GET /api/v1/missions
POST /api/v1/calculators/delta-v
POST /api/v1/simulations/run
```

## 2.3 Authentication

Untuk MVP:

```txt
Authentication: Not required
Authorization : Not required
```

Catatan:

- API bersifat public untuk development lokal.
- Authentication akan ditambahkan pada versi berikutnya.
- Jangan hardcode user system di MVP.

---

# 3. Base URL

## Local Development

```txt
http://localhost:8000/api/v1
```

## Production Example

```txt
https://api.rocket-mission-planner.com/api/v1
```

---

# 4. Standard Response Format

## 4.1 Success Response

Semua response sukses menggunakan format berikut:

```json
{
  "success": true,
  "message": "Request processed successfully",
  "data": {},
  "meta": {}
}
```

Keterangan:

| Field | Type | Description |
|---|---|---|
| success | boolean | Status request |
| message | string | Pesan ringkas |
| data | object / array / null | Payload utama |
| meta | object | Metadata seperti pagination |

## 4.2 Error Response

Semua response error menggunakan format berikut:

```json
{
  "success": false,
  "message": "Validation error",
  "error": {
    "code": "VALIDATION_ERROR",
    "details": [
      {
        "field": "wet_mass",
        "message": "Wet mass must be greater than dry mass"
      }
    ]
  }
}
```

Keterangan:

| Field | Type | Description |
|---|---|---|
| success | boolean | Selalu false untuk error |
| message | string | Pesan error utama |
| error.code | string | Kode error internal |
| error.details | array | Detail error field atau process |

---

# 5. HTTP Status Code

| Status Code | Meaning | Usage |
|---|---|---|
| 200 | OK | Request berhasil |
| 201 | Created | Resource berhasil dibuat |
| 400 | Bad Request | Business rule tidak valid |
| 404 | Not Found | Resource tidak ditemukan |
| 422 | Unprocessable Entity | Schema validation gagal |
| 500 | Internal Server Error | Error tidak terduga |

---

# 6. Error Codes

| Error Code | Description |
|---|---|
| VALIDATION_ERROR | Input tidak sesuai schema |
| BUSINESS_RULE_ERROR | Input valid secara schema, tapi melanggar aturan bisnis |
| RESOURCE_NOT_FOUND | Data tidak ditemukan |
| SIMULATION_FAILED | RocketPy gagal menjalankan simulasi |
| DATABASE_ERROR | Operasi database gagal |
| INTERNAL_SERVER_ERROR | Error tidak terduga |

---

# 7. Pagination Standard

Endpoint list menggunakan query parameter:

```txt
?page=1&limit=10
```

Response meta:

```json
{
  "meta": {
    "page": 1,
    "limit": 10,
    "total": 100,
    "total_pages": 10
  }
}
```

Default:

```txt
page  = 1
limit = 10
```

Maximum limit:

```txt
100
```

---

# 8. Health Check API

## 8.1 Health Check

```txt
GET /api/v1/health
```

### Response 200

```json
{
  "success": true,
  "message": "Service is healthy",
  "data": {
    "service": "Rocket Mission Planner API",
    "status": "healthy",
    "version": "1.0.0"
  },
  "meta": {}
}
```

---

# 9. Mission API

Mission API digunakan untuk mengelola data misi.

## 9.1 Create Mission

```txt
POST /api/v1/missions
```

### Request Body

```json
{
  "name": "Test Flight 001",
  "description": "Basic vertical launch simulation"
}
```

### Validation Rules

| Field | Rule |
|---|---|
| name | Required, string, max 150 chars |
| description | Optional, string |

### Response 201

```json
{
  "success": true,
  "message": "Mission created successfully",
  "data": {
    "id": "8c8f1a6e-90ea-4a99-8ad4-66d3a8fef001",
    "name": "Test Flight 001",
    "description": "Basic vertical launch simulation",
    "status": "draft",
    "created_at": "2026-06-25T10:00:00Z",
    "updated_at": "2026-06-25T10:00:00Z"
  },
  "meta": {}
}
```

---

## 9.2 List Missions

```txt
GET /api/v1/missions?page=1&limit=10
```

### Response 200

```json
{
  "success": true,
  "message": "Missions retrieved successfully",
  "data": [
    {
      "id": "8c8f1a6e-90ea-4a99-8ad4-66d3a8fef001",
      "name": "Test Flight 001",
      "description": "Basic vertical launch simulation",
      "status": "draft",
      "created_at": "2026-06-25T10:00:00Z",
      "updated_at": "2026-06-25T10:00:00Z"
    }
  ],
  "meta": {
    "page": 1,
    "limit": 10,
    "total": 1,
    "total_pages": 1
  }
}
```

---

## 9.3 Get Mission Detail

```txt
GET /api/v1/missions/{mission_id}
```

### Response 200

```json
{
  "success": true,
  "message": "Mission retrieved successfully",
  "data": {
    "id": "8c8f1a6e-90ea-4a99-8ad4-66d3a8fef001",
    "name": "Test Flight 001",
    "description": "Basic vertical launch simulation",
    "status": "draft",
    "rockets": [],
    "simulation_results": [],
    "created_at": "2026-06-25T10:00:00Z",
    "updated_at": "2026-06-25T10:00:00Z"
  },
  "meta": {}
}
```

### Response 404

```json
{
  "success": false,
  "message": "Mission not found",
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "details": []
  }
}
```

---

## 9.4 Update Mission

```txt
PUT /api/v1/missions/{mission_id}
```

### Request Body

```json
{
  "name": "Updated Test Flight 001",
  "description": "Updated mission description",
  "status": "draft"
}
```

### Allowed Status

```txt
draft
ready
simulated
archived
```

### Response 200

```json
{
  "success": true,
  "message": "Mission updated successfully",
  "data": {
    "id": "8c8f1a6e-90ea-4a99-8ad4-66d3a8fef001",
    "name": "Updated Test Flight 001",
    "description": "Updated mission description",
    "status": "draft",
    "created_at": "2026-06-25T10:00:00Z",
    "updated_at": "2026-06-25T11:00:00Z"
  },
  "meta": {}
}
```

---

## 9.5 Delete Mission

```txt
DELETE /api/v1/missions/{mission_id}
```

### Response 200

```json
{
  "success": true,
  "message": "Mission deleted successfully",
  "data": null,
  "meta": {}
}
```

Implementation note:

- Untuk MVP, hard delete diperbolehkan.
- Jika mission dihapus, related rocket configuration dan simulation result ikut dihapus menggunakan cascade delete.

---

# 10. Engine API

Engine API digunakan untuk mengelola data engine roket.

## 10.1 Create Engine

```txt
POST /api/v1/engines
```

### Request Body

```json
{
  "name": "Solid Motor A",
  "thrust": 5000,
  "isp": 210,
  "burn_time": 4.5,
  "propellant_mass": 12.5,
  "motor_curve": [
    { "time": 0, "thrust": 0 },
    { "time": 0.5, "thrust": 4500 },
    { "time": 2.5, "thrust": 5200 },
    { "time": 4.5, "thrust": 0 }
  ],
  "nozzle_radius": 0.035,
  "throat_radius": 0.012
}
```

### Validation Rules

| Field | Rule | Unit |
|---|---|---|
| name | Required | - |
| thrust | Required, > 0 | Newton |
| isp | Required, > 0 | seconds |
| burn_time | Required, > 0 | seconds |
| propellant_mass | Optional, >= 0 | kg |
| motor_curve | Optional, min 2 points, starts at 0, time strictly increasing | seconds / Newton |
| nozzle_radius | Optional, > 0 | meter |
| throat_radius | Optional, > 0 | meter |

### Response 201

```json
{
  "success": true,
  "message": "Engine created successfully",
  "data": {
    "id": "2e7d499d-6d31-4634-9da7-09e3f126a001",
    "name": "Solid Motor A",
    "thrust": 5000,
    "isp": 210,
    "burn_time": 4.5,
    "propellant_mass": 12.5,
    "created_at": "2026-06-25T10:00:00Z",
    "updated_at": "2026-06-25T10:00:00Z"
  },
  "meta": {}
}
```

---

## 10.2 List Engines

```txt
GET /api/v1/engines?page=1&limit=10
```

### Response 200

```json
{
  "success": true,
  "message": "Engines retrieved successfully",
  "data": [
    {
      "id": "2e7d499d-6d31-4634-9da7-09e3f126a001",
      "name": "Solid Motor A",
      "thrust": 5000,
      "isp": 210,
      "burn_time": 4.5,
      "propellant_mass": 12.5
    }
  ],
  "meta": {
    "page": 1,
    "limit": 10,
    "total": 1,
    "total_pages": 1
  }
}
```

---

## 10.3 Get Engine Detail

```txt
GET /api/v1/engines/{engine_id}
```

### Response 200

```json
{
  "success": true,
  "message": "Engine retrieved successfully",
  "data": {
    "id": "2e7d499d-6d31-4634-9da7-09e3f126a001",
    "name": "Solid Motor A",
    "thrust": 5000,
    "isp": 210,
    "burn_time": 4.5,
    "propellant_mass": 12.5,
    "created_at": "2026-06-25T10:00:00Z",
    "updated_at": "2026-06-25T10:00:00Z"
  },
  "meta": {}
}
```

---

## 10.4 Update Engine

```txt
PUT /api/v1/engines/{engine_id}
```

### Request Body

```json
{
  "name": "Solid Motor A Updated",
  "thrust": 5200,
  "isp": 215,
  "burn_time": 4.8,
  "propellant_mass": 13
}
```

### Response 200

```json
{
  "success": true,
  "message": "Engine updated successfully",
  "data": {
    "id": "2e7d499d-6d31-4634-9da7-09e3f126a001",
    "name": "Solid Motor A Updated",
    "thrust": 5200,
    "isp": 215,
    "burn_time": 4.8,
    "propellant_mass": 13,
    "created_at": "2026-06-25T10:00:00Z",
    "updated_at": "2026-06-25T11:00:00Z"
  },
  "meta": {}
}
```

---

## 10.5 Delete Engine

```txt
DELETE /api/v1/engines/{engine_id}
```

### Response 200

```json
{
  "success": true,
  "message": "Engine deleted successfully",
  "data": null,
  "meta": {}
}
```

Business rule:

- Engine tidak boleh dihapus jika masih dipakai oleh rocket configuration aktif.
- Jika masih dipakai, return HTTP 400 dengan code `BUSINESS_RULE_ERROR`.

---

# 11. Rocket Configuration API

Rocket Configuration API digunakan untuk mengelola konfigurasi roket dalam sebuah mission.

## 11.1 Create Rocket Configuration

```txt
POST /api/v1/missions/{mission_id}/rockets
```

### Request Body

```json
{
  "name": "Single Stage Test Rocket",
  "wet_mass": 50,
  "dry_mass": 30,
  "payload_mass": 5,
  "engine_id": "2e7d499d-6d31-4634-9da7-09e3f126a001",
  "diameter": 0.18,
  "length": 1.8,
  "drag_coefficient": 0.75,
  "center_of_mass_position": 0.9,
  "motor_position": 1.4,
  "nose_length": 0.35,
  "nose_kind": "vonKarman",
  "fin_count": 4,
  "fin_root_chord": 0.22,
  "fin_tip_chord": 0.1,
  "fin_span": 0.12,
  "fin_position": 1.55
}
```

### Validation Rules

| Field | Rule | Unit |
|---|---|---|
| name | Required | - |
| wet_mass | Required, > 0 | kg |
| dry_mass | Required, > 0 | kg |
| payload_mass | Required, >= 0 | kg |
| engine_id | Required UUID | - |
| diameter | Optional, > 0 | meter |
| length | Optional, > 0 | meter |
| drag_coefficient | Optional, > 0 | - |
| center_of_mass_position | Optional, >= 0 | meter |
| motor_position | Optional, >= 0 | meter |
| nose_length | Optional, > 0 | meter |
| nose_kind | Optional | - |
| fin_count | Optional, > 0 | count |
| fin_root_chord | Optional, > 0 | meter |
| fin_tip_chord | Optional, > 0 | meter |
| fin_span | Optional, > 0 | meter |
| fin_position | Optional, >= 0 | meter |

Business rules:

- `wet_mass` must be greater than `dry_mass`.
- `payload_mass` must be less than or equal to `dry_mass`.
- `engine_id` must exist.
- `mission_id` must exist.

### Response 201

```json
{
  "success": true,
  "message": "Rocket configuration created successfully",
  "data": {
    "id": "7d65e83b-078d-4b37-a115-cae9b51f0001",
    "mission_id": "8c8f1a6e-90ea-4a99-8ad4-66d3a8fef001",
    "name": "Single Stage Test Rocket",
    "wet_mass": 50,
    "dry_mass": 30,
    "payload_mass": 5,
    "engine_id": "2e7d499d-6d31-4634-9da7-09e3f126a001",
    "created_at": "2026-06-25T10:00:00Z",
    "updated_at": "2026-06-25T10:00:00Z"
  },
  "meta": {}
}
```

---

## 11.2 List Rocket Configurations by Mission

```txt
GET /api/v1/missions/{mission_id}/rockets
```

### Response 200

```json
{
  "success": true,
  "message": "Rocket configurations retrieved successfully",
  "data": [
    {
      "id": "7d65e83b-078d-4b37-a115-cae9b51f0001",
      "mission_id": "8c8f1a6e-90ea-4a99-8ad4-66d3a8fef001",
      "name": "Single Stage Test Rocket",
      "wet_mass": 50,
      "dry_mass": 30,
      "payload_mass": 5,
      "engine_id": "2e7d499d-6d31-4634-9da7-09e3f126a001"
    }
  ],
  "meta": {}
}
```

---

## 11.3 Get Rocket Detail

```txt
GET /api/v1/rockets/{rocket_id}
```

### Response 200

```json
{
  "success": true,
  "message": "Rocket configuration retrieved successfully",
  "data": {
    "id": "7d65e83b-078d-4b37-a115-cae9b51f0001",
    "mission_id": "8c8f1a6e-90ea-4a99-8ad4-66d3a8fef001",
    "name": "Single Stage Test Rocket",
    "wet_mass": 50,
    "dry_mass": 30,
    "payload_mass": 5,
    "engine": {
      "id": "2e7d499d-6d31-4634-9da7-09e3f126a001",
      "name": "Solid Motor A",
      "thrust": 5000,
      "isp": 210,
      "burn_time": 4.5
    },
    "created_at": "2026-06-25T10:00:00Z",
    "updated_at": "2026-06-25T10:00:00Z"
  },
  "meta": {}
}
```

---

## 11.4 Update Rocket Configuration

```txt
PUT /api/v1/rockets/{rocket_id}
```

### Request Body

```json
{
  "name": "Updated Single Stage Rocket",
  "wet_mass": 55,
  "dry_mass": 32,
  "payload_mass": 5,
  "engine_id": "2e7d499d-6d31-4634-9da7-09e3f126a001"
}
```

### Response 200

```json
{
  "success": true,
  "message": "Rocket configuration updated successfully",
  "data": {
    "id": "7d65e83b-078d-4b37-a115-cae9b51f0001",
    "mission_id": "8c8f1a6e-90ea-4a99-8ad4-66d3a8fef001",
    "name": "Updated Single Stage Rocket",
    "wet_mass": 55,
    "dry_mass": 32,
    "payload_mass": 5,
    "engine_id": "2e7d499d-6d31-4634-9da7-09e3f126a001",
    "created_at": "2026-06-25T10:00:00Z",
    "updated_at": "2026-06-25T11:00:00Z"
  },
  "meta": {}
}
```

---

## 11.5 Delete Rocket Configuration

```txt
DELETE /api/v1/rockets/{rocket_id}
```

### Response 200

```json
{
  "success": true,
  "message": "Rocket configuration deleted successfully",
  "data": null,
  "meta": {}
}
```

---

# 12. Calculator API

Calculator API digunakan untuk kalkulasi numerik cepat tanpa menjalankan RocketPy.

Constants:

```txt
g0 = 9.80665 m/s²
```

---

## 12.1 Calculate Delta-V

```txt
POST /api/v1/calculators/delta-v
```

### Request Body

```json
{
  "isp": 210,
  "wet_mass": 50,
  "dry_mass": 30
}
```

### Formula

```txt
delta_v = isp * g0 * ln(wet_mass / dry_mass)
```

### Validation Rules

- `isp` must be greater than 0.
- `wet_mass` must be greater than 0.
- `dry_mass` must be greater than 0.
- `wet_mass` must be greater than `dry_mass`.

### Response 200

```json
{
  "success": true,
  "message": "Delta-V calculated successfully",
  "data": {
    "calculator_type": "delta_v",
    "input": {
      "isp": 210,
      "wet_mass": 50,
      "dry_mass": 30,
      "g0": 9.80665
    },
    "result": {
      "delta_v": 1051.78,
      "unit": "m/s"
    },
    "interpretation": "Estimated ideal velocity change without drag, gravity loss, or steering loss."
  },
  "meta": {}
}
```

---

## 12.2 Calculate TWR

```txt
POST /api/v1/calculators/twr
```

### Request Body

```json
{
  "thrust": 5000,
  "mass": 50
}
```

### Formula

```txt
twr = thrust / (mass * g0)
```

### Validation Rules

- `thrust` must be greater than 0.
- `mass` must be greater than 0.

### Response 200

```json
{
  "success": true,
  "message": "TWR calculated successfully",
  "data": {
    "calculator_type": "twr",
    "input": {
      "thrust": 5000,
      "mass": 50,
      "g0": 9.80665
    },
    "result": {
      "twr": 10.2,
      "unit": "dimensionless"
    },
    "interpretation": "Rocket can ascend. TWR is greater than 1."
  },
  "meta": {}
}
```

---

## 12.3 Calculate Payload Fraction

```txt
POST /api/v1/calculators/payload-fraction
```

### Request Body

```json
{
  "payload_mass": 5,
  "total_mass": 50
}
```

### Formula

```txt
payload_fraction = payload_mass / total_mass
payload_fraction_percentage = payload_fraction * 100
```

### Validation Rules

- `payload_mass` must be greater than or equal to 0.
- `total_mass` must be greater than 0.
- `payload_mass` must be less than or equal to `total_mass`.

### Response 200

```json
{
  "success": true,
  "message": "Payload fraction calculated successfully",
  "data": {
    "calculator_type": "payload_fraction",
    "input": {
      "payload_mass": 5,
      "total_mass": 50
    },
    "result": {
      "payload_fraction": 0.1,
      "payload_fraction_percentage": 10,
      "unit": "percent"
    },
    "interpretation": "Payload represents 10% of total rocket mass."
  },
  "meta": {}
}
```

---

## 12.4 Calculate Mass Ratio

```txt
POST /api/v1/calculators/mass-ratio
```

### Request Body

```json
{
  "wet_mass": 50,
  "dry_mass": 30
}
```

### Formula

```txt
mass_ratio = wet_mass / dry_mass
```

### Validation Rules

- `wet_mass` must be greater than 0.
- `dry_mass` must be greater than 0.
- `wet_mass` must be greater than `dry_mass`.

### Response 200

```json
{
  "success": true,
  "message": "Mass ratio calculated successfully",
  "data": {
    "calculator_type": "mass_ratio",
    "input": {
      "wet_mass": 50,
      "dry_mass": 30
    },
    "result": {
      "mass_ratio": 1.67,
      "unit": "dimensionless"
    },
    "interpretation": "Wet mass is 1.67 times the dry mass."
  },
  "meta": {}
}
```

---

## 12.5 Calculate Propellant Mass

```txt
POST /api/v1/calculators/propellant-mass
```

### Request Body

```json
{
  "wet_mass": 50,
  "dry_mass": 30
}
```

### Formula

```txt
propellant_mass = wet_mass - dry_mass
```

### Response 200

```json
{
  "success": true,
  "message": "Propellant mass calculated successfully",
  "data": {
    "calculator_type": "propellant_mass",
    "input": {
      "wet_mass": 50,
      "dry_mass": 30
    },
    "result": {
      "propellant_mass": 20,
      "unit": "kg"
    },
    "interpretation": "Rocket contains 20 kg of propellant mass."
  },
  "meta": {}
}
```

---

## 12.6 Calculate Initial Acceleration

```txt
POST /api/v1/calculators/initial-acceleration
```

### Request Body

```json
{
  "thrust": 5000,
  "mass": 50
}
```

### Formula

```txt
initial_acceleration = (thrust / mass) - g0
```

### Response 200

```json
{
  "success": true,
  "message": "Initial acceleration calculated successfully",
  "data": {
    "calculator_type": "initial_acceleration",
    "input": {
      "thrust": 5000,
      "mass": 50,
      "g0": 9.80665
    },
    "result": {
      "initial_acceleration": 90.19,
      "unit": "m/s²"
    },
    "interpretation": "Initial upward acceleration after gravity is approximately 90.19 m/s²."
  },
  "meta": {}
}
```

---

# 13. Simulation API

Simulation API digunakan untuk menjalankan simulasi RocketPy.

## 13.1 Run Simulation by Rocket ID

```txt
POST /api/v1/simulations/run
```

### Request Body

```json
{
  "mission_id": "8c8f1a6e-90ea-4a99-8ad4-66d3a8fef001",
  "rocket_id": "7d65e83b-078d-4b37-a115-cae9b51f0001",
  "environment": {
    "latitude": -6.2,
    "longitude": 106.8,
    "elevation": 10,
    "date": "2026-06-25"
  },
  "options": {
    "store_result": true,
    "include_time_series": true
  }
}
```

### Validation Rules

- `mission_id` must exist.
- `rocket_id` must exist.
- `rocket_id` must belong to `mission_id`.
- Environment is optional in MVP.
- If environment is not provided, system uses default environment.

### Default Environment

```json
{
  "latitude": 0,
  "longitude": 0,
  "elevation": 0
}
```

### Response 200

```json
{
  "success": true,
  "message": "Simulation completed successfully",
  "data": {
    "id": "118a2c46-bf7d-4d8d-a6c2-2cc872db0001",
    "mission_id": "8c8f1a6e-90ea-4a99-8ad4-66d3a8fef001",
    "rocket_id": "7d65e83b-078d-4b37-a115-cae9b51f0001",
    "status": "completed",
    "summary": {
      "apogee": 1250.5,
      "max_velocity": 315.7,
      "max_acceleration": 92.4,
      "flight_duration": 38.2
    },
    "units": {
      "apogee": "m",
      "max_velocity": "m/s",
      "max_acceleration": "m/s²",
      "flight_duration": "s"
    },
    "time_series": {
      "altitude": [
        { "time": 0, "value": 0 },
        { "time": 1, "value": 120 },
        { "time": 2, "value": 310 }
      ],
      "velocity": [
        { "time": 0, "value": 0 },
        { "time": 1, "value": 80 },
        { "time": 2, "value": 160 }
      ],
      "acceleration": [
        { "time": 0, "value": 9.8 },
        { "time": 1, "value": 14.2 },
        { "time": 2, "value": 18.5 }
      ]
    },
    "created_at": "2026-06-25T10:00:00Z"
  },
  "meta": {}
}
```

### Response 500

```json
{
  "success": false,
  "message": "Simulation failed",
  "error": {
    "code": "SIMULATION_FAILED",
    "details": [
      {
        "field": "rocketpy",
        "message": "RocketPy failed to complete flight simulation"
      }
    ]
  }
}
```

---

## 13.2 List Simulation Results by Mission

```txt
GET /api/v1/missions/{mission_id}/simulations
```

### Response 200

```json
{
  "success": true,
  "message": "Simulation results retrieved successfully",
  "data": [
    {
      "id": "118a2c46-bf7d-4d8d-a6c2-2cc872db0001",
      "mission_id": "8c8f1a6e-90ea-4a99-8ad4-66d3a8fef001",
      "rocket_id": "7d65e83b-078d-4b37-a115-cae9b51f0001",
      "status": "completed",
      "summary": {
        "apogee": 1250.5,
        "max_velocity": 315.7,
        "max_acceleration": 92.4,
        "flight_duration": 38.2
      },
      "created_at": "2026-06-25T10:00:00Z"
    }
  ],
  "meta": {}
}
```

---

## 13.3 Get Simulation Result Detail

```txt
GET /api/v1/simulations/{simulation_id}
```

### Response 200

```json
{
  "success": true,
  "message": "Simulation result retrieved successfully",
  "data": {
    "id": "118a2c46-bf7d-4d8d-a6c2-2cc872db0001",
    "mission_id": "8c8f1a6e-90ea-4a99-8ad4-66d3a8fef001",
    "rocket_id": "7d65e83b-078d-4b37-a115-cae9b51f0001",
    "status": "completed",
    "summary": {
      "apogee": 1250.5,
      "max_velocity": 315.7,
      "max_acceleration": 92.4,
      "flight_duration": 38.2
    },
    "time_series": {
      "altitude": [],
      "velocity": [],
      "acceleration": []
    },
    "raw_result": {},
    "created_at": "2026-06-25T10:00:00Z"
  },
  "meta": {}
}
```

---

## 13.4 Delete Simulation Result

```txt
DELETE /api/v1/simulations/{simulation_id}
```

### Response 200

```json
{
  "success": true,
  "message": "Simulation result deleted successfully",
  "data": null,
  "meta": {}
}
```

---

# 14. Comparison API

Comparison API digunakan untuk membandingkan beberapa simulation result.

## 14.1 Compare Simulation Results

```txt
POST /api/v1/simulations/compare
```

### Request Body

```json
{
  "simulation_ids": [
    "118a2c46-bf7d-4d8d-a6c2-2cc872db0001",
    "118a2c46-bf7d-4d8d-a6c2-2cc872db0002"
  ]
}
```

### Validation Rules

- `simulation_ids` must contain at least 2 items.
- Maximum 5 simulation results can be compared in MVP.
- All simulation IDs must exist.

### Response 200

```json
{
  "success": true,
  "message": "Simulation comparison generated successfully",
  "data": {
    "items": [
      {
        "simulation_id": "118a2c46-bf7d-4d8d-a6c2-2cc872db0001",
        "rocket_id": "7d65e83b-078d-4b37-a115-cae9b51f0001",
        "summary": {
          "apogee": 1250.5,
          "max_velocity": 315.7,
          "max_acceleration": 92.4,
          "flight_duration": 38.2
        }
      },
      {
        "simulation_id": "118a2c46-bf7d-4d8d-a6c2-2cc872db0002",
        "rocket_id": "7d65e83b-078d-4b37-a115-cae9b51f0002",
        "summary": {
          "apogee": 1488.2,
          "max_velocity": 350.1,
          "max_acceleration": 88.9,
          "flight_duration": 42.6
        }
      }
    ],
    "best_result": {
      "highest_apogee_simulation_id": "118a2c46-bf7d-4d8d-a6c2-2cc872db0002",
      "highest_velocity_simulation_id": "118a2c46-bf7d-4d8d-a6c2-2cc872db0002"
    }
  },
  "meta": {}
}
```

---

# 15. Dashboard API

Dashboard API digunakan frontend untuk menampilkan ringkasan.

## 15.1 Get Dashboard Summary

```txt
GET /api/v1/dashboard/summary
```

### Response 200

```json
{
  "success": true,
  "message": "Dashboard summary retrieved successfully",
  "data": {
    "total_missions": 10,
    "total_rockets": 15,
    "total_simulations": 25,
    "best_apogee": {
      "value": 1500.75,
      "unit": "m",
      "simulation_id": "118a2c46-bf7d-4d8d-a6c2-2cc872db0003"
    },
    "latest_simulation": {
      "id": "118a2c46-bf7d-4d8d-a6c2-2cc872db0004",
      "status": "completed",
      "created_at": "2026-06-25T10:00:00Z"
    }
  },
  "meta": {}
}
```

---

# 16. Validation Summary

## 16.1 Mass Validation

| Field | Rule |
|---|---|
| wet_mass | Must be greater than 0 |
| dry_mass | Must be greater than 0 |
| wet_mass | Must be greater than dry_mass |
| payload_mass | Must be greater than or equal to 0 |
| payload_mass | Must be less than or equal to dry_mass |

## 16.2 Engine Validation

| Field | Rule |
|---|---|
| thrust | Must be greater than 0 |
| isp | Must be greater than 0 |
| burn_time | Must be greater than 0 |
| propellant_mass | Must be greater than or equal to 0 |

## 16.3 Simulation Validation

| Field | Rule |
|---|---|
| mission_id | Must exist |
| rocket_id | Must exist |
| rocket_id | Must belong to mission_id |
| environment.elevation | Can be positive, zero, or negative |
| environment.latitude | Must be between -90 and 90 |
| environment.longitude | Must be between -180 and 180 |

---

# 17. Units Standard

| Quantity | Unit |
|---|---|
| Mass | kg |
| Thrust | Newton |
| Specific Impulse | seconds |
| Delta-V | m/s |
| Velocity | m/s |
| Acceleration | m/s² |
| Altitude | meter |
| Flight Duration | seconds |
| Latitude | decimal degrees |
| Longitude | decimal degrees |
| Elevation | meter |

---

# 18. API Implementation Notes

## 18.1 FastAPI Router Suggestion

```txt
app/api/v1/
├── health.py
├── missions.py
├── engines.py
├── rockets.py
├── calculators.py
├── simulations.py
└── dashboard.py
```

## 18.2 Service Layer Suggestion

```txt
app/services/
├── mission_service.py
├── engine_service.py
├── rocket_service.py
├── calculator_service.py
├── simulation_service.py
└── dashboard_service.py
```

## 18.3 Schema Suggestion

```txt
app/schemas/
├── common.py
├── mission.py
├── engine.py
├── rocket.py
├── calculator.py
├── simulation.py
└── dashboard.py
```

---

# 19. API Endpoint Summary

## Health

| Method | Endpoint | Description |
|---|---|---|
| GET | /api/v1/health | Health check |

## Missions

| Method | Endpoint | Description |
|---|---|---|
| POST | /api/v1/missions | Create mission |
| GET | /api/v1/missions | List missions |
| GET | /api/v1/missions/{mission_id} | Get mission detail |
| PUT | /api/v1/missions/{mission_id} | Update mission |
| DELETE | /api/v1/missions/{mission_id} | Delete mission |

## Engines

| Method | Endpoint | Description |
|---|---|---|
| POST | /api/v1/engines | Create engine |
| GET | /api/v1/engines | List engines |
| GET | /api/v1/engines/{engine_id} | Get engine detail |
| PUT | /api/v1/engines/{engine_id} | Update engine |
| DELETE | /api/v1/engines/{engine_id} | Delete engine |

## Rockets

| Method | Endpoint | Description |
|---|---|---|
| POST | /api/v1/missions/{mission_id}/rockets | Create rocket configuration |
| GET | /api/v1/missions/{mission_id}/rockets | List rocket configurations by mission |
| GET | /api/v1/rockets/{rocket_id} | Get rocket detail |
| PUT | /api/v1/rockets/{rocket_id} | Update rocket configuration |
| DELETE | /api/v1/rockets/{rocket_id} | Delete rocket configuration |

## Calculators

| Method | Endpoint | Description |
|---|---|---|
| POST | /api/v1/calculators/delta-v | Calculate Delta-V |
| POST | /api/v1/calculators/twr | Calculate TWR |
| POST | /api/v1/calculators/payload-fraction | Calculate Payload Fraction |
| POST | /api/v1/calculators/mass-ratio | Calculate Mass Ratio |
| POST | /api/v1/calculators/propellant-mass | Calculate Propellant Mass |
| POST | /api/v1/calculators/initial-acceleration | Calculate Initial Acceleration |

## Simulations

| Method | Endpoint | Description |
|---|---|---|
| POST | /api/v1/simulations/run | Run simulation |
| GET | /api/v1/missions/{mission_id}/simulations | List simulation results by mission |
| GET | /api/v1/simulations/{simulation_id} | Get simulation detail |
| DELETE | /api/v1/simulations/{simulation_id} | Delete simulation result |
| POST | /api/v1/simulations/compare | Compare simulation results |

## Dashboard

| Method | Endpoint | Description |
|---|---|---|
| GET | /api/v1/dashboard/summary | Get dashboard summary |

---

# 20. MVP API Scope

Endpoint yang wajib ada di MVP:

```txt
GET    /api/v1/health
POST   /api/v1/missions
GET    /api/v1/missions
GET    /api/v1/missions/{mission_id}
PUT    /api/v1/missions/{mission_id}
DELETE /api/v1/missions/{mission_id}

POST   /api/v1/engines
GET    /api/v1/engines
GET    /api/v1/engines/{engine_id}
PUT    /api/v1/engines/{engine_id}
DELETE /api/v1/engines/{engine_id}

POST   /api/v1/missions/{mission_id}/rockets
GET    /api/v1/missions/{mission_id}/rockets
GET    /api/v1/rockets/{rocket_id}
PUT    /api/v1/rockets/{rocket_id}
DELETE /api/v1/rockets/{rocket_id}

POST   /api/v1/calculators/delta-v
POST   /api/v1/calculators/twr
POST   /api/v1/calculators/payload-fraction
POST   /api/v1/calculators/mass-ratio

POST   /api/v1/simulations/run
GET    /api/v1/missions/{mission_id}/simulations
GET    /api/v1/simulations/{simulation_id}
```

Endpoint opsional MVP:

```txt
POST   /api/v1/calculators/propellant-mass
POST   /api/v1/calculators/initial-acceleration
DELETE /api/v1/simulations/{simulation_id}
POST   /api/v1/simulations/compare
GET    /api/v1/dashboard/summary
```

---

# 21. Acceptance Criteria

API MVP dianggap selesai apabila:

- Health check dapat diakses.
- Mission dapat dibuat, dibaca, diubah, dan dihapus.
- Engine dapat dibuat, dibaca, diubah, dan dihapus.
- Rocket configuration dapat dibuat berdasarkan mission.
- Calculator Delta-V berjalan sesuai formula.
- Calculator TWR berjalan sesuai formula.
- Calculator Payload Fraction berjalan sesuai formula.
- Calculator Mass Ratio berjalan sesuai formula.
- Simulation dapat dijalankan dari mission dan rocket configuration.
- Simulation result dapat disimpan ke database.
- Simulation result dapat dibaca kembali.
- Semua response sukses mengikuti standard response format.
- Semua response error mengikuti standard error format.
- Semua input numerik divalidasi.
- Swagger/OpenAPI FastAPI dapat digunakan untuk testing manual.

---

# 22. Testing Checklist

## Calculator API Tests

- Delta-V returns correct value.
- Delta-V rejects wet mass lower than dry mass.
- TWR returns correct value.
- Payload fraction rejects payload greater than total mass.
- Mass ratio rejects dry mass equal to zero.

## Mission API Tests

- Create mission success.
- Get mission detail success.
- Get missing mission returns 404.
- Update mission success.
- Delete mission success.

## Engine API Tests

- Create engine success.
- Reject negative thrust.
- Reject zero ISP.
- Reject zero burn time.
- Prevent delete when engine is used by rocket configuration.

## Rocket API Tests

- Create rocket configuration success.
- Reject wet mass lower than dry mass.
- Reject payload mass greater than dry mass.
- Reject missing engine ID.

## Simulation API Tests

- Run simulation success with valid mission and rocket.
- Reject simulation with missing mission.
- Reject simulation with missing rocket.
- Store simulation result after successful run.
- Return simulation detail successfully.

---

# 23. Future API Scope

## V2

- Authentication API
- User API
- Mission sharing API
- Rocket template API
- Engine library API

## V3

- Multi-stage rocket API
- Orbit simulation API
- Satellite deployment API

## V4

- Moon mission API
- Mars mission API
- Interplanetary transfer API

---

# 24. Implementation Order

Recommended implementation order:

1. Common response schema
2. Error handler
3. Health endpoint
4. Mission CRUD
5. Engine CRUD
6. Rocket configuration CRUD
7. Calculator endpoints
8. Simulation endpoint mock
9. RocketPy integration
10. Simulation result storage
11. Simulation result detail endpoint
12. Dashboard summary endpoint
13. API tests
14. Swagger documentation review

---

# 25. Notes

- Jangan membuat authentication pada MVP kecuali benar-benar dibutuhkan.
- Jangan membuat multi-stage rocket pada MVP.
- Jangan membuat orbital simulation pada MVP.
- Fokus utama MVP adalah user dapat membuat mission, mengatur rocket, menjalankan calculator, menjalankan simulation, dan melihat hasilnya.
