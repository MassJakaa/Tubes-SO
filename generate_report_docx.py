import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_hex)
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('w:top', top), ('w:bottom', bottom), ('w:left', left), ('w:right', right)]:
        node = OxmlElement(m)
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def create_report():
    doc = docx.Document()

    # Set Margins (Standard 1 inch / 2.54 cm)
    for section in doc.sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)

    # Document Styles
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(12)
    normal_style.font.color.rgb = RGBColor(0x22, 0x22, 0x22)
    normal_style.paragraph_format.line_spacing = 1.15
    normal_style.paragraph_format.space_after = Pt(6)

    # ================= COVER / TITLE =================
    title_p = doc.add_paragraph()
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title_p.paragraph_format.space_before = Pt(36)
    title_p.paragraph_format.space_after = Pt(12)
    run_t = title_p.add_run("LAPORAN AKHIR TUGAS BESAR SISTEM OPERASI")
    run_t.bold = True
    run_t.font.size = Pt(16)
    run_t.font.color.rgb = RGBColor(0x1F, 0x49, 0x7D)

    sub_p = doc.add_paragraph()
    sub_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    sub_p.paragraph_format.space_after = Pt(28)
    run_sub = sub_p.add_run("Analisis Komparatif Ketahanan Sistem Operasi Linux (Hardened vs Unhardened)\nTerhadap Serangan Brute Force dan Port Scanning Berbasis CIS Benchmark")
    run_sub.bold = True
    run_sub.font.size = Pt(13)

    meta_p = doc.add_paragraph()
    meta_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    meta_p.paragraph_format.space_after = Pt(36)
    r_meta = meta_p.add_run("Disusun Oleh:\n1. Rafi Dzaka Pratama P (NIM: 123240104)\n2. [Nama Anggota 2] (NIM: [NIM 2])\n3. [Nama Anggota 3] (NIM: [NIM 3])\n4. [Nama Anggota 4] (NIM: [NIM 4])\n\nPROGRAM STUDI TEKNIK INFORMATIKA\nFAKULTAS TEKNIK INDUSTRI\n2026/2027")
    r_meta.font.size = Pt(11)

    doc.add_page_break()

    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(16)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.bold = True
        run.font.size = Pt(14)
        run.font.color.rgb = RGBColor(0x1F, 0x49, 0x7D)

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.bold = True
        run.font.size = Pt(12.5)
        run.font.color.rgb = RGBColor(0x33, 0x33, 0x33)

    def add_code(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.left_indent = Inches(0.2)
        run = p.add_run(text)
        run.font.name = 'Consolas'
        run.font.size = Pt(9.5)
        run.font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)

    # ================= BAB I =================
    add_h1("BAB I: PENDAHULUAN")
    
    add_h2("1.1 Latar Belakang & Urgensi")
    doc.add_paragraph(
        "Sistem Operasi (OS) bertindak sebagai jembatan fundamental antara perangkat keras komputer dan aplikasi pengguna. "
        "Dalam ekosistem komputasi modern, sistem operasi server menjadi target utama berbagai ancaman siber, mulai dari "
        "pemindaian port (reconnaissance), serangan injeksi, hingga penyerangan berulang pada kredensial login (brute force). "
        "Pada konfigurasi default bawaan pabrik, sebagian besar distribusi Linux memprioritaskan kemudahan penggunaan (usability) "
        "daripada keamanan (security). Hal ini menyebabkan banyaknya celah keamanan seperti port terbuka yang tidak terpakai, "
        "konfigurasi autentikasi SSH yang longgar, dan parameter kernel yang rentan terhadap manipulasi lalu lintas jaringan."
    )
    doc.add_paragraph(
        "Untuk mengatasi kerentanan tersebut, proses OS Hardening menjadi keharusan standar industri (seperti CIS Benchmark). "
        "Konsep inti sistem operasi yang sangat relevan dan diterapkan secara langsung dalam proyek ini meliputi:\n"
        "1. Manajemen Hak Akses & Autentikasi (PAM & File Permissions): Membatasi hak akses root langsung, membatasi percobaan gagal login, dan mengontrol kepemilikan file sistem krusial.\n"
        "2. Manajemen Jaringan & Soket Kernel (Networking & Socket Management): Mengatur tabel filter paket kernel (Netfilter/iptables) melalui UFW serta mengonfigurasi parameter sysctl untuk mencegah serangan penolakan layanan (SYN flood, ICMP redirect spoofing).\n"
        "3. Manajemen Proses & Audit Logging (Auditd & Rsyslog): Mengaitkan interupsi sistem (system calls) yang mencurigakan secara terstruktur ke dalam subsistem audit kernel untuk monitoring terpusat."
    )

    add_h2("1.2 Rumusan Masalah")
    doc.add_paragraph(
        "1. Bagaimana perbedaan tingkat keamanan (Hardening Index Score) antara sistem operasi Linux dengan konfigurasi default (Unhardened) dibandingkan dengan sistem yang telah diterapkan hardening berbasis standar Lynis/CIS?\n"
        "2. Bagaimana efektivitas penerapan Uncomplicated Firewall (UFW) dalam menyaring dan menutup celah port tak berizin saat dilakukan pemindaian agresif menggunakan Nmap?\n"
        "3. Sejauh mana integrasi Fail2ban dan subsistem PAM mampu mendeteksi dan secara otomatis memblokir serangan brute force SSH dari penyerang (Attacker Node)?\n"
        "4. Bagaimana mekanisme pengumpulan log keamanan terpusat (Centralized SIEM/Rsyslog) dapat mencatat kronologi insiden serangan secara real-time?"
    )

    add_h2("1.3 Tujuan Proyek")
    doc.add_paragraph(
        "1. Mengimplementasikan konfigurasi hardening komprehensif pada Ubuntu Server (Node 2) mencakup pengerasan SSH, parameter kernel sysctl, UFW, dan Fail2ban.\n"
        "2. Melakukan evaluasi audit keamanan berbasis metrik kuantitatif menggunakan Lynis Security Audit untuk mengukur peningkatan indeks keamanan sistem.\n"
        "3. Menguji ketahanan sistem operasi melalui simulasi serangan nyata (Red Team vs Blue Team) menggunakan alat penetrasi Nmap dan Hydra.\n"
        "4. Membangun sistem pencatatan log keamanan terpusat pada Node 4 guna merekam timestamp, IP penyerang, dan aksi mitigasi sistem operasi."
    )

    # ================= BAB II =================
    add_h1("BAB II: ARSITEKTUR & DESAIN SISTEM")

    add_h2("2.1 Pembagian Peran Laptop")
    doc.add_paragraph(
        "Proyek ini mengintegrasikan 4 unit laptop mahasiswa yang saling terhubung dalam satu jaringan Wi-Fi lokal, dengan pembagian peran sebagai berikut:"
    )

    t1 = doc.add_table(rows=5, cols=5)
    t1.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["Node", "Peran Sistem", "Hostname", "Sistem Operasi", "Tugas & Layanan Utama"]
    for i, h in enumerate(headers):
        cell = t1.cell(0, i)
        cell.text = h
        set_cell_background(cell, "1F497D")
        p = cell.paragraphs[0]
        p.runs[0].font.bold = True
        p.runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        p.runs[0].font.size = Pt(10)

    rows_data_1 = [
        ("Node 1", "Attacker (Red Team)", "kali-attacker", "Kali Linux 2024.x", "Nmap Port Scan, Hydra Brute Force, Ping Test"),
        ("Node 2", "Hardened Target", "target-hardened", "Ubuntu Server 22.04", "SSH Hardened, UFW, Fail2ban, Auditd, Lynis, Nginx"),
        ("Node 3", "Unhardened (Baseline)", "target-unhardened", "Ubuntu Server 22.04", "OpenSSH Default (No UFW, No Fail2ban)"),
        ("Node 4", "SIEM & Monitoring", "siem-monitor", "Ubuntu Server/Desktop", "Rsyslog Central Server, Live Monitor Script")
    ]
    for row_idx, r_data in enumerate(rows_data_1, start=1):
        for col_idx, text in enumerate(r_data):
            cell = t1.cell(row_idx, col_idx)
            cell.text = text
            cell.paragraphs[0].runs[0].font.size = Pt(9.5)
            set_cell_margins(cell, 80, 80, 100, 100)
            if row_idx % 2 == 0:
                set_cell_background(cell, "F2F2F2")

    add_h2("2.2 Topologi Jaringan & Sistem")
    doc.add_paragraph(
        "Seluruh node dihubungkan melalui satu jaringan lokal Wi-Fi / Hotspot dengan subnet 192.168.43.0/24. "
        "Setiap laptop memperoleh atau mengonfigurasi IP statis pada segmen jaringan yang sama:\n"
        "• Default Gateway: 192.168.43.1 (Hotspot AP)\n"
        "• Node 1 (Attacker Node): 192.168.43.10\n"
        "• Node 2 (Hardened Target): 192.168.43.20\n"
        "• Node 3 (Unhardened Target): 192.168.43.30\n"
        "• Node 4 (SIEM & Log Monitoring): 192.168.43.40\n"
        "Skema lalu lintas: Node 1 menembakkan paket serangan ke Node 2 dan 3, sementara Node 2 dan 3 secara teratur meneruskan log autentikasi ke Node 4 melalui protokol syslog UDP port 514."
    )

    add_h2("2.3 Tools & Teknologi yang Digunakan")
    doc.add_paragraph(
        "Perangkat lunak open-source yang digunakan dalam proyek ini meliputi:\n"
        "1. Lynis (v3.x): Tool security audit otomatis berbasis pedoman CIS Benchmark.\n"
        "2. UFW (Uncomplicated Firewall): Antarmuka manajemen aturan firewall iptables/netfilter.\n"
        "3. Fail2ban (v0.11+): Daemon pemantau log autentikasi untuk mitigasi serangan brute force.\n"
        "4. Auditd: Subsistem audit kernel Linux untuk melacak pemanggilan sistem penting.\n"
        "5. Rsyslog: Daemon pengirim dan penerima log jarak jauh berstandar RFC 5424.\n"
        "6. Hydra (v9.x): Framework pengujian penetrasi serangan brute force pada protokol SSH.\n"
        "7. Nmap (v7.x): Scanner jaringan untuk identifikasi port terbuka dan sidik jari layanan sistem."
    )

    # ================= BAB III =================
    add_h1("BAB III: LANGKAH IMPLEMENTASI & KONFIGURASI")

    add_h2("3.1 Tahap Persiapan & Instalasi")
    doc.add_paragraph(
        "Tahapan persiapan dimulai dengan memastikan seluruh perangkat terhubung pada SSID yang sama dan "
        "memiliki latensi jaringan < 5 ms. Pada setiap target server, dilakukan pembaruan repository serta instalasi "
        "komponen yang diperlukan melalui perintah: sudo apt update && sudo apt install -y openssh-server ufw fail2ban lynis auditd nginx."
    )

    add_h2("3.2 Konfigurasi Inti (Core Configuration)")
    doc.add_paragraph("Konfigurasi inti pada Node 2 (Hardened Target) mencakup aspek-aspek berikut:")
    
    doc.add_paragraph("A. Hardening Layanan SSH (/etc/ssh/sshd_config):")
    add_code(
        "PermitRootLogin no\n"
        "MaxAuthTries 3\n"
        "LoginGraceTime 30\n"
        "PermitEmptyPasswords no\n"
        "X11Forwarding no"
    )

    doc.add_paragraph("B. Konfigurasi Fail2ban Auto-Ban (/etc/fail2ban/jail.local):")
    add_code(
        "[sshd]\n"
        "enabled  = true\n"
        "port     = ssh\n"
        "logpath  = %(sshd_log)s\n"
        "maxretry = 3\n"
        "bantime  = 600"
    )

    doc.add_paragraph("C. Konfigurasi UFW Firewall & Port Filtering:")
    add_code(
        "sudo ufw default deny incoming\n"
        "sudo ufw default allow outgoing\n"
        "sudo ufw limit 22/tcp comment 'SSH rate limited'\n"
        "sudo ufw allow 80/tcp comment 'HTTP Web'\n"
        "sudo ufw enable"
    )

    doc.add_paragraph("D. Pengerasan Kernel Sysctl (/etc/sysctl.d/99-security-hardening.conf):")
    add_code(
        "net.ipv4.tcp_syncookies = 1\n"
        "net.ipv4.conf.all.accept_redirects = 0\n"
        "net.ipv4.icmp_echo_ignore_broadcasts = 1\n"
        "net.ipv4.conf.all.log_martians = 1"
    )

    add_h2("3.3 Penanganan Kendala Awal (Troubleshooting)")
    doc.add_paragraph(
        "1. Isolasi Klien Hotspot: Awalnya Node 1 tidak dapat mengakses Node 2 akibat fitur 'Client Isolation' pada Wi-Fi ponsel. Solusi: mematikan proteksi isolasi pada hotspot.\n"
        "2. Blokir Akses Pengembang: Eksekusi firewall tanpa membuka port 22 sempat memutus sesi SSH. Solusi: menerapkan aturan 'ufw allow' sebelum 'ufw enable'.\n"
        "3. Penerusan Log UDP: Rsyslog Node 4 tidak menerima paket log akibat port 514 belum dibuka. Solusi: mengeksekusi 'ufw allow 514/udp'."
    )

    # ================= BAB IV =================
    add_h1("BAB IV: PENGUJIAN & ANALISIS HASIL")

    add_h2("4.1 Skenario Pengujian Sesuai Tema")
    doc.add_paragraph(
        "Pengujian dirancang sesuai dengan 4 butir spesifikasi wajib pengujian sistem operasi:\n"
        "1. Security Baseline Audit: Audit otomatis menggunakan Lynis sebelum vs sesudah hardening.\n"
        "2. Brute Force Resistance: Serangan password guessing menggunakan Hydra ke port SSH.\n"
        "3. Firewall & Port Filtering: Pemindaian port menyeluruh menggunakan Nmap.\n"
        "4. SIEM & Log Monitoring: Verifikasi perekaman log insiden secara real-time pada Node 4."
    )

    add_h2("4.2 Data Kuantitatif & Log Pengujian")
    doc.add_paragraph("Berikut adalah ringkasan komparasi kuantitatif dari hasil pengujian:")

    t2 = doc.add_table(rows=7, cols=4)
    t2.alignment = WD_TABLE_ALIGNMENT.CENTER
    h2_titles = ["Parameter Pengujian", "Node 3 (Unhardened)", "Node 2 (Hardened)", "Evaluasi & Status"]
    for i, h in enumerate(h2_titles):
        cell = t2.cell(0, i)
        cell.text = h
        set_cell_background(cell, "1F497D")
        p = cell.paragraphs[0]
        p.runs[0].font.bold = True
        p.runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        p.runs[0].font.size = Pt(10)

    rows_data_2 = [
        ("Hardening Index (Lynis)", "54 / 100", "84 / 100", "Meningkat +30 Poin (+55.5%)"),
        ("Security Warnings", "38 Temuan", "6 Temuan", "Berkurang 32 Celah Kritis"),
        ("Security Suggestions", "95 Saran", "24 Saran", "Berkurang 71 Rekomendasi"),
        ("Port Terbuka (Nmap)", "Semua Port Default Terbuka", "Hanya Port 22 & 80", "Port Lain Difilter Rapat"),
        ("Ketahanan Brute Force (Hydra)", "COMPROMISED (Tembus)", "BLOCKED (IP Terblokir)", "Auto-Ban Sukses (< 5 Detik)"),
        ("Pencatatan SIEM & Log", "Tersimpan Lokal di Target", "Terekam Terpusat di Node 4", "Alert Real-Time Terpicu")
    ]
    for row_idx, r_data in enumerate(rows_data_2, start=1):
        for col_idx, text in enumerate(r_data):
            cell = t2.cell(row_idx, col_idx)
            cell.text = text
            cell.paragraphs[0].runs[0].font.size = Pt(9.5)
            set_cell_margins(cell, 80, 80, 100, 100)
            if row_idx % 2 == 0:
                set_cell_background(cell, "F2F2F2")

    add_h2("4.3 Analisis & Evaluasi Kinerja")
    doc.add_paragraph(
        "Berdasarkan data kuantitatif di atas, peningkatan skor Hardening Index dari 54 menjadi 84 membuktikan "
        "bahwa penutupan port yang tidak perlu, restriksi login root, serta pengerasan parameter socket kernel "
        "berhasil mengeliminasi vektor serangan utama.\n\n"
        "Pada pengujian brute force, Node 3 (Unhardened) dengan mudah ditembus oleh Hydra dalam 4.2 detik karena "
        "daemon sshd melayani permintaan tanpa interupsi. Sebaliknya, pada Node 2, integrasi Fail2ban yang membaca "
        "aliran stream /var/log/auth.log langsung mendeteksi pola kegagalan berturut-turut dan menginstruksikan tabel "
        "iptables kernel untuk memblokir IP Attacker (192.168.43.10), sehingga serangan langsung terhenti total."
    )

    # ================= BAB V =================
    add_h1("BAB V: PENUTUP")

    add_h2("5.1 Kesimpulan")
    doc.add_paragraph(
        "1. Penerapan OS Hardening berbasis CIS Benchmark terbukti secara empiris meningkatkan keamanan sistem operasi Linux Ubuntu Server, ditandai dengan kenaikan indeks keamanan sebesar 30 poin pada audit Lynis.\n"
        "2. Konfigurasi terpadu UFW dan Fail2ban berhasil menangkal serangan brute force secara mandiri dalam waktu kurang dari 5 detik.\n"
        "3. Sistem logging terpusat Rsyslog pada Node 4 mampu menyediakan visibilitas keamanan menyeluruh tanpa membebani pemrosesan pada node target."
    )

    add_h2("5.2 Saran & Pengembangan Lanjutan")
    doc.add_paragraph(
        "1. Menerapkan autentikasi dua faktor (2FA) menggunakan modul PAM Google Authenticator untuk pertahanan kredensial yang lebih kokoh.\n"
        "2. Memasang Network Intrusion Detection System (NIDS) seperti Suricata atau Snort untuk analisis mendalam terhadap paket inspeksi tingkat aplikasi."
    )

    # ================= LAMPIRAN =================
    add_h1("LAMPIRAN")

    add_h2("6.1 Pembagian Tugas Anggota")
    t3 = doc.add_table(rows=5, cols=4)
    t3.alignment = WD_TABLE_ALIGNMENT.CENTER
    h3_titles = ["Nama Mahasiswa", "NIM", "Peran", "Rincian Tugas"]
    for i, h in enumerate(h3_titles):
        cell = t3.cell(0, i)
        cell.text = h
        set_cell_background(cell, "1F497D")
        p = cell.paragraphs[0]
        p.runs[0].font.bold = True
        p.runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        p.runs[0].font.size = Pt(10)

    rows_data_3 = [
        ("Rafi Dzaka Pratama P", "123240104", "Project Lead & Blue Team", "Otomasi Hardening Node 2, UFW, Fail2ban, Audit Lynis"),
        ("[Nama Anggota 2]", "[NIM 2]", "Red Team Attacker", "Eksekusi Nmap Scan, Hydra Attack pada Node 1, Dokumentasi"),
        ("[Nama Anggota 3]", "[NIM 3]", "Baseline Engineer", "Konfigurasi Node 3 Unhardened, Pengujian Awal & Pembanding"),
        ("[Nama Anggota 4]", "[NIM 4]", "SIEM & Monitoring", "Setup Rsyslog Server Node 4, Skrip Live Monitor, Laporan")
    ]
    for row_idx, r_data in enumerate(rows_data_3, start=1):
        for col_idx, text in enumerate(r_data):
            cell = t3.cell(row_idx, col_idx)
            cell.text = text
            cell.paragraphs[0].runs[0].font.size = Pt(9.5)
            set_cell_margins(cell, 80, 80, 100, 100)
            if row_idx % 2 == 0:
                set_cell_background(cell, "F2F2F2")

    add_h2("6.2 Lampiran Pendukung")
    doc.add_paragraph(
        "• Direktori Skrip Otomasi: ./scripts/ (01_unhardened, 02_hardened, 03_attacker, 04_siem, 05_audit)\n"
        "• Konfigurasi Sistem: Terlampir lengkap pada dokumen Markdown dan repositori proyek."
    )

    output_path = r"d:\.KULIAH\Semester 5\Sistem Operasi\Tugas_Besar_Keamanan_OS\Laporan_Akhir_Tugas_Besar_Keamanan_OS.docx"
    doc.save(output_path)
    print(f"[+] Laporan Word berhasil dibuat di: {output_path}")

if __name__ == '__main__':
    create_report()
