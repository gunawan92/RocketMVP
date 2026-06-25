# FORMULAS.md

## Document Information

**Project:** Rocket Mission Planner  
**Version:** 1.0 (MVP)  
**Status:** Draft  
**Last Updated:** June 2026  

---

# 1. Purpose

Dokumen ini menjelaskan formula utama yang digunakan pada Rocket Mission Planner untuk kalkulasi dasar roket, simulasi awal, dan interpretasi hasil penerbangan.

FORMULAS.md digunakan sebagai referensi untuk:

- Backend calculation service
- Frontend calculator module
- Validation rule
- Simulation result interpretation
- Dokumentasi teknis untuk developer

---

# 2. Unit Convention

Semua kalkulasi MVP menggunakan satuan SI.

| Parameter | Unit |
|---|---|
| Mass | kilogram (kg) |
| Thrust | Newton (N) |
| Time | second (s) |
| Distance / Altitude | meter (m) |
| Velocity | meter per second (m/s) |
| Acceleration | meter per second squared (m/s²) |
| Specific Impulse | second (s) |

---

# 3. Constants

## Standard Gravity

```text
g0 = 9.80665 m/s²
```

Description:

`g0` adalah standard gravity yang digunakan untuk kalkulasi roket, terutama pada formula Delta-V dan TWR.

---

# 4. Delta-V

## Description

Delta-V adalah perubahan kecepatan maksimum teoretis yang dapat diberikan oleh roket berdasarkan specific impulse, wet mass, dan dry mass.

Formula ini menggunakan Tsiolkovsky Rocket Equation.

## Formula

```text
DeltaV = ISP × g0 × ln(m0 / mf)
```

## Variables

| Variable | Description | Unit |
|---|---|---|
| DeltaV | Total theoretical change in velocity | m/s |
| ISP | Specific Impulse | s |
| g0 | Standard gravity | m/s² |
| m0 | Wet Mass / Initial Mass | kg |
| mf | Dry Mass / Final Mass | kg |
| ln | Natural logarithm | - |

## Input Requirements

- `ISP` must be greater than `0`
- `m0` must be greater than `0`
- `mf` must be greater than `0`
- `m0` must be greater than `mf`

## Output

```text
Delta-V in m/s
```

## Example

```text
ISP = 250 s
m0  = 100 kg
mf  = 50 kg

g0 = 9.80665

DeltaV = 250 × 9.80665 × ln(100 / 50)
DeltaV = 250 × 9.80665 × ln(2)
DeltaV ≈ 1699.6 m/s
```

## Backend Function Suggestion

```python
def calculate_delta_v(isp: float, wet_mass: float, dry_mass: float) -> float:
    pass
```

## Validation Error Cases

| Case | Error Message |
|---|---|
| ISP <= 0 | ISP must be greater than 0 |
| wet_mass <= 0 | Wet mass must be greater than 0 |
| dry_mass <= 0 | Dry mass must be greater than 0 |
| wet_mass <= dry_mass | Wet mass must be greater than dry mass |

---

# 5. Thrust-to-Weight Ratio (TWR)

## Description

TWR adalah rasio antara gaya dorong roket dan berat roket.

TWR digunakan untuk mengetahui apakah roket mampu lepas landas atau tidak.

## Formula

```text
TWR = Thrust / Weight
```

```text
Weight = Mass × g0
```

Sehingga:

```text
TWR = Thrust / (Mass × g0)
```

## Variables

| Variable | Description | Unit |
|---|---|---|
| TWR | Thrust-to-Weight Ratio | dimensionless |
| Thrust | Engine thrust | N |
| Mass | Rocket mass | kg |
| g0 | Standard gravity | m/s² |
| Weight | Rocket weight | N |

## Input Requirements

- `Thrust` must be greater than `0`
- `Mass` must be greater than `0`

## Output

```text
TWR as dimensionless ratio
```

## Interpretation

| TWR Value | Meaning |
|---|---|
| TWR < 1 | Rocket cannot lift off |
| TWR = 1 | Hover condition |
| TWR > 1 | Rocket can ascend |
| TWR > 1.2 | Better practical lift-off margin |

## Example

```text
Thrust = 1500 N
Mass   = 100 kg

g0 = 9.80665

Weight = 100 × 9.80665
Weight = 980.665 N

TWR = 1500 / 980.665
TWR ≈ 1.53
```

## Backend Function Suggestion

```python
def calculate_twr(thrust: float, mass: float) -> float:
    pass
```

## Validation Error Cases

| Case | Error Message |
|---|---|
| thrust <= 0 | Thrust must be greater than 0 |
| mass <= 0 | Mass must be greater than 0 |

---

# 6. Payload Fraction

## Description

Payload Fraction adalah rasio antara massa payload dan total massa roket.

Formula ini digunakan untuk memahami efisiensi desain roket dalam membawa muatan.

## Formula

```text
Payload Fraction = Payload Mass / Total Mass
```

Untuk output dalam persentase:

```text
Payload Fraction (%) = (Payload Mass / Total Mass) × 100
```

## Variables

| Variable | Description | Unit |
|---|---|---|
| Payload Mass | Payload carried by rocket | kg |
| Total Mass | Total rocket mass | kg |
| Payload Fraction | Payload ratio | dimensionless or % |

## Input Requirements

- `Payload Mass` must be greater than or equal to `0`
- `Total Mass` must be greater than `0`
- `Payload Mass` must be less than or equal to `Total Mass`

## Output

```text
Payload fraction as ratio and percentage
```

## Example

```text
Payload Mass = 10 kg
Total Mass   = 100 kg

Payload Fraction = 10 / 100
Payload Fraction = 0.10
Payload Fraction Percentage = 10%
```

## Backend Function Suggestion

```python
def calculate_payload_fraction(payload_mass: float, total_mass: float) -> dict:
    pass
```

Expected response example:

```json
{
  "ratio": 0.1,
  "percentage": 10.0
}
```

## Validation Error Cases

| Case | Error Message |
|---|---|
| payload_mass < 0 | Payload mass cannot be negative |
| total_mass <= 0 | Total mass must be greater than 0 |
| payload_mass > total_mass | Payload mass cannot be greater than total mass |

---

# 7. Mass Ratio

## Description

Mass Ratio adalah perbandingan antara wet mass dan dry mass.

Mass Ratio digunakan dalam kalkulasi Delta-V dan memberikan gambaran seberapa besar propellant dibandingkan struktur akhir roket.

## Formula

```text
Mass Ratio = Wet Mass / Dry Mass
```

## Variables

| Variable | Description | Unit |
|---|---|---|
| Wet Mass | Rocket mass including propellant | kg |
| Dry Mass | Rocket mass without propellant | kg |
| Mass Ratio | Wet mass divided by dry mass | dimensionless |

## Input Requirements

- `Wet Mass` must be greater than `0`
- `Dry Mass` must be greater than `0`
- `Wet Mass` must be greater than `Dry Mass`

## Output

```text
Mass ratio as dimensionless value
```

## Example

```text
Wet Mass = 100 kg
Dry Mass = 50 kg

Mass Ratio = 100 / 50
Mass Ratio = 2.0
```

## Backend Function Suggestion

```python
def calculate_mass_ratio(wet_mass: float, dry_mass: float) -> float:
    pass
```

## Validation Error Cases

| Case | Error Message |
|---|---|
| wet_mass <= 0 | Wet mass must be greater than 0 |
| dry_mass <= 0 | Dry mass must be greater than 0 |
| wet_mass <= dry_mass | Wet mass must be greater than dry mass |

---

# 8. Propellant Mass

## Description

Propellant Mass adalah massa bahan bakar yang tersedia pada roket.

Formula ini berguna untuk menurunkan nilai propellant dari wet mass dan dry mass.

## Formula

```text
Propellant Mass = Wet Mass - Dry Mass
```

## Variables

| Variable | Description | Unit |
|---|---|---|
| Propellant Mass | Fuel / propellant mass | kg |
| Wet Mass | Rocket mass including propellant | kg |
| Dry Mass | Rocket mass without propellant | kg |

## Input Requirements

- `Wet Mass` must be greater than `0`
- `Dry Mass` must be greater than `0`
- `Wet Mass` must be greater than `Dry Mass`

## Output

```text
Propellant mass in kg
```

## Example

```text
Wet Mass = 100 kg
Dry Mass = 50 kg

Propellant Mass = 100 - 50
Propellant Mass = 50 kg
```

## Backend Function Suggestion

```python
def calculate_propellant_mass(wet_mass: float, dry_mass: float) -> float:
    pass
```

---

# 9. Burn Time

## Description

Burn Time adalah estimasi durasi pembakaran mesin berdasarkan propellant mass dan mass flow rate.

## Formula

```text
Burn Time = Propellant Mass / Mass Flow Rate
```

## Variables

| Variable | Description | Unit |
|---|---|---|
| Burn Time | Engine burn duration | s |
| Propellant Mass | Fuel / propellant mass | kg |
| Mass Flow Rate | Propellant consumption rate | kg/s |

## Input Requirements

- `Propellant Mass` must be greater than `0`
- `Mass Flow Rate` must be greater than `0`

## Output

```text
Burn time in seconds
```

## Example

```text
Propellant Mass = 50 kg
Mass Flow Rate  = 2 kg/s

Burn Time = 50 / 2
Burn Time = 25 s
```

## Backend Function Suggestion

```python
def calculate_burn_time(propellant_mass: float, mass_flow_rate: float) -> float:
    pass
```

---

# 10. Mass Flow Rate

## Description

Mass Flow Rate adalah estimasi laju konsumsi propellant berdasarkan thrust dan specific impulse.

## Formula

```text
Mass Flow Rate = Thrust / (ISP × g0)
```

## Variables

| Variable | Description | Unit |
|---|---|---|
| Mass Flow Rate | Propellant consumption rate | kg/s |
| Thrust | Engine thrust | N |
| ISP | Specific Impulse | s |
| g0 | Standard gravity | m/s² |

## Input Requirements

- `Thrust` must be greater than `0`
- `ISP` must be greater than `0`

## Output

```text
Mass flow rate in kg/s
```

## Example

```text
Thrust = 1500 N
ISP    = 250 s

g0 = 9.80665

Mass Flow Rate = 1500 / (250 × 9.80665)
Mass Flow Rate ≈ 0.612 kg/s
```

## Backend Function Suggestion

```python
def calculate_mass_flow_rate(thrust: float, isp: float) -> float:
    pass
```

---

# 11. Initial Acceleration

## Description

Initial Acceleration adalah akselerasi awal roket setelah efek berat dikurangi dari thrust.

Formula ini hanya estimasi sederhana untuk kalkulator MVP, bukan pengganti simulasi fisika lengkap.

## Formula

```text
Initial Acceleration = (Thrust - Weight) / Mass
```

Karena:

```text
Weight = Mass × g0
```

Maka:

```text
Initial Acceleration = (Thrust - (Mass × g0)) / Mass
```

## Variables

| Variable | Description | Unit |
|---|---|---|
| Initial Acceleration | Net upward acceleration | m/s² |
| Thrust | Engine thrust | N |
| Weight | Rocket weight | N |
| Mass | Rocket mass | kg |
| g0 | Standard gravity | m/s² |

## Input Requirements

- `Thrust` must be greater than `0`
- `Mass` must be greater than `0`

## Output

```text
Initial acceleration in m/s²
```

## Interpretation

| Value | Meaning |
|---|---|
| < 0 | Rocket cannot lift off |
| = 0 | Hover condition |
| > 0 | Rocket can accelerate upward |

## Example

```text
Thrust = 1500 N
Mass   = 100 kg

g0 = 9.80665

Initial Acceleration = (1500 - (100 × 9.80665)) / 100
Initial Acceleration = (1500 - 980.665) / 100
Initial Acceleration ≈ 5.19 m/s²
```

## Backend Function Suggestion

```python
def calculate_initial_acceleration(thrust: float, mass: float) -> float:
    pass
```

---

# 12. Apogee

## Description

Apogee adalah ketinggian maksimum yang dicapai oleh roket selama penerbangan.

Pada MVP, nilai apogee tidak dihitung menggunakan formula sederhana, melainkan diambil dari hasil simulasi RocketPy.

## Source

```text
RocketPy Flight Simulation
```

## Output

```text
Maximum altitude in meter
```

## Unit

```text
m
```

## Notes

Apogee dipengaruhi oleh banyak faktor, termasuk:

- Thrust curve
- Rocket mass
- Drag coefficient
- Diameter roket
- Rail length
- Launch angle
- Wind condition
- Air density
- Motor burn time

Karena itu, kalkulasi manual sederhana tidak direkomendasikan untuk hasil final.

---

# 13. Max Velocity

## Description

Max Velocity adalah kecepatan maksimum yang dicapai roket selama penerbangan.

Pada MVP, nilai ini diambil dari hasil simulasi RocketPy.

## Source

```text
RocketPy Flight Simulation
```

## Output

```text
Maximum velocity in m/s
```

## Unit

```text
m/s
```

---

# 14. Max Acceleration

## Description

Max Acceleration adalah akselerasi maksimum yang dialami roket selama penerbangan.

Pada MVP, nilai ini diambil dari hasil simulasi RocketPy.

## Source

```text
RocketPy Flight Simulation
```

## Output

```text
Maximum acceleration in m/s²
```

## Unit

```text
m/s²
```

---

# 15. Flight Duration

## Description

Flight Duration adalah total durasi penerbangan dari launch sampai landing atau akhir simulasi.

Pada MVP, nilai ini diambil dari hasil simulasi RocketPy.

## Source

```text
RocketPy Flight Simulation
```

## Output

```text
Flight duration in seconds
```

## Unit

```text
s
```

---

# 16. Recommended Calculator Output Format

Backend disarankan mengembalikan hasil kalkulasi dalam format konsisten seperti berikut:

```json
{
  "input": {
    "isp": 250,
    "wet_mass": 100,
    "dry_mass": 50
  },
  "result": {
    "delta_v": 1699.6,
    "unit": "m/s"
  },
  "interpretation": "Rocket has theoretical Delta-V of 1699.6 m/s.",
  "warnings": []
}
```

---

# 17. Validation Rules Summary

| Field | Rule |
|---|---|
| ISP | Must be greater than 0 |
| Wet Mass | Must be greater than 0 |
| Dry Mass | Must be greater than 0 |
| Wet Mass vs Dry Mass | Wet Mass must be greater than Dry Mass |
| Total Mass | Must be greater than 0 |
| Payload Mass | Must be 0 or greater |
| Payload vs Total Mass | Payload Mass cannot be greater than Total Mass |
| Thrust | Must be greater than 0 |
| Mass Flow Rate | Must be greater than 0 |

---

# 18. MVP Formula List

Formula yang masuk MVP:

- Delta-V
- TWR
- Payload Fraction
- Mass Ratio
- Propellant Mass
- Burn Time
- Mass Flow Rate
- Initial Acceleration
- Apogee from RocketPy
- Max Velocity from RocketPy
- Max Acceleration from RocketPy
- Flight Duration from RocketPy

---

# 19. Out of Scope Formula for MVP

Formula berikut tidak masuk MVP:

- Orbital velocity
- Hohmann transfer
- Escape velocity
- Re-entry heating
- Aerodynamic drag manual model
- CFD model
- Multi-stage Delta-V
- Gravity turn optimization
- Interplanetary transfer

---

# 20. Implementation Notes

## Backend

- Semua formula kalkulator dasar sebaiknya ditempatkan dalam module terpisah.
- Hindari mencampur formula dengan route/controller.
- Gunakan type hint untuk semua function.
- Gunakan unit test untuk setiap formula.
- Semua input harus divalidasi sebelum kalkulasi.

Suggested structure:

```text
app/
  calculators/
    delta_v.py
    twr.py
    payload_fraction.py
    mass_ratio.py
    propellant.py
    burn_time.py
    mass_flow_rate.py
    acceleration.py
```

## Frontend

- Tampilkan unit pada setiap input.
- Tampilkan pesan error yang jelas.
- Tampilkan interpretasi hasil, bukan hanya angka.
- Format angka maksimal 2 sampai 4 digit desimal.

## Database

Simpan input dan output kalkulasi untuk kebutuhan mission history.

Suggested fields:

```text
id
mission_id
calculator_type
input_json
result_json
created_at
```

---

# 21. Testing Checklist

## Delta-V

- Should calculate Delta-V correctly when inputs are valid.
- Should reject ISP <= 0.
- Should reject wet_mass <= dry_mass.
- Should reject negative mass.

## TWR

- Should calculate TWR correctly.
- Should return TWR < 1 when thrust is lower than weight.
- Should reject mass <= 0.
- Should reject thrust <= 0.

## Payload Fraction

- Should calculate ratio and percentage.
- Should allow payload_mass = 0.
- Should reject payload_mass > total_mass.

## Mass Ratio

- Should calculate wet_mass / dry_mass correctly.
- Should reject wet_mass <= dry_mass.

## RocketPy Result

- Should return apogee.
- Should return max velocity.
- Should return max acceleration.
- Should return flight duration.
- Should handle simulation failure gracefully.

---

# 22. Notes for Future Versions

Untuk versi setelah MVP, formula dapat diperluas dengan:

- Multi-stage Delta-V calculation
- Orbital mechanics
- Hohmann transfer
- Escape velocity
- Launch window estimation
- Atmospheric drag modeling
- Wind correction model
- Landing prediction
- Reusable rocket descent calculation

