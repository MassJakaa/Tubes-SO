# Panduan Lengkap Eksekusi Tugas Besar Sistem Operasi

**Tema D: Keamanan Sistem Operasi** — OS Hardening, Lynis Security Audit, Fail2ban SSH Protection, Nmap, & SIEM Logging

Disusun untuk Mahasiswa Mata Kuliah Sistem Operasi · Tahun Ajaran 2026/2027
Project Lead: Rafi Dzaka Pratama P (123240104) & Rekan Kelompok

---

## Tujuan Buku Panduan Ini

Panduan ini dirancang agar bisa dipahami dan dipraktikkan langsung oleh seluruh anggota kelompok (bahkan yang masih awam Linux). Isinya mencakup panduan instalasi VirtualBox, cara menghubungkan 4 laptop lewat Hotspot HP tanpa risiko merusak Windows, cara menjalankan skrip otomatis, hingga checklist bukti tangkapan layar (screenshot) untuk laporan akhir.

### Prinsip Utama Pengerjaan

- **Aman untuk laptop:** menggunakan VirtualBox, sehingga Windows asli tidak dihapus atau terganggu.
- **Serba otomatis:** semua konfigurasi rumit (firewall, auto-ban, audit) sudah dibuatkan skrip siap pakai. Anggota cukup mengetik 1 perintah di terminal.
- **Hemat waktu:** total waktu pengujian fisik 4 laptop hanya 20–30 menit.

---

## BAB 1: Persiapan & Bahan yang Dibutuhkan

Sebelum berkumpul bersama kelompok, pastikan bahan berikut sudah siap di laptop masing-masing.

| Bahan / Kebutuhan | Deskripsi & Lokasi Unduh | Penjelasan untuk Anggota |
| :--- | :--- | :--- |
| **1. Oracle VirtualBox** | Sudah disediakan di folder tugas besar: `VirtualBox-Installer.exe` (~105 MB) | Software gratis untuk menjalankan Linux di dalam Windows (seperti membuka aplikasi biasa). |
| **2. File ISO Ubuntu** | Ubuntu Server 22.04 LTS atau Ubuntu Desktop. Cukup 1 orang yang unduh, lalu bagikan via flashdisk. | Sistem operasi Linux yang akan dipasang di dalam VirtualBox. |
| **3. Folder Skrip Otomasi** | Folder `scripts/`: `01_unhardened_target_setup.sh`, `02_hardened_target_setup.sh`, `03_attacker_suite.sh`, `04_siem_collector_setup.sh` | Skrip yang otomatis menginstal dan mengamankan server hanya dengan satu kali tekan Enter. |
| **4. Jaringan (Hotspot HP)** | 1 smartphone salah satu anggota untuk menyalakan Wi-Fi Tethering. | Media penghubung agar keempat laptop bisa saling berkomunikasi dan menyerang di jaringan lokal. |

> **Tips hemat kuota kelompok:** tidak perlu semua anggota mengunduh ISO sendiri-sendiri. Cukup satu orang yang mengunduh ISO Ubuntu (~2 GB), lalu oper ke laptop anggota lain menggunakan flashdisk.

---

## BAB 2: Cara Pasang VirtualBox & Ubuntu di Windows

Ikuti 3 langkah berikut di laptop masing-masing anggota (sekitar 5–10 menit).

### Langkah 1 — Instal VirtualBox di Windows

Buka `VirtualBox-Installer.exe` yang ada di folder tugas besar. Klik **Next → Next →** klik **Yes** saat muncul peringatan "Network Interfaces Warning" **→ Install → Finish**.

### Langkah 2 — Buat Mesin Virtual Baru (Ubuntu)

1. Buka aplikasi Oracle VirtualBox.
2. Klik tombol **New**.
3. Isi kolom yang muncul:
   - **Name:** `Ubuntu-SisOp`
   - **ISO Image:** klik panah dropdown → pilih **Other** → cari dan pilih file ISO Ubuntu di laptop Anda.
   - Centang **"Skip Unattended Installation"** (jika ada pilihan ini).
4. Klik **Next**.
5. **Hardware:** atur RAM (Base Memory) ke **2048 MB (2 GB)** dan Processors ke **2 CPU**. Klik **Next**.
6. **Virtual Hard disk:** biarkan default **25 GB**. Klik **Next → Finish**.

> ### ⚠️ Langkah paling krusial: Pengaturan Bridged Adapter
>
> Agar VM di laptop Anda bisa saling "melihat" dan terhubung dengan laptop anggota lain, jaringan VM harus diubah dari **NAT** menjadi **Bridged**:
>
> 1. Di VirtualBox, klik mesin **Ubuntu-SisOp** → klik **Settings**.
> 2. Klik tab **Network** di sisi kiri.
> 3. Pada **Adapter 1**, ubah "Attached to:" dari **NAT** menjadi **Bridged Adapter**.
> 4. Pada kolom **Name** di bawahnya, pilih kartu Wi-Fi laptop Anda (contoh: Intel Wi-Fi 6 atau Realtek Wireless LAN).
> 5. Klik **OK**.

### Langkah 3 — Nyalakan & Selesaikan Instalasi Ubuntu

Klik tombol **Start** (ikon panah hijau). Pada layar instalasi Ubuntu:

- Pilih **"Try or Install Ubuntu"** → tekan Enter.
- Pilih bahasa **English** → klik Next/Continue sampai bagian membuat user.
- Masukkan nama & password yang mudah diingat (misalnya username mahasiswa dan password `123456`).
- Tunggu instalasi selesai, lalu klik **Restart Now**.

---

## BAB 3: Pembagian Peran 4 Laptop Kelompok

Setiap anggota memiliki peran dan tugas khusus. Tentukan siapa memegang laptop nomor berapa.

| Node | Peran & Nama Host | Tugas Utama | Skrip yang Dijalankan |
| :--- | :--- | :--- | :--- |
| **Laptop 1** | **Attacker Node** (Red Team / Penyerang). Hostname: `kali-attacker` | Melakukan port scanning (Nmap) dan serangan tebak password (Hydra) ke Laptop 2 dan Laptop 3. | Skrip penyerang interaktif: `./03_attacker_suite.sh` |
| **Laptop 2** | **Hardened Target** (Blue Team / Sistem Aman). Hostname: `target-hardened` | Server yang sudah dipasangi firewall UFW, Fail2ban auto-ban, auditd, dan pengerasan kernel sysctl. | Skrip hardening: `sudo bash 02_hardened_target_setup.sh` |
| **Laptop 3** | **Unhardened Target** (Sistem Rentan / Pembanding). Hostname: `target-unhardened` | Server dengan setelan standar pabrik tanpa proteksi, untuk membuktikan bahwa sistem default mudah dibobol. | Skrip baseline rentan: `sudo bash 01_unhardened_target_setup.sh` |
| **Laptop 4** | **SIEM & Monitoring Node** (Pengawas / Log Collector). Hostname: `siem-monitor` | Mengumpulkan log jarak jauh (Rsyslog) dan menampilkan peringatan serangan secara langsung (live alert). | Skrip server log & monitoring: `sudo bash 04_siem_collector_setup.sh` |

---

## BAB 4: Langkah-Langkah Pengujian Bersama (Hari-H)

Saat semua anggota sudah berkumpul membawa laptop masing-masing, ikuti urutan eksekusi berikut.

### Langkah 1 — Koneksi Hotspot & Cek Alamat IP

1. Nyalakan Hotspot HP salah satu anggota (pastikan fitur **"AP Isolation / Client Isolation"** di HP **tidak aktif**).
2. Sambungkan keempat laptop fisik ke Wi-Fi Hotspot tersebut.
3. Nyalakan VM Ubuntu di VirtualBox masing-masing laptop.
4. Buka terminal di VM masing-masing, lalu ketik:

   ```bash
   hostname -I
   ```

5. Catat alamat IP masing-masing laptop (contoh: Laptop 1 = `192.168.43.10`, Laptop 2 = `192.168.43.20`, Laptop 3 = `192.168.43.30`).

### Langkah 2 — Jalankan Skrip di Laptop 3 (Unhardened Target)

Buka terminal di VM Laptop 3, masuk ke folder `scripts`, lalu jalankan:

```bash
sudo bash 01_unhardened_target_setup.sh
```

**Apa yang terjadi?** Skrip otomatis membuat user `korban` dengan password `password123`, mematikan firewall, dan menghitung skor keamanan awal (Lynis).

**Tindakan anggota:** catat skor awal Lynis yang muncul di layar (misal skor 54).

### Langkah 3 — Jalankan Skrip di Laptop 2 (Hardened Target)

Buka terminal di VM Laptop 2, masuk ke folder `scripts`, lalu jalankan:

```bash
sudo bash 02_hardened_target_setup.sh
```

**Apa yang terjadi?** Skrip otomatis mengaktifkan firewall UFW (hanya port 22 & 80), mengaktifkan Fail2ban auto-ban, mengunci kernel sysctl, dan menghitung skor keamanan akhir.

**Tindakan anggota:** perhatikan skor Lynis meningkat drastis menjadi 84. 📸 **Ambil screenshot!**

### Langkah 4 — Jalankan Skrip di Laptop 4 (SIEM Monitor)

Buka terminal di VM Laptop 4, jalankan:

```bash
sudo bash 04_siem_collector_setup.sh
sudo monitor-serangan
```

**Apa yang terjadi?** Layar menjadi pemantau radar serangan berwarna hitam yang menunggu log. Biarkan terminal ini tetap terbuka selama pengujian.

### Langkah 5 — Eksekusi Serangan dari Laptop 1 (Attacker)

Buka terminal di Laptop 1. Masuk ke folder `scripts` dan jalankan menu utama:

```bash
chmod +x 03_attacker_suite.sh
./03_attacker_suite.sh
```

Akan muncul menu pilihan angka 1 sampai 7. Lakukan pengujian berurutan:

#### A. Menu 1 — Uji Latensi Jaringan (Ping Test)

Laptop 1 melakukan ping ke Laptop 2 dan 3. Periksa angka `time=...ms`. Sesuai ketentuan tugas besar, latensi harus **< 5 ms**.

📸 Ambil screenshot terminal ini!

#### B. Menu 2 — Nmap Port Scanning (Uji Firewall)

Nmap memindai kedua target:

- **Laptop 3 (Unhardened):** banyak port terbuka bebas (`open`).
- **Laptop 2 (Hardened):** port selain 22 dan 80 tertutup rapat (`filtered`/`closed`) oleh UFW.

📸 Ambil screenshot perbandingan hasil Nmap ini!

#### C. Menu 3 — Hydra Brute Force ke Laptop 3 (Unhardened)

Hydra mencoba menebak kata sandi akun `korban`. Karena Laptop 3 tidak memiliki pengamanan, dalam beberapa detik akan muncul teks hijau:

```text
[22][ssh] host: 192.168.43.30 login: korban password: password123
```

Ini bukti bahwa server unhardened berhasil ditembus.

📸 Ambil screenshot terminal Hydra yang sukses menembus!

#### D. Menu 4 — Hydra Brute Force ke Laptop 2 (Hardened — Fail2ban)

Hydra mencoba menebak kata sandi ke Laptop 2. Setelah 3 kali gagal, Fail2ban langsung memblokir IP Laptop 1. Koneksi berikutnya menghasilkan pesan `Connection refused` atau `Operation timed out`. Serangan penyerang gagal total.

📸 Ambil screenshot terminal yang menunjukkan koneksi terblokir!

### Langkah 6 — Verifikasi Kemenangan Pertahanan di Laptop 2 & Laptop 4

1. Di **Laptop 2 (Hardened Target)**, ketik:

   ```bash
   sudo fail2ban-client status sshd
   ```

   Anda akan melihat baris `Banned IP list: 192.168.43.10` (IP penyerang resmi diblokir).

   📸 Ambil screenshot bukti Banned IP ini!

2. Di **Laptop 4 (SIEM Monitor)**, lihat layar `monitor-serangan`. Akan tercatat tanggal, jam, dan baris `Ban 192.168.43.10` secara otomatis.

   📸 Ambil screenshot layar monitor log ini!

3. Di **Laptop 2**, cetak tabel perbandingan:

   ```bash
   bash 05_audit_comparator.sh
   ```

   📸 Ambil screenshot tabel perbandingan nilai skor Lynis!

---

## BAB 5: Checklist Bukti Tangkapan Layar (untuk Laporan Word)

Semua screenshot yang sudah diambil dimasukkan ke dalam file Word `Laporan_Akhir_Tugas_Besar_Keamanan_OS.docx` pada **Bab IV.2**.

| No | Nama Bukti Tangkapan Layar | Diambil dari Layar Laptop | Status |
| :---: | :--- | :--- | :---: |
| 1 | Hasil Ping sweep (latensi < 5 ms) | Laptop 1 (Attacker) | [ ] |
| 2 | Hasil Nmap scan (Unhardened vs Hardened) | Laptop 1 (Attacker) | [ ] |
| 3 | Hydra berhasil tembus pada target unhardened | Laptop 1 (Attacker) | [ ] |
| 4 | Hydra terblokir (Connection refused) pada hardened | Laptop 1 (Attacker) | [ ] |
| 5 | `fail2ban-client status sshd` (Banned IP list) | Laptop 2 (Hardened) | [ ] |
| 6 | Terminal Live Log Monitor (SIEM) | Laptop 4 (SIEM) | [ ] |
| 7 | Tabel Skor Audit Lynis (54 vs 84) | Laptop 2 (Hardened) | [ ] |
| 8 | Foto dokumentasi kelompok saat mengerjakan bersama (Lampiran) | Kamera HP | [ ] |

---

## BAB 6: Tanya Jawab & Solusi Kendala (Troubleshooting)

### Q1: Laptop 1 tidak bisa ping ke Laptop 2 atau 3 (Request Timed Out). Kenapa?

**Solusi:**

1. Pastikan di VirtualBox, jaringan VM sudah diatur ke **Bridged Adapter** (bukan NAT).
2. Periksa pengaturan Hotspot di HP. Pastikan opsi **"AP Isolation"** atau **"Client Isolation"** dimatikan.
3. Di Windows laptop target, coba matikan sementara Windows Defender Firewall saat pengujian.

### Q2: Saat menjalankan skrip muncul pesan "Permission denied"?

**Solusi:** tambahkan `sudo` di depan perintah, contoh:

```bash
sudo bash 02_hardened_target_setup.sh
```

atau berikan izin eksekusi:

```bash
chmod +x *.sh
```

### Q3: Setelah uji coba nomor 4, Laptop 1 sama sekali tidak bisa connect lagi ke Laptop 2. Apakah rusak?

**Solusi:** **Tidak rusak.** Itu tanda pertahanan Fail2ban berhasil, karena IP Laptop 1 telah diblokir. Untuk membuka blokir saat demo ulang, ketik di Laptop 2:

```bash
sudo fail2ban-client unban 192.168.43.10
```

---

*Panduan Praktikum Tugas Besar Sistem Operasi · Dibuat untuk Kelompok Sistem Operasi 2026/2027 · Sukses selalu!*