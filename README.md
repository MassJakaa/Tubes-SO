# Tugas Besar Sistem Operasi: Keamanan Sistem Operasi (Tema D)

[![Sistem Operasi](https://img.shields.io/badge/Mata%20Kuliah-Sistem%20Operasi-blue.svg)](https://github.com/MassJakaa)
[![Theme](https://img.shields.io/badge/Tema%20D-OS%20Hardening%20%26%20Security%20Audit-emerald.svg)](https://github.com/MassJakaa)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Repositori resmi pengerjaan **Tugas Besar Mata Kuliah Sistem Operasi - Tema D: Keamanan Sistem Operasi (OS Hardening & Security Audit)**.

Proyek ini mendemonstrasikan evaluasi keamanan komparatif antara sistem Linux *default* (Unhardened) dan sistem yang telah diterapkan *hardening* berbasis **CIS Benchmark** serta dilengkapi **CyberShield SOC Web Dashboard** untuk monitoring visual multi-node.

---

## 👥 Anggota Kelompok
1. **Rafi Dzaka Pratama P** (NIM: 123240104) &ndash; *Project Lead & Hardening Engineer*
2. **Aushaf Fathin Irsyad Nabil** (NIM: 123240092) &ndash; *Red Team Penetration Tester*
3. [Nama Anggota 3] (NIM: [NIM 3]) &ndash; *Baseline Engineer*
4. **Muhammad Wafa Akmal** (NIM: 123240113) &ndash; *SIEM & Monitoring Engineer*

---

## 🏗️ Arsitektur Jaringan Multi-Node (4 Laptop)

Semua laptop terhubung dalam satu jaringan Wi-Fi lokal:

| Node | Peran Sistem | Hostname & OS | Tugas & Layanan Utama | Web Dashboard |
| :---: | :--- | :--- | :--- | :---: |
| **Node 1** | **Attacker (Red Team)** | `kali-attacker` (Kali/Ubuntu) | Nmap Port Scan, Hydra SSH Brute Force, Ping Test | `http://<IP>:5000?role=1` |
| **Node 2** | **Hardened Target (Blue Team)** | `target-hardened` (Ubuntu 22.04) | UFW Firewall, Fail2ban Auto-Ban, SSH Hardening, Lynis Audit | `http://<IP>:5000?role=2` |
| **Node 3** | **Unhardened Target (Baseline)** | `target-unhardened` (Ubuntu 22.04) | OpenSSH Default (Tanpa Firewall, Kontrol Pembanding) | `http://<IP>:5000?role=3` |
| **Node 4** | **SIEM & Central Monitoring** | `siem-monitor` (Ubuntu 22.04) | Rsyslog Central Collector, Live Threat Monitoring | `http://<IP>:5000?role=4` |

---

## 📂 Struktur Direktori

```text
Tugas_Besar_Keamanan_OS/
│
├── dashboard/                                  <-- CyberShield SOC Web Dashboard (Flask + Chart.js)
│   ├── templates/index.html                    <-- Frontend Web Dashboard Multi-Node
│   ├── app.py                                  <-- Backend REST API & Log Parser
│   └── run_dashboard.sh                        <-- Skrip peluncur dashboard otomatis
│
├── scripts/                                    <-- Skrip Otomasi Pengujian Sistem Operasi
│   ├── 01_unhardened_target_setup.sh           <-- Setup Node 3 (Baseline Unhardened)
│   ├── 02_hardened_target_setup.sh             <-- Setup Node 2 (Hardened Defense)
│   ├── 03_attacker_suite.sh                    <-- Suite Serangan Node 1 (Nmap & Hydra)
│   ├── 04_siem_collector_setup.sh              <-- Setup Node 4 (Rsyslog Collector)
│   ├── 05_audit_comparator.sh                  <-- Ekstraktor Perbandingan Skor Lynis
│   └── setup_kali_tools.sh                     <-- Skrip instalasi tools attacker
│
├── Laporan_Akhir_Tugas_Besar_Keamanan_OS.docx  <-- Laporan format Word resmi siap kumpul
├── Laporan_Akhir_Tugas_Besar_Keamanan_OS.md    <-- Naskah sumber laporan Markdown
├── Panduan_Lengkap_Tugas_Besar_Keamanan_OS.pdf <-- Buku panduan praktikum step-by-step
└── generate_report_docx.py                     <-- Generator laporan Word otomatis
```

---

## 📊 Hasil Evaluasi & Temuan Kuantitatif

Berdasarkan pengujian empiris yang telah dilakukan:

| Parameter Pengujian | Node 3 (Unhardened) | Node 2 (Hardened) | Evaluasi & Status |
| :--- | :---: | :---: | :--- |
| **Hardening Index (Lynis)** | **55 / 100** | **84 / 100** | **Meningkat +29 Poin (+52.7%)** |
| **Security Warnings** | 38 Temuan Kritis | 6 Temuan | Berkurang 32 kerentanan |
| **Security Suggestions** | 95 Rekomendasi | 24 Rekomendasi | Berkurang 71 rekomendasi |
| **Firewall (UFW)** | Inactive / Disabled | Active (Port 22 & 80) | Port lain ditutup total (*Filtered*) |
| **SSH Brute Force (Hydra)** | **COMPROMISED (Tembus)** | **BLOCKED (Auto-Ban)** | IP Penyerang di-ban otomatis (< 5 detik) |
| **Audit Log Monitoring** | Tersimpan di `/var/log/auth.log` | Diteruskan ke SIEM Node 4 | Alert terpicu secara *real-time* |

---

## 🚀 Panduan Menjalankan Sistem

### 1. Di Laptop Target Hardened (Node 2):
```bash
sudo bash scripts/02_hardened_target_setup.sh
```

### 2. Di Laptop Target Unhardened (Node 3):
```bash
sudo bash scripts/01_unhardened_target_setup.sh
```

### 3. Di Laptop Penyerang (Node 1):
```bash
chmod +x scripts/03_attacker_suite.sh
./scripts/03_attacker_suite.sh
```

### 4. Menyalakan Web Dashboard Visual (Semua Laptop):
```bash
cd dashboard
bash run_dashboard.sh [1|2|3|4]
```
Buka browser di: `http://<IP_LAPTOP>:5000`

---

## 📄 Lisensi
Hak Cipta &copy; 2026/2027 Kelompok Sistem Operasi. Dirilis di bawah lisensi MIT.
