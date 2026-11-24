#!/bin/bash
# ==============================================================================
# SKRIP SETUP: NODE 3 - UNHARDENED TARGET (BASELINE PEMBANDING)
# Mata Kuliah: Sistem Operasi
# ==============================================================================

if [ "$EUID" -ne 0 ]; then
  echo "[!] Jalankan skrip ini sebagai root (sudo bash 01_unhardened_target_setup.sh)"
  exit 1
fi

echo "=========================================================="
echo " [1/4] Mempersiapkan Node 3: Unhardened Target..."
echo "=========================================================="

# Update paket
apt-get update -y

# Instal OpenSSH server dan Lynis untuk baseline audit
apt-get install -y openssh-server lynis curl net-tools

# Pastikan firewall UFW dimatikan (Unhardened)
ufw disable
systemctl stop ufw
echo "[+] Firewall UFW: DISABLED (Kondisi default rentan)"

# Buat akun pengujian dengan password lemah untuk simulasi brute force
USER_TEST="korban"
PASS_TEST="password123"

if id "$USER_TEST" &>/dev/null; then
    echo "[!] User $USER_TEST sudah ada, memperbarui password..."
    echo "$USER_TEST:$PASS_TEST" | chpasswd
else
    useradd -m -s /bin/bash "$USER_TEST"
    echo "$USER_TEST:$PASS_TEST" | chpasswd
    echo "[+] User '$USER_TEST' dibuat dengan password lemah: '$PASS_TEST'"
fi

# Konfigurasi SSH Default (Sangat longgar/tanpa proteksi)
SSHD_CONFIG="/etc/ssh/sshd_config"
sed -i 's/^#*PermitRootLogin.*/PermitRootLogin yes/' $SSHD_CONFIG
sed -i 's/^#*PasswordAuthentication.*/PasswordAuthentication yes/' $SSHD_CONFIG
sed -i 's/^#*MaxAuthTries.*/MaxAuthTries 10/' $SSHD_CONFIG

systemctl restart ssh
echo "[+] Layanan OpenSSH berjalan pada port default 22."

# Menjalankan Lynis Baseline Audit Awal
echo "=========================================================="
echo " [2/4] Menjalankan Lynis Security Baseline Audit..."
echo "=========================================================="
mkdir -p /var/log/audit-results
lynis audit system --quick --auditor "Mahasiswa-SisOp" > /var/log/audit-results/lynis_unhardened.txt

echo "=========================================================="
echo " [SELESAI] Node 3 Selesai Dikonfigurasi!"
echo " IP Node 3: $(hostname -I | awk '{print $1}')"
echo " Hasil audit Lynis tersimpan di: /var/log/audit-results/lynis_unhardened.txt"
echo " Skor Hardening Index Unhardened:"
grep -E "Hardening index" /var/log/lynis.log || grep -E "Hardening index" /var/log/audit-results/lynis_unhardened.txt
echo "=========================================================="
