import asyncio
import os
from playwright.async_api import async_playwright

HTML_CONTENT = """<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<title>Panduan Lengkap Praktikum Tugas Besar Sistem Operasi</title>
<style>
  @page {
    size: A4 portrait;
    margin: 18mm 16mm 18mm 16mm;
    @bottom-right {
      content: "Halaman " counter(page) " dari " counter(pages);
      font-size: 8.5pt;
      font-family: 'Segoe UI', Arial, sans-serif;
      color: #64748b;
    }
    @bottom-left {
      content: "Tugas Besar Sistem Operasi - Tema D (Keamanan OS)";
      font-size: 8.5pt;
      font-family: 'Segoe UI', Arial, sans-serif;
      color: #64748b;
    }
  }

  body {
    font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, Helvetica, Arial, sans-serif;
    color: #1e293b;
    line-height: 1.55;
    font-size: 10pt;
    margin: 0;
    padding: 0;
  }

  .cover {
    page-break-after: always;
    display: flex;
    flex-direction: column;
    justify-content: center;
    min-height: 90vh;
    padding: 30px 20px;
    box-sizing: border-box;
  }

  .badge-topic {
    display: inline-block;
    background: #0284c7;
    color: white;
    font-weight: 700;
    font-size: 9pt;
    padding: 4px 14px;
    border-radius: 20px;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 18px;
  }

  h1.main-title {
    font-size: 24pt;
    font-weight: 800;
    color: #0f172a;
    line-height: 1.25;
    margin: 0 0 12px 0;
  }

  .subtitle {
    font-size: 13pt;
    color: #475569;
    line-height: 1.45;
    margin-bottom: 25px;
    font-weight: 400;
  }

  .card-summary {
    background: #f8fafc;
    border: 1.5px solid #e2e8f0;
    border-left: 5px solid #0284c7;
    border-radius: 10px;
    padding: 16px 20px;
    margin-bottom: 30px;
  }

  .card-summary h4 {
    margin: 0 0 8px 0;
    font-size: 11pt;
    color: #0f172a;
  }

  .card-summary p {
    margin: 0;
    color: #334155;
    font-size: 9.5pt;
  }

  .meta-box {
    margin-top: auto;
    border-top: 1px solid #cbd5e1;
    padding-top: 15px;
    font-size: 9pt;
    color: #64748b;
  }

  h2 {
    font-size: 14pt;
    font-weight: 700;
    color: #0f172a;
    border-bottom: 2px solid #0284c7;
    padding-bottom: 6px;
    margin-top: 24px;
    margin-bottom: 12px;
    page-break-after: avoid;
  }

  h3 {
    font-size: 11.5pt;
    font-weight: 600;
    color: #1e3a8a;
    margin-top: 16px;
    margin-bottom: 8px;
    page-break-after: avoid;
  }

  p {
    margin: 0 0 10px 0;
    color: #334155;
    text-align: justify;
  }

  .step-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 12px 16px;
    margin-bottom: 12px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    page-break-inside: avoid;
  }

  .step-header {
    display: flex;
    align-items: center;
    margin-bottom: 8px;
  }

  .step-num {
    background: #0284c7;
    color: white;
    width: 24px;
    height: 24px;
    border-radius: 50%;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    font-size: 9.5pt;
    margin-right: 10px;
    flex-shrink: 0;
  }

  .step-title {
    font-weight: 700;
    font-size: 10.5pt;
    color: #0f172a;
  }

  .callout-important {
    background: #fef2f2;
    border: 1.5px solid #fecaca;
    border-left: 4px solid #ef4444;
    border-radius: 8px;
    padding: 10px 14px;
    margin: 12px 0;
    page-break-inside: avoid;
  }

  .callout-important strong {
    color: #991b1b;
    display: block;
    margin-bottom: 4px;
    font-size: 9.5pt;
  }

  .callout-tip {
    background: #f0fdf4;
    border: 1.5px solid #bbf7d0;
    border-left: 4px solid #22c55e;
    border-radius: 8px;
    padding: 10px 14px;
    margin: 12px 0;
    page-break-inside: avoid;
  }

  .callout-tip strong {
    color: #166534;
    display: block;
    margin-bottom: 4px;
    font-size: 9.5pt;
  }

  code {
    background: #f1f5f9;
    color: #0f172a;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 9pt;
    padding: 2px 5px;
    border-radius: 4px;
    border: 1px solid #e2e8f0;
  }

  pre {
    background: #0f172a;
    color: #f8fafc;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 8.5pt;
    padding: 10px 14px;
    border-radius: 6px;
    overflow-x: auto;
    margin: 6px 0 10px 0;
    line-height: 1.45;
  }

  table {
    width: 100%;
    border-collapse: collapse;
    margin: 12px 0;
    font-size: 9pt;
    page-break-inside: avoid;
  }

  th {
    background: #1e293b;
    color: white;
    text-align: left;
    padding: 8px 10px;
    font-weight: 600;
  }

  td {
    border: 1px solid #cbd5e1;
    padding: 7px 10px;
    color: #334155;
    vertical-align: top;
  }

  tr:nth-child(even) td {
    background: #f8fafc;
  }

  ul, ol {
    margin: 4px 0 10px 20px;
    padding: 0;
    color: #334155;
  }

  li {
    margin-bottom: 4px;
  }

  .page-break {
    page-break-after: always;
  }
</style>
</head>
<body>

<!-- ================= COVER PAGE ================= -->
<div class="cover">
  <div>
    <span class="badge-topic">Buku Panduan Praktikum Praktis</span>
    <h1 class="main-title">PANDUAN LENGKAP EKSEKUSI TUGAS BESAR SISTEM OPERASI</h1>
    <div class="subtitle">
      Tema D: Keamanan Sistem Operasi (OS Hardening, Lynis Security Audit, Fail2ban SSH Protection, Nmap, & SIEM Logging)
    </div>
  </div>

  <div class="card-summary">
    <h4>Tujuan Buku Panduan Ini</h4>
    <p>
      Panduan ini dirancang khusus agar <strong>bisa dipahami dan dipraktikkan langsung oleh seluruh anggota kelompok</strong> (bahkan yang masih awam Linux). Dilengkapi panduan instalasi VirtualBox, cara menghubungkan 4 laptop lewat Hotspot HP tanpa resiko merusak Windows, cara menjalankan skrip otomatis, hingga checklist bukti tangkapan layar (screenshot) untuk laporan akhir.
    </p>
  </div>

  <div style="background: #e0f2fe; border: 1px solid #bae6fd; border-radius: 8px; padding: 14px 18px; margin-bottom: 25px;">
    <strong style="color: #0369a1; display: block; margin-bottom: 6px;">Prinsip Utama Pengerjaan:</strong>
    <ul style="margin: 0 0 0 18px; font-size: 9.5pt; color: #0c4a6e;">
      <li><strong>Aman untuk Laptop:</strong> Kita menggunakan VirtualBox, jadi sistem operasi Windows asli teman-teman tidak akan dihapus atau terganggu.</li>
      <li><strong>Serba Otomatis:</strong> Semua konfigurasi rumit (firewall, auto-ban, audit) sudah dibuatkan skrip siap pakai. Anggota kelompok hanya perlu ketik 1 perintah di terminal!</li>
      <li><strong>Hemat Waktu:</strong> Total waktu pengujian fisik 4 laptop hanya butuh 20 - 30 menit.</li>
    </ul>
  </div>

  <div class="meta-box">
    <strong>Disusun untuk Mahasiswa Mata Kuliah Sistem Operasi</strong><br>
    Program Studi Informatika / Sistem Komputer &bull; Tahun Ajaran 2026/2027<br>
    <em>Project Lead: Rafi Dzaka Pratama P (123240104) & Rekan Kelompok</em>
  </div>
</div>

<!-- ================= BAB 1: PERSIAPAN & BAHAN ================= -->
<h2>BAB 1: PERSIAPAN & BAHAN YANG DIBUTUHKAN</h2>
<p>
  Sebelum mulai kumpul bersama kelompok, pastikan bahan-bahan berikut sudah siap di laptop masing-masing:
</p>

<table>
  <tr>
    <th style="width: 25%;">Bahan / Kebutuhan</th>
    <th style="width: 40%;">Deskripsi & Lokasi Unduh</th>
    <th style="width: 35%;">Penjelasan untuk Anggota</th>
  </tr>
  <tr>
    <td><strong>1. Oracle VirtualBox</strong></td>
    <td>
      Sudah disediakan di folder tugas besar:<br>
      <code>VirtualBox-Installer.exe</code><br>
      <em>(Ukuran: ~105 MB)</em>
    </td>
    <td>Software gratis untuk menjalankan Linux di dalam Windows (seperti buka aplikasi biasa).</td>
  </tr>
  <tr>
    <td><strong>2. File ISO Ubuntu</strong></td>
    <td>
      Gunakan <strong>Ubuntu Server 22.04 LTS</strong> atau <strong>Ubuntu Desktop</strong>.<br>
      <em>(Cukup 1 orang yang unduh, lalu bagikan via flashdisk).</em>
    </td>
    <td>Sistem operasi Linux yang akan dipasang di dalam VirtualBox.</td>
  </tr>
  <tr>
    <td><strong>3. Folder Skrip Otomasi</strong></td>
    <td>
      Folder <code>scripts/</code> di folder tugas besar:<br>
      &bull; <code>01_unhardened_target_setup.sh</code><br>
      &bull; <code>02_hardened_target_setup.sh</code><br>
      &bull; <code>03_attacker_suite.sh</code><br>
      &bull; <code>04_siem_collector_setup.sh</code>
    </td>
    <td>Skrip sakti yang otomatis menginstal dan mengamankan server hanya dengan satu kali tekan Enter.</td>
  </tr>
  <tr>
    <td><strong>4. Jaringan (Hotspot HP)</strong></td>
    <td>
      1 Smartphone salah satu anggota untuk menyalakan <strong>Wi-Fi Tethering</strong>.
    </td>
    <td>Media penghubung agar ke-4 laptop bisa saling berkomunikasi dan menyerang di jaringan lokal.</td>
  </tr>
</table>

<div class="callout-tip">
  <strong>TIPS HEMAT KUOTA KELOMPOK:</strong>
  Tidak perlu semua anggota download ISO sendiri-sendiri! Cukup ketua/satu orang yang download file ISO Ubuntu (~2 GB), lalu oper file ISO tersebut ke laptop anggota lain menggunakan flashdisk.
</div>

<!-- ================= BAB 2: CARA INSTAL VIRTUALBOX & UBUNTU ================= -->
<h2>BAB 2: CARA PASANG VIRTUALBOX & UBUNTU DI WINDOWS</h2>
<p>
  Ikuti 4 langkah mudah berikut di laptop masing-masing anggota (hanya butuh waktu sekitar 5–10 menit):
</p>

<div class="step-card">
  <div class="step-header">
    <div class="step-num">1</div>
    <div class="step-title">Instal Aplikasi VirtualBox di Windows</div>
  </div>
  <p>
    Buka file <code>VirtualBox-Installer.exe</code> yang sudah ada di folder tugas besar. Klik <strong>Next</strong> &rarr; <strong>Next</strong> &rarr; klik <strong>Yes</strong> saat ada peringatan <em>"Network Interfaces Warning"</em> &rarr; klik <strong>Install</strong> &rarr; lalu klik <strong>Finish</strong>. VirtualBox sekarang sudah terpasang!
  </p>
</div>

<div class="step-card">
  <div class="step-header">
    <div class="step-num">2</div>
    <div class="step-title">Buat Mesin Virtual Baru (Ubuntu)</div>
  </div>
  <ol>
    <li>Buka aplikasi <strong>Oracle VirtualBox</strong>.</li>
    <li>Klik tombol <strong>New</strong> (ikon bintang biru di bagian atas).</li>
    <li>Isi kolom yang muncul:
      <ul>
        <li><strong>Name:</strong> <code>Ubuntu-SisOp</code></li>
        <li><strong>ISO Image:</strong> Klik panah dropdown &rarr; pilih <em>Other</em> &rarr; cari dan pilih file ISO Ubuntu yang ada di laptop Anda.</li>
        <li>Centang kotak <strong>"Skip Unattended Installation"</strong> (jika ada pilihan ini).</li>
      </ul>
    </li>
    <li>Klik <strong>Next</strong>.</li>
    <li><strong>Hardware:</strong> Atur RAM (Base Memory) ke <strong>2048 MB (2 GB)</strong> dan Processors ke <strong>2 CPU</strong>. Klik <strong>Next</strong>.</li>
    <li><strong>Virtual Hard disk:</strong> Biarkan default <strong>25 GB</strong>. Klik <strong>Next</strong> &rarr; lalu <strong>Finish</strong>.</li>
  </ol>
</div>

<div class="callout-important">
  <strong>LANGKAH PALING KRUSIAL (JANGAN SAMPAI TERLEWAT): PENGATURAN BRIDGED ADAPTER</strong>
  Agar mesin virtual di laptop Anda bisa saling "melihat" dan terhubung dengan laptop teman-teman yang lain, jaringan VM harus diubah dari NAT menjadi Bridged:
  <ol style="margin-top: 6px; margin-bottom: 0;">
    <li>Di VirtualBox, klik mesin <strong>Ubuntu-SisOp</strong> Anda &rarr; klik menu <strong>Settings</strong> (ikon gerigi).</li>
    <li>Klik tab <strong>Network</strong> di sisi kiri.</li>
    <li>Pada <strong>Adapter 1</strong>, ubah tulisan <em>"Attached to:"</em> dari <strong>NAT</strong> menjadi <strong>Bridged Adapter</strong>.</li>
    <li>Pada kolom <em>Name</em> di bawahnya, pilih kartu Wi-Fi laptop Anda (contoh: <em>Intel Wi-Fi 6</em> atau <em>Realtek Wireless LAN</em>).</li>
    <li>Klik <strong>OK</strong>.</li>
  </ol>
</div>

<div class="step-card">
  <div class="step-header">
    <div class="step-num">3</div>
    <div class="step-title">Menyalakan & Menyelesaikan Instalasi Ubuntu</div>
  </div>
  <p>
    Klik tombol <strong>Start</strong> (ikon panah hijau). Layar instalasi Ubuntu akan menyala:
  </p>
  <ul>
    <li>Pilih <em>"Try or Install Ubuntu"</em> &rarr; tekan Enter.</li>
    <li>Pilih bahasa <em>English</em> &rarr; klik Next/Continue terus sampai bagian membuat user.</li>
    <li><strong>Masukkan Nama & Password:</strong> Buat yang mudah diingat, misalnya username <code>mahasiswa</code> dan password <code>123456</code>.</li>
    <li>Tunggu hingga proses instalasi selesai, lalu klik <strong>Restart Now</strong>.</li>
  </ul>
</div>

<div class="page-break"></div>

<!-- ================= BAB 3: PEMBAGIAN PERAN 4 LAPTOP ================= -->
<h2>BAB 3: PEMBAGIAN PERAN 4 LAPTOP KELOMPOK</h2>
<p>
  Dalam tugas besar Keamanan Sistem Operasi, setiap anggota memiliki peran dan tugas khusus. Tentukan siapa memegang laptop nomor berapa:
</p>

<table>
  <tr>
    <th style="width: 15%;">Node</th>
    <th style="width: 25%;">Peran & Nama Host</th>
    <th style="width: 30%;">Tugas Utama</th>
    <th style="width: 30%;">Skrip yang Dijalankan</th>
  </tr>
  <tr>
    <td><strong>Laptop 1</strong></td>
    <td><strong>Attacker Node</strong><br><em>(Red Team / Penyerang)</em><br>Hostname: <code>kali-attacker</code></td>
    <td>Melakukan scanning port (Nmap) dan menembakkan serangan tebak password (Hydra) ke Laptop 2 dan Laptop 3.</td>
    <td>Menjalankan skrip penyerang interaktif:<br><code>./03_attacker_suite.sh</code></td>
  </tr>
  <tr>
    <td><strong>Laptop 2</strong></td>
    <td><strong>Hardened Target</strong><br><em>(Blue Team / Sistem Aman)</em><br>Hostname: <code>target-hardened</code></td>
    <td>Server yang sudah dipasangi firewall UFW, Fail2ban auto-ban, auditd, dan pengerasan kernel sysctl.</td>
    <td>Menjalankan skrip hardening:<br><code>sudo bash 02_hardened_target_setup.sh</code></td>
  </tr>
  <tr>
    <td><strong>Laptop 3</strong></td>
    <td><strong>Unhardened Target</strong><br><em>(Sistem Rentan / Pembanding)</em><br>Hostname: <code>target-unhardened</code></td>
    <td>Server dengan setelan standar pabrik tanpa proteksi untuk membuktikan bahwa sistem default mudah dibobol.</td>
    <td>Menjalankan skrip baseline rentan:<br><code>sudo bash 01_unhardened_target_setup.sh</code></td>
  </tr>
  <tr>
    <td><strong>Laptop 4</strong></td>
    <td><strong>SIEM & Monitoring Node</strong><br><em>(Pengawas / Log Collector)</em><br>Hostname: <code>siem-monitor</code></td>
    <td>Mengumpulkan log jarak jauh (Rsyslog) dan menampilkan peringatan serangan secara langsung (live alert).</td>
    <td>Menjalankan skrip server log & monitoring:<br><code>sudo bash 04_siem_collector_setup.sh</code></td>
  </tr>
</table>

<!-- ================= BAB 4: PANDUAN PENGUJIAN STEP-BY-STEP ================= -->
<h2>BAB 4: LANGKAH-LANGKAH PENGUJIAN BERSAMA (HARI-H)</h2>
<p>
  Saat semua anggota kelompok sudah kumpul membawa laptop masing-masing, ikuti urutan eksekusi berikut:
</p>

<h3>Langkah 1: Koneksi Hotspot & Cek Alamat IP</h3>
<ol>
  <li>Nyalakan <strong>Hotspot HP</strong> salah satu anggota kelompok (pastikan fitur <em>"AP Isolation / Client Isolation"</em> di HP tidak aktif).</li>
  <li>Sambungkan ke-4 laptop fisik ke Wi-Fi Hotspot tersebut.</li>
  <li>Nyalakan VM Ubuntu di VirtualBox masing-masing laptop.</li>
  <li>Buka terminal di VM masing-masing, lalu ketik:
    <pre>hostname -I</pre>
  </li>
  <li>Catat alamat IP masing-masing laptop (contoh: Laptop 1 = <code>192.168.43.10</code>, Laptop 2 = <code>192.168.43.20</code>, Laptop 3 = <code>192.168.43.30</code>).</li>
</ol>

<h3>Langkah 2: Jalankan Skrip di Laptop 3 (Unhardened Target)</h3>
<p>Buka terminal di VM Laptop 3, masuk ke folder scripts, lalu jalankan:</p>
<pre>sudo bash 01_unhardened_target_setup.sh</pre>
<p>
  <em>Apa yang terjadi?</em> Skrip otomatis membuat user <code>korban</code> dengan password <code>password123</code>, mematikan firewall, dan menghitung skor keamanan awal (Lynis).<br>
  <strong>Tindakan Anggota:</strong> Catat skor awal Lynis yang muncul di layar (misal skor <strong>54</strong>).
</p>

<h3>Langkah 3: Jalankan Skrip di Laptop 2 (Hardened Target)</h3>
<p>Buka terminal di VM Laptop 2, masuk ke folder scripts, lalu jalankan:</p>
<pre>sudo bash 02_hardened_target_setup.sh</pre>
<p>
  <em>Apa yang terjadi?</em> Skrip otomatis mengaktifkan UFW firewall (hanya port 22 & 80), mengaktifkan Fail2ban auto-ban, mengunci kernel sysctl, dan menghitung skor keamanan akhir.<br>
  <strong>Tindakan Anggota:</strong> Perhatikan skor Lynis meningkat drastis menjadi <strong>84</strong>. Ambil screenshot!
</p>

<h3>Langkah 4: Jalankan Skrip di Laptop 4 (SIEM Monitor)</h3>
<p>Buka terminal di VM Laptop 4, jalankan:</p>
<pre>sudo bash 04_siem_collector_setup.sh
sudo monitor-serangan</pre>
<p>
  <em>Apa yang terjadi?</em> Layar akan menjadi pemantau radar serangan berwarna hitam yang menunggu log. Biarkan terminal ini tetap terbuka selama pengujian.
</p>

<div class="page-break"></div>

<h3>Langkah 5: Eksekusi Serangan dari Laptop 1 (Attacker)</h3>
<p>Buka terminal di Laptop 1 (Penyerang). Masuk ke folder scripts dan jalankan menu utama:</p>
<pre>chmod +x 03_attacker_suite.sh
./03_attacker_suite.sh</pre>

<p>Akan muncul menu pilihan angka 1 sampai 7. Lakukan pengujian berurutan:</p>

<div class="step-card">
  <div class="step-header">
    <div class="step-num">A</div>
    <div class="step-title">Pilih Menu 1: Uji Latensi Jaringan (Ping Test)</div>
  </div>
  <p>
    Laptop 1 akan melakukan ping ke Laptop 2 dan 3. Periksa angka <code>time=...ms</code>. Sesuai ketentuan tugas besar, latensi harus <strong>&lt; 5 ms</strong>. <br>
    📸 <strong>Ambil Screenshot terminal ini!</strong>
  </p>
</div>

<div class="step-card">
  <div class="step-header">
    <div class="step-num">B</div>
    <div class="step-title">Pilih Menu 2: Nmap Port Scanning (Uji Firewall)</div>
  </div>
  <p>
    Nmap akan memindai kedua target:
  </p>
  <ul>
    <li>Pada Laptop 3 (Unhardened): Terlihat banyak port terbuka secara bebas (open).</li>
    <li>Pada Laptop 2 (Hardened): Port selain 22 dan 80 tertutup rapat (filtered/closed) oleh UFW!</li>
  </ul>
  📸 <strong>Ambil Screenshot perbandingan hasil Nmap ini!</strong>
</div>

<div class="step-card">
  <div class="step-header">
    <div class="step-num">C</div>
    <div class="step-title">Pilih Menu 3: Hydra Brute Force ke Laptop 3 (Unhardened)</div>
  </div>
  <p>
    Hydra akan mencoba menebak kata sandi akun <code>korban</code>. Karena Laptop 3 tidak memiliki pengamanan, dalam waktu beberapa detik akan muncul teks hijau bertuliskan: <br>
    <code>[22][ssh] host: 192.168.43.30 login: korban password: password123</code><br>
    Ini bukti bahwa server unhardened berhasil ditembus! <br>
    📸 <strong>Ambil Screenshot terminal Hydra yang sukses menembus!</strong>
  </p>
</div>

<div class="step-card">
  <div class="step-header">
    <div class="step-num">D</div>
    <div class="step-title">Pilih Menu 4: Hydra Brute Force ke Laptop 2 (Hardened - Fail2ban)</div>
  </div>
  <p>
    Hydra mencoba menebak kata sandi ke Laptop 2. Setelah 3 kali gagal, <strong>Fail2ban langsung bertindak memblokir IP Laptop 1!</strong> <br>
    Koneksi berikutnya akan menghasilkan pesan: <code>Connection refused</code> atau <code>Operation timed out</code>. Serangan penyerang gagal total!<br>
    📸 <strong>Ambil Screenshot terminal yang menunjukkan koneksi terblokir!</strong>
  </p>
</div>

<h3>Langkah 6: Verifikasi Kemenangan Pertahanan di Laptop 2 & Laptop 4</h3>
<ol>
  <li><strong>Di Laptop 2 (Hardened Target), ketik:</strong>
    <pre>sudo fail2ban-client status sshd</pre>
    Anda akan melihat baris: <code>Banned IP list: 192.168.43.10</code> (IP penyerang resmi diblokir). <br>
    📸 <strong>Ambil Screenshot bukti Banned IP ini!</strong>
  </li>
  <li><strong>Di Laptop 4 (SIEM Monitor):</strong>
    Lihat layar <code>monitor-serangan</code>. Akan tercatat log tanggal, jam, dan baris <code>Ban 192.168.43.10</code> secara otomatis. <br>
    📸 <strong>Ambil Screenshot layar monitor log ini!</strong>
  </li>
  <li><strong>Di Laptop 2, cetak tabel perbandingan:</strong>
    <pre>bash 05_audit_comparator.sh</pre>
    📸 <strong>Ambil Screenshot tabel perbandingan nilai skor Lynis!</strong>
  </li>
</ol>

<!-- ================= BAB 5: CHECKLIST SCREENSHOT ================= -->
<h2>BAB 5: CHECKLIST BUKTI TANGKAPAN LAYAR (UNTUK LAPORAN WORD)</h2>
<p>
  Semua screenshot yang sudah diambil tinggal dimasukkan ke dalam file Word yang sudah disiapkan (<code>Laporan_Akhir_Tugas_Besar_Keamanan_OS.docx</code>) pada <strong>Bab IV.2</strong>:
</p>

<table>
  <tr>
    <th style="width: 10%;">No</th>
    <th style="width: 45%;">Nama Bukti Tangkapan Layar (Screenshot)</th>
    <th style="width: 30%;">Diambil dari Layar Laptop</th>
    <th style="width: 15%; text-align: center;">Status</th>
  </tr>
  <tr>
    <td>1</td>
    <td>Screenshot hasil Ping sweep (latensi &lt; 5 ms)</td>
    <td>Laptop 1 (Attacker)</td>
    <td style="text-align: center;">[ &nbsp; ]</td>
  </tr>
  <tr>
    <td>2</td>
    <td>Screenshot hasil Nmap scan (Unhardened vs Hardened)</td>
    <td>Laptop 1 (Attacker)</td>
    <td style="text-align: center;">[ &nbsp; ]</td>
  </tr>
  <tr>
    <td>3</td>
    <td>Screenshot Hydra berhasil tembus pada target unhardened</td>
    <td>Laptop 1 (Attacker)</td>
    <td style="text-align: center;">[ &nbsp; ]</td>
  </tr>
  <tr>
    <td>4</td>
    <td>Screenshot Hydra terblokir (Connection refused) pada hardened</td>
    <td>Laptop 1 (Attacker)</td>
    <td style="text-align: center;">[ &nbsp; ]</td>
  </tr>
  <tr>
    <td>5</td>
    <td>Screenshot <code>fail2ban-client status sshd</code> (Banned IP list)</td>
    <td>Laptop 2 (Hardened)</td>
    <td style="text-align: center;">[ &nbsp; ]</td>
  </tr>
  <tr>
    <td>6</td>
    <td>Screenshot Terminal Live Log Monitor (SIEM)</td>
    <td>Laptop 4 (SIEM)</td>
    <td style="text-align: center;">[ &nbsp; ]</td>
  </tr>
  <tr>
    <td>7</td>
    <td>Screenshot Tabel Skor Audit Lynis (54 vs 84)</td>
    <td>Laptop 2 (Hardened)</td>
    <td style="text-align: center;">[ &nbsp; ]</td>
  </tr>
  <tr>
    <td>8</td>
    <td>Foto dokumentasi kelompok saat mengerjakan bersama (Lampiran)</td>
    <td>Kamera HP</td>
    <td style="text-align: center;">[ &nbsp; ]</td>
  </tr>
</table>

<!-- ================= BAB 6: FAQ & TROUBLESHOOTING ================= -->
<h2>BAB 6: TANYA JAWAB & SOLUSI KENDALA (TROUBLESHOOTING)</h2>

<div class="step-card">
  <strong>Q1: Laptop 1 tidak bisa melakukan ping ke Laptop 2 atau 3 (Request Timed Out). Kenapa?</strong>
  <p style="margin-top: 4px;">
    <strong>Solusi:</strong>
    1. Pastikan di VirtualBox, pengaturan jaringan VM sudah diatur ke <strong>Bridged Adapter</strong> (bukan NAT).<br>
    2. Periksa pengaturan Hotspot di HP. Pastikan opsi <em>"AP Isolation"</em> atau <em>"Client Isolation"</em> dimatikan.<br>
    3. Di Windows laptop target, coba matikan sementara Windows Defender Firewall saat pengujian.
  </p>
</div>

<div class="step-card">
  <strong>Q2: Saat menjalankan skrip muncul pesan "Permission denied"?</strong>
  <p style="margin-top: 4px;">
    <strong>Solusi:</strong> Tambahkan kata <code>sudo</code> di depan perintah, contoh: <code>sudo bash 02_hardened_target_setup.sh</code> atau berikan izin eksekusi: <code>chmod +x *.sh</code>.
  </p>
</div>

<div class="step-card">
  <strong>Q3: Setelah uji coba nomor 4, Laptop 1 sama sekali tidak bisa connect lagi ke Laptop 2. Apakah rusak?</strong>
  <p style="margin-top: 4px;">
    <strong>Solusi:</strong> TIDAK RUSAK! Itu tanda bahwa pertahanan <strong>Fail2ban berhasil 100%</strong> karena IP Laptop 1 telah diblokir. Jika ingin membuka blokirnya untuk demo ulang, ketik di Laptop 2:
    <pre>sudo fail2ban-client unban 192.168.43.10</pre>
  </p>
</div>

<div style="text-align: center; margin-top: 25px; padding-top: 15px; border-top: 1px solid #e2e8f0; font-size: 8.5pt; color: #64748b;">
  Panduan Praktikum Tugas Besar Sistem Operasi &bull; Dibuat untuk Kelompok Sistem Operasi 2026/2027 &bull; Sukses Selalu!
</div>

</body>
</html>
"""

async def generate_pdf():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    html_path = os.path.join(script_dir, "tutorial_tugas_besar.html")
    pdf_path = os.path.join(script_dir, "Panduan_Lengkap_Tugas_Besar_Keamanan_OS.pdf")

    print(f"[*] Menulis HTML ke: {html_path}")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(HTML_CONTENT)

    print(f"[*] Mengonversi ke PDF menggunakan Playwright...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(f"file:///{html_path.replace(os.sep, '/')}")
        await page.wait_for_load_state("networkidle")

        await page.pdf(
            path=pdf_path,
            format="A4",
            print_background=True,
            display_header_footer=False,
            margin={"top": "10mm", "bottom": "10mm", "left": "10mm", "right": "10mm"}
        )
        print(f"[+] PDF Berhasil Dibuat di: {pdf_path}")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(generate_pdf())
