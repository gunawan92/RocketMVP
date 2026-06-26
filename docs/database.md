# DATABASE DESIGN DOCUMENT

## Project Name

Rocket Mission Planner

## Document Name

DATABASE.md

## Version

1.0 (MVP)

## Status

Draft

## Last Updated

June 2026

---

# 1. Overview

Rocket Mission Planner menggunakan database untuk menyimpan data misi, konfigurasi roket, data engine, hasil kalkulasi, dan hasil simulasi penerbangan.

Database utama yang digunakan adalah **PostgreSQL** karena struktur data pada MVP bersifat relasional dan membutuhkan konsistensi antar entitas.

Untuk data hasil simulasi yang fleksibel seperti time-series altitude, velocity, acceleration, dan raw output dari RocketPy, sistem menggunakan tipe data **JSONB** di PostgreSQL.

Pendekatan ini memberikan kombinasi terbaik antara:

- Struktur relasional yang kuat
- Konsistensi data
- Kemudahan query
- Fleksibilitas penyimpanan hasil simulasi
- Kemudahan integrasi dengan SQLAlchemy dan Alembic

---

# 2. Database Decision



## Primary Database

```txt
PostgreSQL 16+
```

## ORM

```txt
SQLAlchemy 2.x
```

## Migration Tool

```txt
Alembic
```

## Flexible Data Storage

```txt
PostgreSQL JSONB
```

## ID Strategy

```txt
UUID
```

## Timestamp Strategy

```txt
created_at
updated_at
```

## Soft Delete

```txt
Not required for MVP
```

## Cache

```txt
Not required for MVP
```

## Message Queue

```txt
Not required for MVP
```

---

# 3. Why PostgreSQL

PostgreSQL dipilih karena project ini memiliki data yang saling berelasi.

Contoh relasi utama:

```txt
Mission -> Rocket Configuration
Mission -> Simulation Result
Rocket -> Engine
Rocket -> Calculator Result
```

PostgreSQL cocok untuk:

- Menyimpan data mission secara konsisten
- Menjaga foreign key antar table
- Melakukan query analitik sederhana
- Menyimpan data semi-terstruktur menggunakan JSONB
- Mendukung migration yang rapi dengan Alembic
- Cocok untuk aplikasi API-first berbasis FastAPI

---

# 4. Why Not MongoDB for MVP

MongoDB tidak dipilih sebagai database utama MVP karena struktur data Rocket Mission Planner masih jelas secara relasional.

MongoDB dapat dipertimbangkan di masa depan jika aplikasi mulai menyimpan:

- Telemetry real-time skala besar
- Simulation event streaming
- Sensor data fleksibel
- Log eksperimen dalam jumlah besar
- Data yang schema-nya sering berubah

Untuk MVP, PostgreSQL sudah cukup dan lebih aman secara desain.

---

# 5. Database Design Principles

Desain database mengikuti prinsip berikut:

1. **Relational first**  
   Data utama disimpan dalam table relasional.

2. **JSONB for simulation output**  
   Data simulasi yang fleksibel disimpan dalam JSONB.

3. **UUID as primary key**  
   Setiap record menggunakan UUID agar aman untuk integrasi API.

4. **Explicit foreign keys**  
   Relasi antar table harus jelas.

5. **Validation at application and database level**  
   Validasi dilakukan di Pydantic, service layer, dan constraint database.

6. **MVP simplicity**  
   Tidak membuat table terlalu banyak sebelum dibutuhkan.

---

# 6. Entity Relationship Overview

## Core Entities

```txt
missions
rockets
engines
calculator_results
simulation_results
```

## Relationship Diagram

```txt
missions
   │
   ├── rockets
   │      │
   │      └── engines
   │
   ├── calculator_results
   │
   └── simulation_results
```

## Relationship Summary

| Entity | Relationship | Description |
|---|---|---|
| missions | has many rockets | Satu misi dapat memiliki beberapa konfigurasi roket |
| rockets | belongs to mission | Setiap roket terikat ke satu mission |
| rockets | belongs to engine | Setiap roket dapat memakai satu engine |
| missions | has many calculator_results | Satu mission dapat memiliki banyak hasil kalkulasi |
| missions | has many simulation_results | Satu mission dapat memiliki banyak hasil simulasi |
| simulation_results | belongs to rocket | Hasil simulasi berasal dari satu konfigurasi roket |

---

# 7. Tables

## 7.1 missions

Table `missions` menyimpan data utama misi.

### Columns

| Column | Type | Required | Description |
|---|---|---:|---|
| id | UUID | Yes | Primary key |
| name | VARCHAR(150) | Yes | Nama mission |
| description | TEXT | No | Deskripsi mission |
| status | VARCHAR(50) | Yes | Status mission |
| created_at | TIMESTAMP | Yes | Waktu dibuat |
| updated_at | TIMESTAMP | Yes | Waktu terakhir diubah |

### Status Values

```txt
DRAFT
READY
SIMULATED
ARCHIVED
```

### SQL Draft

```sql
CREATE TABLE missions (
    id UUID PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    description TEXT,
    status VARCHAR(50) NOT NULL DEFAULT 'DRAFT',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

---

## 7.2 engines

Table `engines` menyimpan data engine roket.

### Columns

| Column | Type | Required | Description |
|---|---|---:|---|
| id | UUID | Yes | Primary key |
| name | VARCHAR(150) | Yes | Nama engine |
| thrust | DOUBLE PRECISION | Yes | Thrust dalam Newton |
| isp | DOUBLE PRECISION | Yes | Specific impulse dalam detik |
| burn_time | DOUBLE PRECISION | No | Durasi pembakaran dalam detik |
| propellant_mass | DOUBLE PRECISION | No | Massa propellant dalam kg |
| manufacturer | VARCHAR(150) | No | Nama pembuat engine |
| notes | TEXT | No | Catatan tambahan |
| created_at | TIMESTAMP | Yes | Waktu dibuat |
| updated_at | TIMESTAMP | Yes | Waktu terakhir diubah |

### Validation Rules

```txt
thrust > 0
isp > 0
burn_time > 0 if provided
propellant_mass > 0 if provided
```

### SQL Draft

```sql
CREATE TABLE engines (
    id UUID PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    thrust DOUBLE PRECISION NOT NULL CHECK (thrust > 0),
    isp DOUBLE PRECISION NOT NULL CHECK (isp > 0),
    burn_time DOUBLE PRECISION CHECK (burn_time IS NULL OR burn_time > 0),
    propellant_mass DOUBLE PRECISION CHECK (propellant_mass IS NULL OR propellant_mass > 0),
    manufacturer VARCHAR(150),
    notes TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

---

## 7.3 rockets

Table `rockets` menyimpan konfigurasi roket.

### Columns

| Column | Type | Required | Description |
|---|---|---:|---|
| id | UUID | Yes | Primary key |
| mission_id | UUID | Yes | Foreign key ke missions |
| engine_id | UUID | No | Foreign key ke engines |
| name | VARCHAR(150) | Yes | Nama konfigurasi roket |
| wet_mass | DOUBLE PRECISION | Yes | Massa penuh dalam kg |
| dry_mass | DOUBLE PRECISION | Yes | Massa kering dalam kg |
| payload_mass | DOUBLE PRECISION | Yes | Massa payload dalam kg |
| diameter | DOUBLE PRECISION | No | Diameter roket dalam meter |
| length | DOUBLE PRECISION | No | Panjang roket dalam meter |
| drag_coefficient | DOUBLE PRECISION | No | Koefisien drag |
| notes | TEXT | No | Catatan tambahan |
| created_at | TIMESTAMP | Yes | Waktu dibuat |
| updated_at | TIMESTAMP | Yes | Waktu terakhir diubah |

### Validation Rules

```txt
wet_mass > 0
dry_mass > 0
payload_mass >= 0
wet_mass > dry_mass
diameter > 0 if provided
length > 0 if provided
drag_coefficient > 0 if provided
```

### SQL Draft

```sql
CREATE TABLE rockets (
    id UUID PRIMARY KEY,
    mission_id UUID NOT NULL REFERENCES missions(id) ON DELETE CASCADE,
    engine_id UUID REFERENCES engines(id) ON DELETE SET NULL,
    name VARCHAR(150) NOT NULL,
    wet_mass DOUBLE PRECISION NOT NULL CHECK (wet_mass > 0),
    dry_mass DOUBLE PRECISION NOT NULL CHECK (dry_mass > 0),
    payload_mass DOUBLE PRECISION NOT NULL CHECK (payload_mass >= 0),
    diameter DOUBLE PRECISION CHECK (diameter IS NULL OR diameter > 0),
    length DOUBLE PRECISION CHECK (length IS NULL OR length > 0),
    drag_coefficient DOUBLE PRECISION CHECK (drag_coefficient IS NULL OR drag_coefficient > 0),
    notes TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT check_wet_mass_greater_than_dry_mass CHECK (wet_mass > dry_mass)
);
```

---

## 7.4 calculator_results

Table `calculator_results` menyimpan hasil kalkulasi rumus sederhana.

Contoh kalkulasi:

- Delta-V
- TWR
- Payload Fraction
- Mass Ratio
- Burn Time
- Mass Flow Rate

### Columns

| Column | Type | Required | Description |
|---|---|---:|---|
| id | UUID | Yes | Primary key |
| mission_id | UUID | No | Foreign key ke missions |
| rocket_id | UUID | No | Foreign key ke rockets |
| calculator_type | VARCHAR(100) | Yes | Jenis kalkulasi |
| input_data | JSONB | Yes | Input kalkulasi |
| result_data | JSONB | Yes | Hasil kalkulasi |
| created_at | TIMESTAMP | Yes | Waktu kalkulasi dibuat |

### Calculator Type Values

```txt
DELTA_V
TWR
PAYLOAD_FRACTION
MASS_RATIO
BURN_TIME
MASS_FLOW_RATE
INITIAL_ACCELERATION
```

### Example input_data

```json
{
  "isp": 250,
  "g0": 9.80665,
  "wet_mass": 100,
  "dry_mass": 40
}
```

### Example result_data

```json
{
  "value": 2246.5,
  "unit": "m/s",
  "formula": "delta_v = isp * g0 * ln(wet_mass / dry_mass)",
  "interpretation": "Delta-V calculated successfully"
}
```

### SQL Draft

```sql
CREATE TABLE calculator_results (
    id UUID PRIMARY KEY,
    mission_id UUID REFERENCES missions(id) ON DELETE SET NULL,
    rocket_id UUID REFERENCES rockets(id) ON DELETE SET NULL,
    calculator_type VARCHAR(100) NOT NULL,
    input_data JSONB NOT NULL,
    result_data JSONB NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

---

## 7.5 simulation_results

Table `simulation_results` menyimpan hasil simulasi RocketPy.

### Columns

| Column | Type | Required | Description |
|---|---|---:|---|
| id | UUID | Yes | Primary key |
| mission_id | UUID | Yes | Foreign key ke missions |
| rocket_id | UUID | Yes | Foreign key ke rockets |
| status | VARCHAR(50) | Yes | Status simulasi |
| apogee | DOUBLE PRECISION | No | Ketinggian maksimum dalam meter |
| max_velocity | DOUBLE PRECISION | No | Kecepatan maksimum dalam m/s |
| max_acceleration | DOUBLE PRECISION | No | Akselerasi maksimum dalam m/s² |
| flight_duration | DOUBLE PRECISION | No | Durasi penerbangan dalam detik |
| summary | JSONB | No | Ringkasan hasil simulasi |
| time_series | JSONB | No | Data grafik simulasi |
| raw_result | JSONB | No | Output mentah dari simulation engine |
| error_message | TEXT | No | Pesan error jika simulasi gagal |
| created_at | TIMESTAMP | Yes | Waktu simulasi dibuat |

### Status Values

```txt
PENDING
RUNNING
SUCCESS
FAILED
```

### Example summary

```json
{
  "apogee": {
    "value": 1200.5,
    "unit": "m"
  },
  "max_velocity": {
    "value": 320.2,
    "unit": "m/s"
  },
  "max_acceleration": {
    "value": 45.8,
    "unit": "m/s2"
  },
  "flight_duration": {
    "value": 88.4,
    "unit": "s"
  }
}
```

### Example time_series

```json
{
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
}
```

### SQL Draft

```sql
CREATE TABLE simulation_results (
    id UUID PRIMARY KEY,
    mission_id UUID NOT NULL REFERENCES missions(id) ON DELETE CASCADE,
    rocket_id UUID NOT NULL REFERENCES rockets(id) ON DELETE CASCADE,
    status VARCHAR(50) NOT NULL DEFAULT 'PENDING',
    apogee DOUBLE PRECISION,
    max_velocity DOUBLE PRECISION,
    max_acceleration DOUBLE PRECISION,
    flight_duration DOUBLE PRECISION,
    summary JSONB,
    time_series JSONB,
    raw_result JSONB,
    error_message TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

---

# 8. Optional Future Tables

Table berikut tidak wajib untuk MVP, tetapi dapat ditambahkan pada versi berikutnya.

## 8.1 environments

Untuk menyimpan konfigurasi lingkungan simulasi.

```txt
id
mission_id
name
latitude
longitude
elevation
air_temperature
wind_speed
pressure
created_at
updated_at
```

## 8.2 payloads

Untuk menyimpan data payload secara terpisah.

```txt
id
mission_id
name
mass
description
created_at
updated_at
```

## 8.3 simulation_events

Untuk menyimpan event detail dari simulasi.

```txt
id
simulation_result_id
event_type
time
altitude
velocity
data
created_at
```

## 8.4 users

Untuk versi dengan authentication.

```txt
id
name
email
password_hash
role
created_at
updated_at
```

---

# 9. Indexing Strategy

## Required Indexes

```sql
CREATE INDEX idx_rockets_mission_id ON rockets(mission_id);
CREATE INDEX idx_rockets_engine_id ON rockets(engine_id);
CREATE INDEX idx_calculator_results_mission_id ON calculator_results(mission_id);
CREATE INDEX idx_calculator_results_rocket_id ON calculator_results(rocket_id);
CREATE INDEX idx_calculator_results_type ON calculator_results(calculator_type);
CREATE INDEX idx_simulation_results_mission_id ON simulation_results(mission_id);
CREATE INDEX idx_simulation_results_rocket_id ON simulation_results(rocket_id);
CREATE INDEX idx_simulation_results_status ON simulation_results(status);
CREATE INDEX idx_simulation_results_created_at ON simulation_results(created_at);
```

## Optional JSONB Indexes

JSONB index tidak wajib untuk MVP awal.

Jika query terhadap `summary`, `time_series`, atau `raw_result` mulai sering dilakukan, tambahkan GIN index.

```sql
CREATE INDEX idx_simulation_results_summary_gin
ON simulation_results USING GIN (summary);

CREATE INDEX idx_calculator_results_result_data_gin
ON calculator_results USING GIN (result_data);
```

Catatan:

- Jangan membuat terlalu banyak index di awal.
- Index mempercepat read, tetapi memperlambat write.
- Mulai dengan index foreign key dan status terlebih dahulu.

---

# 10. Migration Strategy

Migration menggunakan Alembic.

## Goals

- Semua perubahan schema harus tercatat.
- Database production tidak boleh diubah manual tanpa migration.
- Migration harus bisa diulang di environment local, staging, dan production.

## Recommended Commands

Generate migration:

```bash
alembic revision --autogenerate -m "create initial tables"
```

Run migration:

```bash
alembic upgrade head
```

Rollback one step:

```bash
alembic downgrade -1
```

View migration history:

```bash
alembic history
```

Current database revision:

```bash
alembic current
```

---

# 11. Seed Data

Seed data digunakan untuk menyediakan engine awal dan contoh mission.

## MVP Seed Data

Minimal seed:

```txt
1 sample mission
2 sample engines
1 sample rocket configuration
```

## Example Engine Seed

```json
{
  "name": "Sample Solid Motor A",
  "thrust": 5000,
  "isp": 220,
  "burn_time": 3.5,
  "propellant_mass": 8.2,
  "manufacturer": "Internal Sample"
}
```

## Example Mission Seed

```json
{
  "name": "Demo Suborbital Mission",
  "description": "Sample mission for testing calculator and simulation flow",
  "status": "DRAFT"
}
```

Seed data harus ditempatkan di:

```txt
app/database/seed.py
```

atau folder:

```txt
scripts/seed.py
```

---

# 12. Data Validation Rules

Validasi harus dilakukan di dua level:

1. Pydantic schema
2. Database constraint

## Mission Validation

```txt
name is required
name max length = 150
status must be valid enum
```

## Engine Validation

```txt
thrust > 0
isp > 0
burn_time > 0 if provided
propellant_mass > 0 if provided
```

## Rocket Validation

```txt
wet_mass > 0
dry_mass > 0
wet_mass > dry_mass
payload_mass >= 0
payload_mass <= wet_mass
diameter > 0 if provided
length > 0 if provided
drag_coefficient > 0 if provided
```

## Calculator Validation

```txt
calculator_type must be valid enum
input_data must contain required formula variables
result_data must contain value and unit
```

## Simulation Validation

```txt
mission_id must exist
rocket_id must exist
rocket must have valid wet_mass and dry_mass
rocket must have engine data before running simulation
simulation status must be valid enum
```

---

# 13. JSONB Usage

JSONB digunakan untuk data yang bentuknya fleksibel.

## Fields Using JSONB

| Table | Field | Purpose |
|---|---|---|
| calculator_results | input_data | Menyimpan input formula |
| calculator_results | result_data | Menyimpan hasil formula |
| simulation_results | summary | Ringkasan hasil simulasi |
| simulation_results | time_series | Data grafik |
| simulation_results | raw_result | Output mentah RocketPy |

## Rules

- JSONB tidak digunakan untuk data inti yang sering difilter.
- Data penting seperti `apogee`, `max_velocity`, `max_acceleration`, dan `flight_duration` tetap disimpan sebagai column biasa.
- JSONB dipakai untuk data tambahan yang dapat berkembang.

---

# 14. API and Database Mapping

## Mission API

| Endpoint | Table |
|---|---|
| POST /api/missions | missions |
| GET /api/missions | missions |
| GET /api/missions/{id} | missions, rockets, simulation_results |
| PUT /api/missions/{id} | missions |
| DELETE /api/missions/{id} | missions |

## Rocket API

| Endpoint | Table |
|---|---|
| POST /api/rockets | rockets |
| GET /api/rockets | rockets |
| GET /api/rockets/{id} | rockets, engines |
| PUT /api/rockets/{id} | rockets |
| DELETE /api/rockets/{id} | rockets |

## Engine API

| Endpoint | Table |
|---|---|
| POST /api/engines | engines |
| GET /api/engines | engines |
| GET /api/engines/{id} | engines |
| PUT /api/engines/{id} | engines |
| DELETE /api/engines/{id} | engines |

## Calculator API

| Endpoint | Table |
|---|---|
| POST /api/calculators/delta-v | calculator_results |
| POST /api/calculators/twr | calculator_results |
| POST /api/calculators/payload-fraction | calculator_results |
| POST /api/calculators/mass-ratio | calculator_results |

## Simulation API

| Endpoint | Table |
|---|---|
| POST /api/simulations/run | simulation_results |
| GET /api/simulations/{id} | simulation_results |
| GET /api/missions/{id}/simulations | simulation_results |

---

# 15. SQLAlchemy Model Notes

## Recommended Base Fields

Setiap model utama sebaiknya memiliki:

```python
id: UUID
created_at: datetime
updated_at: datetime
```

Kecuali `calculator_results` dan `simulation_results`, `updated_at` tidak wajib karena record tersebut bersifat historical.

## Recommended Folder Structure

```txt
app/
├── models/
│   ├── mission.py
│   ├── rocket.py
│   ├── engine.py
│   ├── calculator_result.py
│   └── simulation_result.py
│
├── schemas/
│   ├── mission.py
│   ├── rocket.py
│   ├── engine.py
│   ├── calculator.py
│   └── simulation.py
│
└── database/
    ├── db.py
    ├── session.py
    └── seed.py
```

---

# 16. Backup Strategy

## Local Backup

Gunakan `pg_dump`.

```bash
pg_dump -U postgres -d rocket_mission_planner > backup.sql
```

## Restore

```bash
psql -U postgres -d rocket_mission_planner < backup.sql
```

## Production Backup Recommendation

Untuk production:

- Backup harian
- Simpan backup minimal 7 hari
- Gunakan compressed backup
- Test restore secara berkala

Example compressed backup:

```bash
pg_dump -U postgres -d rocket_mission_planner | gzip > backup_$(date +%Y%m%d).sql.gz
```

---

# 17. Local Development Database

Gunakan Docker Compose untuk local development.

## docker-compose Example

```yaml
services:
  postgres:
    image: postgres:16
    container_name: rocket_mission_postgres
    environment:
      POSTGRES_DB: rocket_mission_planner
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

## DATABASE_URL Example

```env
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/rocket_mission_planner
```

---

# 18. Naming Convention

## Table Names

Gunakan plural snake_case.

```txt
missions
rockets
engines
simulation_results
calculator_results
```

## Column Names

Gunakan snake_case.

```txt
created_at
updated_at
mission_id
rocket_id
calculator_type
```

## Enum Values

Gunakan uppercase string.

```txt
DRAFT
SUCCESS
FAILED
DELTA_V
```

## Index Names

Gunakan format:

```txt
idx_{table}_{column}
```

Example:

```txt
idx_simulation_results_mission_id
```

---

# 19. Data Retention

Untuk MVP:

- Mission disimpan permanen.
- Rocket configuration disimpan permanen selama mission masih ada.
- Calculator result disimpan sebagai history.
- Simulation result disimpan sebagai history.
- Tidak ada auto-delete.

Future:

- Tambahkan archive mission.
- Tambahkan delete simulation history.
- Tambahkan export result ke CSV/JSON.

---

# 20. Security Considerations

MVP belum menggunakan authentication, tetapi database tetap harus aman.

## Rules

- Jangan expose database langsung ke internet.
- Gunakan environment variable untuk credential.
- Jangan commit `.env` ke repository.
- Gunakan user database khusus aplikasi.
- Hindari memakai superuser PostgreSQL untuk aplikasi.
- Batasi akses port PostgreSQL di production.

## Recommended Production User

```sql
CREATE USER rocket_app_user WITH PASSWORD 'change_this_password';
GRANT CONNECT ON DATABASE rocket_mission_planner TO rocket_app_user;
GRANT USAGE ON SCHEMA public TO rocket_app_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO rocket_app_user;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO rocket_app_user;
```

---

# 21. Testing Strategy

## Database Test Scope

Test yang wajib ada:

- Create mission
- Update mission
- Delete mission
- Create rocket with valid mission_id
- Reject rocket if wet_mass <= dry_mass
- Create engine with valid thrust and ISP
- Reject engine with negative thrust
- Store calculator result as JSONB
- Store simulation result as JSONB
- Query simulation result by mission_id

## Test Database

Gunakan database terpisah untuk testing.

```env
TEST_DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/rocket_mission_test
```

---

# 22. Acceptance Criteria

DATABASE.md dianggap selesai apabila:

- Database utama ditentukan dengan jelas.
- Semua entity MVP terdefinisi.
- Relasi antar table jelas.
- Schema table memiliki column dan tipe data.
- Field JSONB dijelaskan penggunaannya.
- Index utama ditentukan.
- Migration strategy tersedia.
- Backup strategy tersedia.
- Validasi data dijelaskan.
- Database siap diimplementasikan dengan SQLAlchemy dan Alembic.

---

# 23. Implementation Order

Urutan implementasi database yang disarankan:

1. Setup PostgreSQL local dengan Docker Compose.
2. Setup SQLAlchemy connection.
3. Setup Alembic.
4. Buat model `missions`.
5. Buat model `engines`.
6. Buat model `rockets`.
7. Buat model `calculator_results`.
8. Buat model `simulation_results`.
9. Generate initial migration.
10. Run migration.
11. Buat seed data.
12. Buat database tests.
13. Hubungkan service layer ke database.

---

# 24. Future Database Scope

## V2

- users
- authentication_tokens
- mission_shares
- rocket_templates
- engine_library

## V3

- multi_stage_rockets
- rocket_stages
- orbit_results
- satellite_payloads

## V4

- interplanetary_missions
- celestial_bodies
- transfer_windows
- mission_cost_estimates

---

# 25. Final Recommendation

Untuk MVP Rocket Mission Planner, gunakan:

```txt
PostgreSQL + SQLAlchemy + Alembic + JSONB
```

Desain ini paling seimbang untuk kebutuhan MVP karena tetap sederhana, kuat secara relasional, dan fleksibel untuk menyimpan hasil simulasi yang kompleks.
