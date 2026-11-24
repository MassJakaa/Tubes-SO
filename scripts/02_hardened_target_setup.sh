#!/bin/bash
# ==============================================================================
# SKRIP SETUP: NODE 2 - HARDENED TARGET (SISTEM YANG DIAMANKAN)
# Mata Kuliah: Sistem Operasi
# ==============================================================================

if [ "$EUID" -ne 0 ]; then
  echo "[!] Jalankan skrip ini sebagai root (sudo bash 02_hardened_target_setup.sh)"
  exit 1
fi

echo "=========================================================="
echo " [1/6] Memperbarui Repositori & Menginstal Paket Keamanan..."
echo "=========================================================="
apt-get update -y
apt-get install -y openssh-server ufw fail2ban auditd audispd-plugins lynis nginx curl net-tools libpam-tmpdir

# -------------------------------------------------------------
# 1. SSH HARDENING
# -------------------------------------------------------------
echo "=========================================================="
echo " [2/6] Menerapkan Hardening pada Layanan OpenSSH..."
echo "=========================================================="
SSHD_CONFIG="/etc/ssh/sshd_config"
cp $SSHD_CONFIG /etc/ssh/sshd_config.bak

# Larang login langsung sebagai root
sed -i 's/^#*PermitRootLogin.*/PermitRootLogin no/' $SSHD_CONFIG
# Batasi percobaan autentikasi maksimal 3 kali
sed -i 's/^#*MaxAuthTries.*/MaxAuthTries 3/' $SSHD_CONFIG
# Batasi waktu sesi login login grace time ke 30 detik
sed -i 's/^#*LoginGraceTime.*/LoginGraceTime 30/' $SSHD_CONFIG
# Larang password kosong
sed -i 's/^#*PermitEmptyPasswords.*/PermitEmptyPasswords no/' $SSHD_CONFIG
# Nonaktifkan X11 forwarding jika tidak dibutuhkan
sed -i 's/^#*X11Forwarding.*/X11Forwarding no/' $SSHD_CONFIG

# Buat akun pengujian (sama dengan unhardened) untuk uji brute force
USER_TEST="korban"
PASS_TEST="password123"
if id "$USER_TEST" &>/dev/null; then
    echo "$USER_TEST:$PASS_TEST" | chpasswd
else
    useradd -m -s /bin/bash "$USER_TEST"
    echo "$USER_TEST:$PASS_TEST" | chpasswd
fi

systemctl restart ssh
echo "[+] Konfigurasi SSH berhasil diperketat."

# -------------------------------------------------------------
# 2. FAIL2BAN CONFIGURATION (BRUTE FORCE RESISTANCE)
# -------------------------------------------------------------
echo "=========================================================="
echo " [3/6] Mengonfigurasi Fail2ban untuk Proteksi Brute Force..."
echo "=========================================================="
cat << 'EOF' > /etc/fail2ban/jail.local
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
EOF

systemctl enable fail2ban
systemctl restart fail2ban
echo "[+] Fail2ban aktif: Maksimal 3 kali gagal login SSH -> IP diblokir selama 10 menit."

# -------------------------------------------------------------
# 3. FIREWALL HARDENING (UFW & PORT FILTERING)
# -------------------------------------------------------------
echo "=========================================================="
echo " [4/6] Mengonfigurasi UFW Firewall & Port Filtering..."
echo "=========================================================="
ufw --force reset
ufw default deny incoming
ufw default allow outgoing

# Izinkan SSH dengan limitasi (rate-limiting untuk mencegah flooding)
ufw limit 22/tcp comment 'SSH with rate-limiting'
# Izinkan Web Server HTTP port 80
ufw allow 80/tcp comment 'Web Server HTTP'

# Aktifkan UFW
ufw --force enable
systemctl enable ufw
echo "[+] UFW Aktif! Hanya port 22 dan 80 yang terbuka."

# -------------------------------------------------------------
# 4. KERNEL PARAMETER HARDENING (SYSCTL)
# -------------------------------------------------------------
echo "=========================================================="
echo " [5/6] Menerapkan Hardening Kernel via /etc/sysctl.conf..."
echo "=========================================================="
cat << 'EOF' > /etc/sysctl.d/99-security-hardening.conf
# Perlindungan dari SYN Flood attack
net.ipv4.tcp_syncookies = 1
# Nonaktifkan packet forwarding
net.ipv4.ip_forward = 0
# Tolak ICMP redirect (mencegah manipulasi rute perutean)
net.ipv4.conf.all.accept_redirects = 0
net.ipv4.conf.default.accept_redirects = 0
net.ipv6.conf.all.accept_redirects = 0
# Abaikan ping broadcast (mencegah Smurf attack)
net.ipv4.icmp_echo_ignore_broadcasts = 1
# Catat paket spoofing/martian
net.ipv4.conf.all.log_martians = 1
# Proteksi buffer overflow melalui kernel ASLR
kernel.randomize_va_space = 2
EOF

sysctl --system > /dev/null 2>&1
echo "[+] Parameter Kernel Sysctl berhasil diperketat."

# -------------------------------------------------------------
# 5. AUDITD KERNEL MONITORING RULES
# -------------------------------------------------------------
cat << 'EOF' > /etc/audit/rules.d/hardening.rules
# Pantau perubahan akun dan file otentikasi
-w /etc/passwd -p wa -k identity
-w /etc/shadow -p wa -k identity
-w /etc/group -p wa -k identity
-w /etc/ssh/sshd_config -p wa -k sshd_config
-w /var/log/auth.log -p wa -k authlog
EOF
augenrules --load > /dev/null 2>&1
systemctl restart auditd

# -------------------------------------------------------------
# 6. MENJALANKAN LYNIS POST-HARDENING AUDIT
# -------------------------------------------------------------
echo "=========================================================="
echo " [6/6] Menjalankan Lynis Security Audit (Post-Hardening)..."
echo "=========================================================="
mkdir -p /var/log/audit-results
lynis audit system --quick --auditor "Mahasiswa-SisOp" > /var/log/audit-results/lynis_hardened.txt

echo "=========================================================="
echo " [SELESAI] Node 2 (Hardened Target) Berhasil Dikonfigurasi!"
echo " IP Node 2: $(hostname -I | awk '{print $1}')"
echo " UFW Status:"
ufw status
echo " Skor Hardening Index Hardened:"
grep -E "Hardening index" /var/log/lynis.log || grep -E "Hardening index" /var/log/audit-results/lynis_hardened.txt
echo "=========================================================="
