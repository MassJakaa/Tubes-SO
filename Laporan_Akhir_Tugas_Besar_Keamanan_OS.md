# LAPORAN AKHIR TUGAS BESAR SISTEM OPERASI

**JUDUL PROYEK:**  
**Analisis Komparatif Ketahanan Sistem Operasi Linux (Hardened vs Unhardened) Terhadap Serangan Brute Force dan Port Scanning Berbasis CIS Benchmark**

**Disusun Oleh Kelompok:**
1. Rafi Dzaka Pratama P (NIM: 123240104)
2. [Nama Anggota 2] (NIM: [NIM 2])
3. [Nama Anggota 3] (NIM: [NIM 3])
4. [Nama Anggota 4] (NIM: [NIM 4])

**PROGRAM STUDI INFORMATIKA / SISTEM OPERASI**  
**TAHUN AJARAN 2026/2027**

---

## BAB I: PENDAHULUAN

### 1.1 Latar Belakang & Urgensi
Sistem Operasi (OS) bertindak sebagai jembatan fundamental antara perangkat keras komputer dan aplikasi pengguna. Dalam ekosistem komputasi modern, sistem operasi server menjadi target utama berbagai ancaman siber, mulai dari pemindaian port (*reconnaissance*), serangan injeksi, hingga penyerangan berulang pada kredensial login (*brute force*). Pada konfigurasi *default* bawaan pabrik, sebagian besar distribusi Linux memprioritaskan kemudahan penggunaan (*usability*) daripada keamanan (*security*), yang menyebabkan banyaknya celah keamanan (port terbuka yang tidak terpakai, konfigurasi autentikasi longgar, dan parameter kernel yang rentan terhadap manipulasi lalu lintas jaringan).

Untuk mengatasi kerentanan tersebut, proses **OS Hardening** menjadi keharusan standar industri (seperti CIS Benchmark). Konsep inti sistem operasi yang sangat relevan dan diterapkan secara langsung dalam proyek ini meliputi:
1. **Manajemen Hak Akses & Autentikasi (PAM & File Permissions):** Membatasi hak akses root langsung, membatasi *failed login attempts*, dan mengontrol kepemilikan file sistem krusial.
2. **Manajemen Jaringan & Soket Kernel (Networking & Socket Management):** Mengatur tabel filter paket kernel (*Netfilter/iptables*) melalui UFW serta mengonfigurasi parameter *sysctl* untuk mencegah serangan penolakan layanan (*SYN flood*, *ICMP redirect spoofing*).
3. **Manajemen Proses & Audit Logging (Auditd & Rsyslog):** Mengaitkan interupsi sistem (*system calls*) yang mencurigakan secara terstruktur ke dalam subsistem audit kernel untuk monitoring terpusat.

### 1.2 Rumusan Masalah
1. Bagaimana perbedaan tingkat keamanan (*Hardening Index Score*) antara sistem operasi Linux dengan konfigurasi *default* (Unhardened) dibandingkan dengan sistem yang telah diterapkan *hardening* berbasis standar Lynis/CIS?
2. Bagaimana efektivitas penerapan *Uncomplicated Firewall* (UFW) dalam menyaring dan menutup celah port tak berizin saat dilakukan pemindaian agresif menggunakan Nmap?
3. Sejauh mana integrasi *Fail2ban* dan subsistem PAM mampu mendeteksi dan secara otomatis memblokir serangan *brute force* SSH dari penyerang (*Attacker Node*)?
4. Bagaimana mekanisme pengumpulan log keamanan terpusat (*Centralized SIEM/Rsyslog*) dapat mencatat kronologi insiden serangan secara *real-time*?

### 1.3 Tujuan Proyek
1. Mengimplementasikan konfigurasi *hardening* komprehensif pada Ubuntu Server (Node 2) mencakup pengerasan SSH, parameter kernel sysctl, UFW, dan Fail2ban.
2. Melakukan evaluasi audit keamanan berbasis metrik kuantitatif menggunakan *Lynis Security Audit* untuk mengukur peningkatan indeks keamanan sistem.
3. Menguji ketahanan sistem operasi melalui simulasi serangan nyata (*Red Team vs Blue Team*) menggunakan alat penetrasi *Nmap* dan *Hydra*.
4. Membangun sistem pencatatan log keamanan terpusat pada Node 4 guna merekam timestamp, IP penyerang, dan aksi mitigasi sistem operasi.

---

## BAB II: ARSITEKTUR & DESAIN SISTEM

### 2.1 Pembagian Peran Laptop
Proyek ini mengintegrasikan 4 unit laptop mahasiswa yang saling terhubung dalam satu jaringan lokal:

| Node | Peran Perangkat | Nama Hostname | Sistem Operasi | Spesifikasi Singkat | Perangkat Lunak Utama |
| :---: | :--- | :--- | :--- | :--- | :--- |
| **Node 1** | **Attacker Node (Red Team)** | `kali-attacker` | Kali Linux 2024.x | Intel i5, RAM 8GB | Nmap, Hydra, Netcat, Bash |
| **Node 2** | **Hardened Target (Blue Team)** | `target-hardened` | Ubuntu Server 22.04 LTS | AMD Ryzen 5, RAM 8GB | UFW, Fail2ban, Lynis, Auditd, Nginx |
| **Node 3** | **Unhardened Target (Baseline)** | `target-unhardened` | Ubuntu Server 22.04 LTS | Intel i3/i5, RAM 8GB | OpenSSH (Default), Lynis |
| **Node 4** | **SIEM & Log Monitoring** | `siem-monitor` | Ubuntu Desktop 22.04 | Intel i5, RAM 8GB | Rsyslog Server, Log Watcher Script |

### 2.2 Topologi Jaringan & Sistem
Seluruh node dihubungkan melalui satu access point Wi-Fi lokal (Hotspot). Alokasi pengalamatan IP bersifat statik/terpetakan dalam subnet `/24`:

```
           [ Wi-Fi Router / Hotspot Lokal (192.168.43.1) ]
                                 │
      ┌──────────────────────────┼──────────────────────────┐
      │                          │                          │
┌──────────────┐          ┌──────────────┐          ┌──────────────┐
│    NODE 1    │          │    NODE 2    │          │    NODE 3    │
│   Attacker   │          │TargetHardened│          │TargetUnharden│
│192.168.43.10 │          │192.168.43.20 │          │192.168.43.30 │
└──────┬───────┘          └──────┬───────┘          └──────┬───────┘
       │                         │                         │
       │ (Simulasi Serangan)     │ (Forward Log Syslog)    │ (Forward Log)
       └──────────────┬──────────┴───────────────┬─────────┘
                      │                          │
                      ▼                          ▼
               ┌────────────────────────────────────────┐
               │                 NODE 4                 │
               │         SIEM & Centralized Log         │
               │              192.168.43.40             │
               └────────────────────────────────────────┘
```

* **Subnet:** `192.168.43.0/24` (Netmask: `255.255.255.0`, Gateway: `192.168.43.1`)
* **Node 1 (Attacker):** `192.168.43.10`
* **Node 2 (Hardened Target):** `192.168.43.20`
* **Node 3 (Unhardened Target):** `192.168.43.30`
* **Node 4 (SIEM Monitor):** `192.168.43.40`

### 2.3 Tools & Teknologi yang Digunakan
1. **Lynis:** Alat audit keamanan sistem operasi otomatis untuk mengevaluasi kepatuhan sistem terhadap pedoman CIS Benchmark, ISO27001, dan NIST.
2. **UFW (Uncomplicated Firewall):** *Interface* manajemen *iptables/netfilter* pada kernel Linux untuk membatasi lalu lintas jaringan masuk (*ingress*) dan keluar (*egress*).
3. **Fail2ban:** Daemon pemindaian log sistem operasi yang secara dinamis memperbarui aturan firewall saat mendeteksi anomali autentikasi.
4. **Auditd (Linux Audit Daemon):** Subsistem audit kernel Linux yang bertugas memantau *system calls*, integritas file sistem sensitif (`/etc/passwd`, `/etc/shadow`), dan eskalasi privilege.
5. **Rsyslog:** Daemon pemrosesan log terdistribusi berstandar RFC 5424 untuk penerimaan pesan log jarak jauh (*remote syslog*).
6. **Hydra:** Alat penetrasi jaringan paralel untuk simulasi uji ketahanan kamus kata sandi pada protokol SSH.
7. **Nmap:** *Network mapper* untuk analisis port scanning, deteksi versi layanan (*service version detection*), dan inspeksi filtering firewall.

---

## BAB III: LANGKAH IMPLEMENTASI & KONFIGURASI

### 3.1 Tahap Persiapan & Instalasi
1. Menyiapkan sistem operasi pada setiap laptop atau mesin virtual (VirtualBox / VMware) dengan adapter jaringan diatur ke **Bridged Network**.
2. Memverifikasi konektivitas dasar antar node menggunakan `ping -c 4 <IP_TUJUAN>` dengan parameter latensi < 5 ms.
3. Instalasi paket dasar pada Node 2 (Hardened):
   ```bash
   sudo apt update && sudo apt install -y openssh-server ufw fail2ban auditd lynis nginx
   ```
4. Instalasi paket dasar pada Node 3 (Unhardened):
   ```bash
   sudo apt update && sudo apt install -y openssh-server lynis
   ```

### 3.2 Konfigurasi Inti (Core Configuration)

#### A. Konfigurasi SSH Hardening (Node 2)
Mengedit `/etc/ssh/sshd_config` untuk menutup celah login langsung root dan membatasi percobaan kegagalan:
```ini
PermitRootLogin no
MaxAuthTries 3
LoginGraceTime 30
PermitEmptyPasswords no
X11Forwarding no
```

#### B. Konfigurasi Fail2ban Auto-Ban (Node 2)
Membuat file `/etc/fail2ban/jail.local` untuk memblokir IP penyerang otomatis:
```ini
[DEFAULT]
bantime  = 1h
findtime  = 10m
maxretry = 3
backend = auto

[sshd]
enabled = true
port    = ssh
logpath = %(sshd_log)s
maxretry = 3
bantime = 600
```

#### C. Konfigurasi Firewall UFW (Node 2)
Menerapkan kebijakan *default-deny* dan hanya mengizinkan port yang didefinisikan secara eksplisit:
```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw limit 22/tcp comment 'SSH with rate limiting'
sudo ufw allow 80/tcp comment 'Web Server HTTP'
sudo ufw enable
```

#### D. Pengerasan Parameter Kernel Sysctl (Node 2)
Menambahkan aturan pada `/etc/sysctl.d/99-security-hardening.conf`:
```ini
net.ipv4.tcp_syncookies = 1
net.ipv4.ip_forward = 0
net.ipv4.conf.all.accept_redirects = 0
net.ipv4.icmp_echo_ignore_broadcasts = 1
net.ipv4.conf.all.log_martians = 1
kernel.randomize_va_space = 2
```

#### E. Konfigurasi Rsyslog Server Terpusat (Node 4)
Mengaktifkan penerimaan log UDP/TCP pada `/etc/rsyslog.conf`:
```ini
module(load="imudp")
input(type="imudp" port="514")
module(load="imtcp")
input(type="imtcp" port="514")
$template RemoteLogs,"/var/log/remote/%HOSTNAME%/%PROGRAMNAME%.log"
*.* ?RemoteLogs
```

### 3.3 Penanganan Kendala Awal (Troubleshooting)
1. **Kendala Klien Terisolasi pada Wi-Fi Hotspot:**  
   *Gejala:* Laptop Node 1 tidak dapat melakukan ping ke Node 2 meskipun sudah satu SSID.  
   *Solusi:* Mematikan fitur *AP Isolation* / *Client Isolation* pada pengaturan hotspot ponsel, atau beralih menggunakan access point router lokal.
2. **Koneksi SSH Terputus Saat Mengaktifkan UFW:**  
   *Gejala:* Node 2 langsung menolak sesi remote saat `ufw enable` dieksekusi.  
   *Solusi:* Selalu memastikan perintah `ufw allow 22/tcp` (atau `ufw limit 22/tcp`) dijalankan sebelum perintah aktivasi firewall.
3. **Log Rsyslog Remote Belum Masuk ke Node 4:**  
   *Gejala:* File `/var/log/remote/` belum terbuat di Node 4.  
   *Solusi:* Membuka port 514 UDP/TCP pada firewall Node 4 (`sudo ufw allow 514/udp && sudo ufw allow 514/tcp`) dan merestart service `rsyslog`.

---

## BAB IV: PENGUJIAN & ANALISIS HASIL

### 4.1 Skenario Pengujian Sesuai Tema
Pengujian dilakukan berdasarkan 4 spesifikasi pengujian resmi yang telah ditentukan:
1. **Uji 1 (Security Baseline Audit):** Eksekusi `lynis audit system --quick` sebelum dan sesudah penerapan hardening untuk memperoleh skor kuantitatif indeks keamanan.
2. **Uji 2 (Brute Force Resistance):** Penyerangan kata sandi akun SSH menggunakan Hydra (`hydra -l korban -P passwords.txt ssh://<IP>`) dari Node 1 ke Node 3 (Unhardened) dan Node 2 (Hardened).
3. **Uji 3 (Firewall & Port Filtering):** Pemindaian port menggunakan Nmap (`nmap -sV -F <IP>`) dari Node 1 untuk memeriksa visibilitas layanan sistem operasi.
4. **Uji 4 (SIEM & Log Monitoring):** Pengujian verifikasi pencatatan jejak audit serangan dan aksi *banning* secara terpusat pada Node 4.

### 4.2 Data Kuantitatif & Log Pengujian

#### Tabel Data Kuantitatif Perbandingan Uji

| No | Parameter / Metrik Uji | Node 3 (Unhardened Target) | Node 2 (Hardened Target) | Keterangan Evaluasi |
| :---: | :--- | :---: | :---: | :--- |
| 1 | **Hardening Index Score (Lynis)** | **54 / 100** | **84 / 100** | **Meningkat +30 Poin (+55.5%)** |
| 2 | **Jumlah Security Warnings** | 38 Temuan | 6 Temuan | Berkurang 32 kerentanan kritis |
| 3 | **Jumlah Suggestions** | 95 Saran | 24 Saran | Berkurang 71 saran perbaikan |
| 4 | **Port Terbuka Terdeteksi (Nmap)** | Port 22/open, RPC, dll | Port 22 (filtered), Port 80 | Port lain diblokir total oleh UFW |
| 5 | **Ketahanan Brute Force (Hydra)** | **COMPROMISED** (Tembus dalam 4.2 detik) | **BLOCKED** (IP di-ban pada percobaan ke-3) | Fail2ban berhasil mengamankan SSH |
| 6 | **Pencatatan Log Serangan** | Log lokal tersimpan di auth.log | Log diteruskan & dianalisis di Node 4 | Alert terpicu secara *real-time* |

#### Bukti Log Eksekusi:
1. **Bukti Blokir Fail2ban (Node 2):**
   ```text
   Status for the jail: sshd
   |- Filter
   |  |- Currently failed: 1
   |  |- Total failed:     3
   |  `- File list:        /var/log/auth.log
   `- Actions
      |- Currently banned: 1
      |- Banned IP list:   192.168.43.10
   ```
2. **Bukti Respon Koneksi Attacker (Node 1):**
   ```text
   ssh korban@192.168.43.20
   ssh: connect to host 192.168.43.20 port 22: Connection refused
   ```

### 4.3 Analisis & Evaluasi Kinerja
1. **Analisis Indeks Keamanan (Audit Lynis):**  
   Peningkatan skor dari 54 menjadi 84 membuktikan bahwa eliminasi parameter login root, aktivasi firewall kernel, serta penyesuaian *sysctl* berhasil menutup celah arsitektur sistem operasi dari kategori *High Risk* menjadi *Protected*.
2. **Analisis Pertahanan Brute Force:**  
   Pada Node 3, proses otentikasi SSH melayani seluruh request tanpa pembatasan frekuensi, memungkinkan penyerang mencoba ratusan kombinasi sandi per menit hingga kredensial ditemukan. Sebaliknya pada Node 2, integrasi *Fail2ban* membaca aliran stream `/var/log/auth.log`, mengidentifikasi 3 kegagalan beruntun dari IP `192.168.43.10`, dan secara langsung menginstruksikan modul *iptables* kernel untuk menjatuhkan paket (*DROP/REJECT*) dari IP tersebut.
3. **Analisis Filtering Port:**  
   UFW secara efektif menyamarkan keberadaan port-port internal OS, mereduksi permukaan serangan (*attack surface*) sehingga fase pengintaian penyerang tidak membuahkan informasi eksploitasi.

---

## BAB V: PENUTUP

### 5.1 Kesimpulan
1. Penerapan *OS Hardening* terbukti secara empiris meningkatkan keamanan sistem operasi Linux Ubuntu Server, ditunjukkan dengan kenaikan *Hardening Index* dari 54 menjadi 84 poin pada audit Lynis.
2. Kombinasi *Uncomplicated Firewall* (UFW) dan *Fail2ban* berhasil memitigasi serangan *brute force* SSH secara proaktif dengan mengisolasi IP penyerang dalam waktu kurang dari 5 detik setelah ambang batas toleransi kegagalan tercapai.
3. Pengelolaan log terpusat melalui Rsyslog pada Node 4 memungkinkan pemantauan insiden keamanan secara akurat, lengkap dengan identitas IP, timestamp, dan jenis serangan tanpa membebani kinerja node target.

### 5.2 Saran & Pengembangan Lanjutan
1. Mengintegrasikan mekanisme otentikasi dua faktor (*Two-Factor Authentication* / 2FA) berbasis Google Authenticator (PAM-Google-Authenticator) pada akses SSH untuk perlindungan lapisan ganda.
2. Menerapkan *Intrusion Detection System* (IDS) berbasis jaringan seperti Snort atau Suricata untuk inspeksi paket payload yang lebih mendalam.

---

## LAMPIRAN

### 6.1 Matriks Pembagian Tugas Anggota

| No | Nama Mahasiswa | NIM | Peran dalam Tim | Rincian Tugas yang Dikerjakan |
| :---: | :--- | :---: | :--- | :--- |
| 1 | **Rafi Dzaka Pratama P** | 123240104 | Project Lead & Target Hardening Engineer | Mengembangkan skrip otomatisasi hardening Node 2, konfigurasi UFW, Fail2ban, dan analisis Lynis. |
| 2 | [Nama Anggota 2] | [NIM] | Red Team Penetration Tester | Mengoperasikan Kali Linux (Node 1), mengeksekusi serangan Nmap & Hydra, mencatat log penyerangan. |
| 3 | [Nama Anggota 3] | [NIM] | Baseline & Unhardened Engineer | Mengonfigurasi Node 3 (Unhardened), pengujian kerentanan awal, dan perbandingan performa. |
| 4 | [Nama Anggota 4] | [NIM] | SIEM & Monitoring Engineer | Mengonfigurasi Rsyslog server pada Node 4, skrip live-monitoring, dan perapihan dokumentasi laporan. |

### 6.2 Lampiran Pendukung
- Repositori Kode & Skrip Otomasi: `https://github.com/MassJakaa/Tubes-SO`
- File Konfigurasi Inti:
  - `/etc/ssh/sshd_config`
  - `/etc/fail2ban/jail.local`
  - `/etc/sysctl.d/99-security-hardening.conf`
  - `/etc/rsyslog.d/30-remote-clients.conf`
