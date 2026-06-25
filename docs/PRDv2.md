PRODUCT REQUIREMENT DOCUMENT (PRD) V2

Rocket Mission Planner - Educational Game Edition

Version: 2.0

Status: Draft

Owner: Gunawan WP

Platform:

- Flutter (STELA Ecosystem)
- FastAPI Backend
- Physics Engine
- Future Unity Visualization

Target Audience:

- SMP
- SMA
- Guru IPA
- Guru Fisika
- STEM Club

---

1. Product Vision

Rocket Mission Planner adalah game edukasi berbasis eksperimen yang mengajarkan konsep fisika, rekayasa, dan pemecahan masalah melalui simulasi roket yang interaktif.

Siswa tidak diminta menghafal rumus.

Siswa belajar melalui:

- mencoba
- gagal
- memperbaiki desain
- mencoba kembali

Tujuan utama bukan memenangkan game, tetapi memahami hubungan sebab-akibat dalam desain roket.

---

2. Educational Philosophy

Prinsip utama:

Learning By Experiment

Bukan:

"Hafalkan rumus"

Tetapi:

"Apa yang terjadi jika bahan bakar ditambah?"

"Apa yang terjadi jika sirip diperkecil?"

"Apa yang terjadi jika payload diperbesar?"

Siswa menemukan konsep fisika melalui simulasi.

---

3. Learning Outcomes

SMP

Siswa memahami:

- gaya dorong
- massa
- gravitasi
- hambatan udara
- kestabilan dasar

---

SMA

Siswa memahami:

- thrust to weight ratio
- efisiensi bahan bakar
- aerodinamika dasar
- multi-stage rocket
- konsep orbit dasar

---

4. Core Gameplay Loop

Player memilih misi

↓

Merakit roket

↓

Menjalankan simulasi

↓

Melihat hasil

↓

Menganalisis kegagalan

↓

Memperbaiki desain

↓

Mencoba lagi

---

5. Game Modes

Mode 1

Rocket Sandbox

Tujuan:

Eksperimen bebas

Tidak ada target

Tidak ada skor

---

Mode 2

Mission Challenge

Contoh:

Capai 1 Km

Capai 10 Km

Capai 50 Km

Capai 100 Km

Masuk Orbit

---

Mode 3

Classroom Mode

Digunakan guru.

Guru dapat memberikan:

- target misi
- batas bahan bakar
- batas payload

---

6. Rocket Builder

Ini adalah fitur utama.

Player membangun roket menggunakan slider dan pilihan visual.

---

7. Adjustable Parameters

7.1 Rocket Height

Nama UI:

Tinggi Roket

Range:

5 m - 50 m

Efek:

- kapasitas bahan bakar bertambah
- massa bertambah
- drag bertambah

---

7.2 Rocket Diameter

Nama UI:

Diameter Roket

Range:

0.5 m - 5 m

Efek:

- stabilitas meningkat
- hambatan udara meningkat

---

7.3 Nose Cone

Pilihan:

- Pendek
- Sedang
- Lancip

Efek:

- drag berubah
- stabilitas berubah

---

7.4 Fin Size

Pilihan:

- Kecil
- Sedang
- Besar

Efek:

- kestabilan berubah
- massa berubah

---

7.5 Payload

Pilihan:

5 Kg

10 Kg

25 Kg

50 Kg

100 Kg

Efek:

- massa meningkat
- kebutuhan bahan bakar meningkat

---

8. Engine System

Player tidak melihat istilah teknis kompleks.

Pilihan:

Engine A

Engine B

Engine C

Engine D

Backend:

masing-masing memiliki:

- thrust
- isp
- burn duration

---

9. Fuel System

Sistem ini menjadi fitur unggulan.

---

Single Stage

Visual:

[ Fuel Tank ]

---

Two Stage

Visual:

[ Stage 1 ]
Fuel %

[ Stage 2 ]
Fuel %

---

Three Stage

Visual:

[ Stage 1 ]
Fuel %

[ Stage 2 ]
Fuel %

[ Stage 3 ]
Fuel %

---

Learning Outcome:

Siswa memahami:

- mengapa roket bertingkat digunakan
- efisiensi multi-stage

---

10. Weather System

Pilihan:

☀ Cerah

🌤 Berawan

💨 Berangin

⛈ Badai

Variabel:

- wind speed
- turbulence

---

11. Mission Objectives

Contoh:

---

Mission 1

Target:

1 Km

Reward:

Basic Engine

---

Mission 2

Target:

10 Km

Reward:

Medium Engine

---

Mission 3

Target:

50 Km

Reward:

Advanced Fuel Tank

---

Mission 4

Target:

100 Km

Reward:

Large Payload Bay

---

12. Success Conditions

Mission dianggap berhasil jika:

- mencapai target ketinggian
- payload selamat
- tidak mengalami kegagalan kritis

---

13. Failure Engine

Game harus menjelaskan penyebab kegagalan.

---

Failure 1

Rocket Too Heavy

Pesan:

Mesin tidak cukup kuat mengangkat roket.

---

Failure 2

Fuel Exhausted

Pesan:

Bahan bakar habis sebelum target tercapai.

---

Failure 3

Unstable Flight

Pesan:

Sirip terlalu kecil untuk ukuran roket.

---

Failure 4

Strong Wind

Pesan:

Angin terlalu kuat sehingga roket keluar jalur.

---

Failure 5

Structural Failure

Pesan:

Roket mengalami kerusakan akibat beban berlebih.

---

Failure 6

Stage Separation Failure

Pesan:

Tahap berikutnya gagal aktif.

---

Failure 7

Payload Failure

Pesan:

Payload gagal mencapai tujuan.

---

14. Simulation Result Screen

Menampilkan:

Ketinggian Maksimum

Kecepatan Maksimum

Durasi Terbang

Status Misi

---

Visual:

Grafik lintasan

Grafik kecepatan

Grafik ketinggian

---

15. Scoring System

Skor dihitung dari:

40% Mission Success

25% Fuel Efficiency

20% Payload Delivery

15% Stability

---

Rating:

⭐

⭐⭐

⭐⭐⭐

⭐⭐⭐⭐

⭐⭐⭐⭐⭐

---

16. Teacher Features (Future)

Guru dapat:

- membuat tantangan
- melihat hasil siswa
- membandingkan desain

---

17. Technology Architecture

Frontend:

Flutter (STELA)

Backend:

FastAPI

Physics Layer:

Rocket Physics Engine

Advanced Layer:

RocketPy

Database:

PostgreSQL

Charts:

Plotly

Future:

Unity Visualization

---

18. MVP Scope

Included:

✓ Rocket Builder

✓ Mission Challenge

✓ Failure Engine

✓ Altitude Simulation

✓ Fuel Simulation

✓ Weather Simulation

✓ Result Dashboard

Not Included:

✗ Multiplayer

✗ Real Orbital Mechanics

✗ Moon Mission

✗ Mars Mission

✗ Real-Time Weather

✗ Complex Aerospace Modeling

---

19. Success Metric

Siswa mampu:

- memahami hubungan massa dan gaya dorong
- memahami fungsi bahan bakar
- memahami fungsi sirip
- memahami konsep kestabilan
- memahami mengapa desain tertentu gagal

tanpa harus menghafal rumus fisika terlebih dahulu.