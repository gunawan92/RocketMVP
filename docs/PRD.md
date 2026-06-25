# PRODUCT REQUIREMENT DOCUMENT (PRD)

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

# 1. Executive Summary

Rocket Mission Planner adalah platform berbasis web yang memungkinkan pengguna melakukan simulasi dan analisis misi roket secara interaktif.

Aplikasi ini dirancang untuk menggabungkan kemampuan simulasi RocketPy dengan antarmuka web modern sehingga pengguna dapat menghitung performa roket, melakukan simulasi penerbangan, menyimpan misi, membandingkan konfigurasi roket, dan memvisualisasikan hasil simulasi dalam bentuk grafik.

Target utama produk ini bukan untuk menggantikan software aerospace profesional, melainkan menyediakan platform edukasi dan eksperimen engineering yang mudah digunakan oleh programmer, mahasiswa teknik, hobbyist, dan peneliti pemula.

---

# 2. Problem Statement

Saat ini sebagian besar software simulasi roket memiliki salah satu dari dua masalah utama:

1. Terlalu kompleks untuk pengguna umum.
2. Tidak menyediakan antarmuka web yang mudah digunakan.

RocketPy memiliki kemampuan simulasi roket yang baik, namun pengguna masih perlu memahami Python dan menulis kode untuk menjalankan simulasi.

Rocket Mission Planner bertujuan menjembatani kesenjangan tersebut dengan menyediakan platform berbasis web yang memungkinkan pengguna melakukan simulasi roket tanpa harus menulis kode secara langsung.

Produk ini akan menyediakan:

- Simulasi roket berbasis web.
- Dashboard visual untuk hasil simulasi.
- Penyimpanan data misi.
- Kalkulator dasar performa roket.
- Integrasi dengan RocketPy sebagai simulation engine.

---

# 3. Product Vision

Membangun platform simulasi roket berbasis web yang mudah digunakan, akurat secara matematis untuk kebutuhan edukasi, terbuka untuk eksperimen, dan dapat dikembangkan menjadi mission planning platform yang lebih besar.

Rocket Mission Planner diharapkan menjadi alat bantu pembelajaran dan eksperimen engineering untuk memahami performa roket, konfigurasi misi, dan hasil simulasi penerbangan secara visual.

---

# 4. Goals

## 4.1 Business Goals

- Membangun portofolio engineering project yang kuat.
- Menjadi platform edukasi roket berbasis web.
- Menjadi fondasi awal untuk simulator aerospace yang lebih besar.
- Menjadi showcase integrasi antara backend scientific computing dan frontend modern.

## 4.2 Product Goals

- User dapat membuat misi roket tanpa menulis kode Python.
- User dapat mengisi parameter roket melalui UI.
- User dapat menjalankan kalkulasi dasar roket.
- User dapat menjalankan simulasi berbasis RocketPy.
- User dapat melihat hasil simulasi dalam bentuk angka dan grafik.
- User dapat menyimpan hasil simulasi.
- User dapat membandingkan beberapa hasil simulasi.

## 4.3 Technical Goals

- Menggunakan API-first architecture.
- Backend modular dan mudah dikembangkan.
- Mendukung integrasi simulation engine secara terpisah.
- Mendukung penyimpanan konfigurasi dan hasil simulasi.
- Mudah dideploy menggunakan Docker.
- Siap dikembangkan untuk simulasi skala lebih besar di masa depan.

---

# 5. Target Users

## 5.1 Programmer

### Karakteristik

- Memiliki pengalaman coding.
- Ingin memahami fisika roket.
- Tertarik membuat eksperimen berbasis data.
- Membutuhkan akses data hasil simulasi yang jelas.

### Kebutuhan

- API yang jelas.
- Data simulasi yang mudah diproses.
- Simulasi cepat.
- Dokumentasi teknis.

---

## 5.2 Mahasiswa Teknik

### Karakteristik

- Sedang belajar aerospace engineering, mechanical engineering, physics, atau bidang terkait.
- Membutuhkan alat simulasi untuk belajar.
- Membutuhkan visualisasi untuk memahami konsep roket.

### Kebutuhan

- Visualisasi hasil simulasi.
- Perhitungan otomatis.
- Dokumentasi konsep dasar.
- Input parameter yang mudah dipahami.

---

## 5.3 Hobbyist

### Karakteristik

- Menyukai roket dan luar angkasa.
- Tidak selalu memiliki kemampuan pemrograman.
- Ingin mencoba berbagai konfigurasi roket.

### Kebutuhan

- UI sederhana.
- Input mudah.
- Grafik hasil simulasi.
- Penjelasan hasil yang tidak terlalu teknis.

---

## 5.4 Aerospace Enthusiast

### Karakteristik

- Memiliki minat tinggi pada dunia antariksa.
- Ingin memahami konsep dasar mission planning.
- Tertarik melihat performa roket dari berbagai konfigurasi.

### Kebutuhan

- Simulasi interaktif.
- Data performa roket.
- Grafik penerbangan.
- Perbandingan konfigurasi.

---

# 6. Platform

Rocket Mission Planner akan dikembangkan sebagai web application.

## Platform Utama

- Web Application

## Target Device

- Desktop
- Laptop
- Tablet

## Browser Target

- Google Chrome
- Microsoft Edge
- Mozilla Firefox

---

# 7. Technology Stack

## Backend

- Python
- FastAPI
- RocketPy
- SQLAlchemy
- Pydantic

## Database

- PostgreSQL

## Frontend

- React
- TailwindCSS

## Visualization

- Plotly

## Deployment

- Docker
- Linux VPS
- Nginx

## Development Tools

- Git
- GitHub
- Postman / Insomnia
- Alembic for database migration

---

# 8. User Flow

## 8.1 Basic Mission Simulation Flow

1. User membuka dashboard Rocket Mission Planner.
2. User membuat mission baru.
3. User mengisi informasi dasar misi.
4. User membuat atau memilih konfigurasi roket.
5. User mengisi parameter payload, massa roket, motor, diameter, panjang, dan parameter dasar lainnya.
6. User menjalankan kalkulasi awal seperti Delta-V, TWR, Mass Ratio, dan Payload Fraction.
7. User menjalankan simulasi RocketPy.
8. Sistem memproses simulasi melalui backend.
9. Sistem mengembalikan hasil simulasi.
10. User melihat hasil berupa ringkasan numerik dan grafik.
11. User menyimpan hasil simulasi.
12. User dapat membuka kembali hasil simulasi dari dashboard.
13. User dapat membandingkan dua atau lebih hasil simulasi.

---

# 9. Core Features

## 9.1 Rocket Calculator

Rocket Calculator digunakan untuk menghitung performa dasar roket sebelum menjalankan simulasi lengkap.

### Calculator yang tersedia

- Delta-V Calculator
- Thrust-to-Weight Ratio Calculator
- Payload Fraction Calculator
- Mass Ratio Calculator

### Output

- Nilai numerik hasil perhitungan.
- Satuan hasil.
- Penjelasan singkat hasil perhitungan.
- Validasi input jika nilai tidak valid.

---

## 9.2 Mission Management

Mission Management digunakan untuk mengelola data misi.

### Fitur

- Membuat mission baru.
- Melihat daftar mission.
- Melihat detail mission.
- Mengedit mission.
- Menghapus mission.
- Menyimpan konfigurasi mission.

### Data Mission

- Nama misi.
- Deskripsi misi.
- Payload.
- Rocket configuration.
- Simulation result.
- Created date.
- Updated date.

---

## 9.3 Rocket Configuration

Rocket Configuration digunakan untuk membuat konfigurasi teknis roket.

### Fitur

- Membuat konfigurasi roket.
- Menentukan massa roket.
- Menentukan massa propelan.
- Menentukan payload.
- Menentukan mesin.
- Menentukan diameter roket.
- Menentukan panjang roket.
- Menentukan parameter dasar aerodinamika.

### Output

- Konfigurasi roket tersimpan.
- Validasi input parameter.
- Ringkasan performa awal.

---

## 9.4 Simulation Engine

Simulation Engine digunakan untuk menjalankan simulasi berbasis RocketPy.

### Input

- Rocket configuration.
- Payload mass.
- Motor data.
- Launch rail angle.
- Launch rail length.
- Environment parameter.

### Output Utama

- Apogee.
- Max velocity.
- Max acceleration.
- Flight duration.
- Time series altitude.
- Time series velocity.
- Time series acceleration.

---

## 9.5 Visualization Dashboard

Visualization Dashboard digunakan untuk menampilkan hasil simulasi secara visual.

### Grafik MVP

- Altitude vs Time.
- Velocity vs Time.
- Acceleration vs Time.

### Ringkasan Numerik

- Apogee.
- Maximum velocity.
- Maximum acceleration.
- Flight duration.
- Launch status.

---

## 9.6 Simulation Comparison

Simulation Comparison digunakan untuk membandingkan beberapa hasil simulasi.

### Fitur

- Membandingkan dua atau lebih simulation result.
- Menampilkan perbedaan apogee.
- Menampilkan perbedaan max velocity.
- Menampilkan perbedaan max acceleration.
- Menampilkan grafik perbandingan sederhana.

---

# 10. MVP Scope

MVP fokus pada simulasi dasar roket satu tahap dengan input sederhana.

## 10.1 Included in MVP

### Rocket Calculator

- Delta-V Calculator.
- TWR Calculator.
- Payload Fraction Calculator.
- Mass Ratio Calculator.

### Mission Management

- Create mission.
- Read mission.
- Update mission.
- Delete mission.
- Store mission configuration.

### Rocket Configuration

- Create rocket configuration.
- Update rocket configuration.
- Store rocket parameter.
- Validate rocket parameter.

### Simulation Engine

- Integrasi RocketPy.
- Run basic rocket simulation.
- Store simulation result.
- Return simulation summary.

### Visualization

- Altitude vs Time chart.
- Velocity vs Time chart.
- Acceleration vs Time chart.
- Numeric simulation summary.

### Comparison

- Compare at least two simulation results.

---

# 11. Out of Scope for MVP

Fitur berikut tidak termasuk dalam MVP:

- Multi-user.
- Authentication.
- Role management.
- Multi-stage rockets.
- Orbital transfer.
- Moon mission planning.
- Mars mission planning.
- CFD simulation.
- Real-time weather integration.
- Multiplayer collaboration.
- Payment system.
- Public mission sharing.
- AI mission assistant.
- Advanced aerodynamic modeling.
- Satellite deployment.

---

# 12. Functional Requirements

## 12.1 Mission Requirements

- System must allow user to create a mission.
- System must allow user to view all missions.
- System must allow user to view mission detail.
- System must allow user to update mission data.
- System must allow user to delete a mission.
- System must store mission creation date and update date.

## 12.2 Rocket Configuration Requirements

- System must allow user to create rocket configuration.
- System must allow user to update rocket configuration.
- System must validate all required rocket parameters.
- System must reject invalid values such as negative mass, zero thrust, or invalid burn time.
- System must associate rocket configuration with a mission.

## 12.3 Calculator Requirements

- System must calculate Delta-V.
- System must calculate Thrust-to-Weight Ratio.
- System must calculate Payload Fraction.
- System must calculate Mass Ratio.
- System must return result with unit and explanation.
- System must display validation error if input is invalid.

## 12.4 Simulation Requirements

- System must accept rocket configuration as simulation input.
- System must run RocketPy simulation through backend service.
- System must return simulation summary.
- System must store simulation result in database.
- System must return error message if simulation fails.
- System must not delete mission data if simulation fails.

## 12.5 Visualization Requirements

- System must display altitude chart.
- System must display velocity chart.
- System must display acceleration chart.
- System must display simulation summary cards.
- System must allow user to open previous simulation result.

## 12.6 Comparison Requirements

- System must allow user to select at least two simulation results.
- System must display numerical comparison.
- System must display simple chart comparison.
- System must highlight differences between simulation results.

---

# 13. Non-Functional Requirements

## 13.1 Performance

- Basic simulation should complete in less than 10 seconds under normal input conditions.
- Mission list page should load in less than 3 seconds.
- Dashboard chart rendering should complete in less than 3 seconds after data is received.

## 13.2 Reliability

- System should handle simulation errors gracefully.
- Failed simulation should not corrupt stored mission data.
- API should return consistent error format.
- Database migration should be version controlled.

## 13.3 Security

- API input must be validated.
- System must reject negative or impossible numeric values.
- Backend must protect against oversized payloads.
- CORS configuration must be restricted for production.

## 13.4 Maintainability

- Backend should be modular.
- Simulation logic should be separated from API controller.
- Calculator logic should be separated from database logic.
- Codebase should follow clear folder structure.

## 13.5 Usability

- UI should be easy to understand for non-programmers.
- Form labels should use clear engineering terms.
- Error messages should be readable.
- Graphs should include axis labels and units.

---

# 14. Data Model

## 14.1 Mission

| Field | Type | Description |
|---|---|---|
| id | UUID / Integer | Unique mission identifier |
| name | String | Mission name |
| description | Text | Mission description |
| status | String | Draft, simulated, archived |
| created_at | DateTime | Created timestamp |
| updated_at | DateTime | Updated timestamp |

---

## 14.2 Rocket Configuration

| Field | Type | Description |
|---|---|---|
| id | UUID / Integer | Unique rocket configuration identifier |
| mission_id | UUID / Integer | Related mission ID |
| rocket_name | String | Rocket name |
| dry_mass | Float | Rocket dry mass |
| propellant_mass | Float | Propellant mass |
| payload_mass | Float | Payload mass |
| total_mass | Float | Total rocket mass |
| diameter | Float | Rocket diameter |
| length | Float | Rocket length |
| drag_coefficient | Float | Estimated drag coefficient |
| created_at | DateTime | Created timestamp |
| updated_at | DateTime | Updated timestamp |

---

## 14.3 Engine / Motor

| Field | Type | Description |
|---|---|---|
| id | UUID / Integer | Unique engine identifier |
| mission_id | UUID / Integer | Related mission ID |
| engine_name | String | Engine name |
| thrust | Float | Thrust value |
| burn_time | Float | Burn duration |
| specific_impulse | Float | Specific impulse |
| propellant_mass | Float | Propellant mass |
| created_at | DateTime | Created timestamp |

---

## 14.4 Simulation Result

| Field | Type | Description |
|---|---|---|
| id | UUID / Integer | Unique simulation result identifier |
| mission_id | UUID / Integer | Related mission ID |
| rocket_configuration_id | UUID / Integer | Related rocket configuration ID |
| apogee | Float | Maximum altitude |
| max_velocity | Float | Maximum velocity |
| max_acceleration | Float | Maximum acceleration |
| flight_duration | Float | Flight duration |
| altitude_time_series | JSON | Altitude data over time |
| velocity_time_series | JSON | Velocity data over time |
| acceleration_time_series | JSON | Acceleration data over time |
| status | String | Success or failed |
| error_message | Text | Error message if simulation failed |
| created_at | DateTime | Created timestamp |

---

# 15. API Endpoint Draft

## 15.1 Mission API

| Method | Endpoint | Description |
|---|---|---|
| GET | /api/missions | Get all missions |
| POST | /api/missions | Create new mission |
| GET | /api/missions/{mission_id} | Get mission detail |
| PUT | /api/missions/{mission_id} | Update mission |
| DELETE | /api/missions/{mission_id} | Delete mission |

---

## 15.2 Rocket Configuration API

| Method | Endpoint | Description |
|---|---|---|
| POST | /api/missions/{mission_id}/rocket-configurations | Create rocket configuration |
| GET | /api/missions/{mission_id}/rocket-configurations | Get rocket configurations by mission |
| GET | /api/rocket-configurations/{configuration_id} | Get rocket configuration detail |
| PUT | /api/rocket-configurations/{configuration_id} | Update rocket configuration |
| DELETE | /api/rocket-configurations/{configuration_id} | Delete rocket configuration |

---

## 15.3 Calculator API

| Method | Endpoint | Description |
|---|---|---|
| POST | /api/calculators/delta-v | Calculate Delta-V |
| POST | /api/calculators/twr | Calculate Thrust-to-Weight Ratio |
| POST | /api/calculators/payload-fraction | Calculate Payload Fraction |
| POST | /api/calculators/mass-ratio | Calculate Mass Ratio |

---

## 15.4 Simulation API

| Method | Endpoint | Description |
|---|---|---|
| POST | /api/missions/{mission_id}/simulations/run | Run simulation |
| GET | /api/missions/{mission_id}/simulations | Get simulation results by mission |
| GET | /api/simulations/{simulation_id} | Get simulation result detail |
| DELETE | /api/simulations/{simulation_id} | Delete simulation result |

---

## 15.5 Comparison API

| Method | Endpoint | Description |
|---|---|---|
| POST | /api/simulations/compare | Compare selected simulation results |

---

# 16. Acceptance Criteria

## 16.1 Rocket Calculator

- User can input required values for Delta-V calculation.
- System returns Delta-V result with unit.
- System shows validation error when input is invalid.
- User can calculate TWR, Payload Fraction, and Mass Ratio.

## 16.2 Mission Management

- User can create a mission from the dashboard.
- Created mission appears in mission list.
- User can open mission detail.
- User can update mission information.
- User can delete mission.

## 16.3 Rocket Configuration

- User can create rocket configuration inside a mission.
- System validates required rocket parameters.
- User can update configuration.
- Configuration can be used for simulation.

## 16.4 Simulation

- User can run simulation from a valid rocket configuration.
- System returns apogee, max velocity, max acceleration, and flight duration.
- Simulation result is stored in database.
- Failed simulation returns readable error message.

## 16.5 Visualization

- User can see Altitude vs Time chart.
- User can see Velocity vs Time chart.
- User can see Acceleration vs Time chart.
- User can see numerical summary of simulation result.

## 16.6 Comparison

- User can select at least two simulation results.
- System displays numerical comparison.
- System displays basic chart comparison.

---

# 17. Success Metrics

MVP dianggap berhasil apabila:

- User dapat membuat dan menyimpan minimal 1 misi.
- User dapat membuat minimal 1 konfigurasi roket.
- User dapat menghitung Delta-V, TWR, Payload Fraction, dan Mass Ratio.
- User dapat menjalankan simulasi dasar menggunakan RocketPy.
- Simulasi dasar menghasilkan output apogee, max velocity, max acceleration, dan flight duration.
- User dapat melihat minimal 3 grafik hasil simulasi.
- User dapat menyimpan hasil simulasi.
- User dapat membuka kembali hasil simulasi yang tersimpan.
- User dapat membandingkan minimal 2 hasil simulasi.
- Simulasi dasar selesai dalam waktu kurang dari 10 detik pada kondisi normal.

---

# 18. Risks

## 18.1 Technical Risks

### RocketPy Integration Risk

Integrasi RocketPy dapat membutuhkan adaptasi khusus agar cocok dengan input dari web form.

Mitigation:

- Buat service layer khusus untuk RocketPy.
- Pisahkan input validation dari simulation execution.
- Mulai dari konfigurasi simulasi paling sederhana.

---

### Simulation Performance Risk

Simulasi dapat berjalan lambat jika parameter terlalu kompleks.

Mitigation:

- Batasi parameter MVP.
- Gunakan timeout untuk simulation execution.
- Optimalkan payload data grafik.

---

### Accuracy Risk

Hasil simulasi dapat kurang akurat jika input tidak lengkap atau model terlalu sederhana.

Mitigation:

- Jelaskan batasan simulasi di UI.
- Gunakan satuan yang jelas.
- Tambahkan validasi input.
- Dokumentasikan asumsi simulasi.

---

## 18.2 Product Risks

### Scope Creep

Project dapat berkembang terlalu besar karena topik aerospace sangat luas.

Mitigation:

- Fokus MVP hanya pada roket satu tahap.
- Fitur orbital dan interplanetary masuk Future Scope.
- Gunakan Out of Scope sebagai batas development.

---

### User Complexity Risk

Pengguna non-teknis dapat kesulitan memahami parameter roket.

Mitigation:

- Tambahkan tooltip pada form.
- Gunakan label yang mudah dipahami.
- Sediakan default value.
- Sediakan template konfigurasi di versi berikutnya.

---

# 19. Future Scope

## 19.1 Version 2

- Multi-stage rockets.
- Engine library.
- Rocket templates.
- Reusable rocket profile.
- Better mission comparison.
- Export simulation result to CSV.

## 19.2 Version 3

- Orbit simulation.
- Satellite deployment simulation.
- Transfer orbit analysis.
- More advanced environment modeling.
- Real-time weather integration.

## 19.3 Version 4

- Moon mission planner.
- Mars mission planner.
- Interplanetary mission planner.
- Advanced trajectory planning.
- AI-assisted mission recommendation.

---

# 20. MVP Deliverables

## Deliverable 1: Rocket Calculator

- Delta-V Calculator.
- TWR Calculator.
- Payload Fraction Calculator.
- Mass Ratio Calculator.

## Deliverable 2: Mission Management

- CRUD mission.
- Mission detail page.
- Mission storage.

## Deliverable 3: Rocket Configuration

- Rocket configuration form.
- Rocket parameter validation.
- Configuration storage.

## Deliverable 4: RocketPy Integration

- Simulation service.
- RocketPy input mapping.
- Simulation execution.
- Simulation error handling.

## Deliverable 5: Simulation Dashboard

- Simulation summary.
- Altitude chart.
- Velocity chart.
- Acceleration chart.

## Deliverable 6: Simulation Comparison

- Select simulation results.
- Compare numerical outputs.
- Display basic comparison chart.

---

# 21. Timeline

Target MVP: 90 Hari

## Phase 1: Foundation

Duration: 1 - 2 Weeks

Scope:

- Project setup.
- Backend setup.
- Frontend setup.
- Database setup.
- Docker setup.
- Initial API structure.

---

## Phase 2: Mission and Configuration

Duration: 2 - 3 Weeks

Scope:

- Mission CRUD.
- Rocket configuration CRUD.
- Database schema.
- Form validation.

---

## Phase 3: Calculator Module

Duration: 1 - 2 Weeks

Scope:

- Delta-V Calculator.
- TWR Calculator.
- Payload Fraction Calculator.
- Mass Ratio Calculator.
- Calculator API.
- Calculator UI.

---

## Phase 4: Simulation Module

Duration: 3 - 4 Weeks

Scope:

- RocketPy integration.
- Simulation service.
- Simulation API.
- Simulation result storage.
- Error handling.

---

## Phase 5: Visualization and Comparison

Duration: 2 - 3 Weeks

Scope:

- Simulation dashboard.
- Plotly charts.
- Simulation detail page.
- Simulation comparison.

---

## Phase 6: Testing and Polish

Duration: 1 - 2 Weeks

Scope:

- API testing.
- UI testing.
- Input validation testing.
- Bug fixing.
- Documentation update.

---

# 22. Recommended Folder Structure

## Backend

```txt
backend/
├── app/
│   ├── main.py
│   ├── core/
│   │   ├── config.py
│   │   └── database.py
│   ├── modules/
│   │   ├── missions/
│   │   │   ├── models.py
│   │   │   ├── schemas.py
│   │   │   ├── routes.py
│   │   │   └── services.py
│   │   ├── rocket_configurations/
│   │   │   ├── models.py
│   │   │   ├── schemas.py
│   │   │   ├── routes.py
│   │   │   └── services.py
│   │   ├── calculators/
│   │   │   ├── schemas.py
│   │   │   ├── routes.py
│   │   │   └── services.py
│   │   └── simulations/
│   │       ├── models.py
│   │       ├── schemas.py
│   │       ├── routes.py
│   │       └── services.py
│   └── shared/
│       ├── exceptions.py
│       └── responses.py
├── alembic/
├── tests/
├── Dockerfile
└── requirements.txt
```

## Frontend

```txt
frontend/
├── src/
│   ├── app/
│   ├── components/
│   ├── features/
│   │   ├── missions/
│   │   ├── rocket-configurations/
│   │   ├── calculators/
│   │   ├── simulations/
│   │   └── comparisons/
│   ├── services/
│   ├── types/
│   └── utils/
├── public/
├── Dockerfile
└── package.json
```

---

# 23. MVP Notes

MVP harus tetap sederhana dan fokus pada satu tujuan utama: user dapat membuat misi, mengisi konfigurasi roket, menjalankan simulasi dasar, melihat hasil numerik, melihat grafik, dan menyimpan hasil simulasi.

Fitur yang terlalu kompleks seperti orbital simulation, multi-stage rocket, weather integration, dan AI assistant tidak boleh dimasukkan ke dalam MVP agar development tetap realistis dalam target 90 hari.

