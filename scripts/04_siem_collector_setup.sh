#!/bin/bash
# ==============================================================================
# SKRIP SETUP: NODE 4 - SIEM & LOG MONITORING SERVER
# Mata Kuliah: Sistem Operasi
# ==============================================================================

if [ "$EUID" -ne 0 ]; then
  echo "[!] Jalankan skrip ini sebagai root (sudo bash 04_siem_collector_setup.sh)"
  exit 1
fi

echo "=========================================================="
echo " [1/3] Mengonfigurasi Rsyslog Server sebagai Log Collector..."
echo "=========================================================="

apt-get update -y
apt-get install -y rsyslog ufw net-tools

# Aktifkan penerimaan log via UDP & TCP pada port 514
RSYSLOG_CONF="/etc/rsyslog.conf"
sed -i 's/^#*module(load="imudp")/module(load="imudp")/' $RSYSLOG_CONF
sed -i 's/^#*input(type="imudp" port="514")/input(type="imudp" port="514")/' $RSYSLOG_CONF
sed -i 's/^#*module(load="imtcp")/module(load="imtcp")/' $RSYSLOG_CONF
sed -i 's/^#*input(type="imtcp" port="514")/input(type="imtcp" port="514")/' $RSYSLOG_CONF

# Buat template penyimpanan log dari client eksternal berdasarkan IP
cat << 'EOF' > /etc/rsyslog.d/30-remote-clients.conf
$template RemoteLogs,"/var/log/remote/%HOSTNAME%/%PROGRAMNAME%.log"
*.* ?RemoteLogs
& ~
EOF

# Buka firewall untuk port syslog 514
ufw allow 514/udp comment 'Rsyslog UDP'
ufw allow 514/tcp comment 'Rsyslog TCP'

systemctl restart rsyslog
echo "[+] Rsyslog Server Aktif pada Port 514 UDP/TCP."

echo "=========================================================="
echo " [2/3] Membuat Skrip Live Security Event Monitor..."
echo "=========================================================="
cat << 'EOF' > /usr/local/bin/monitor-serangan
#!/bin/bash
clear
echo "=========================================================="
echo "   LIVE SECURITY INCIDENT & SIEM MONITOR (NODE 4)         "
echo "=========================================================="
echo " Menunggu event log dari Node 2 (Hardened) & Node 3...    "
echo " Menampilkan deteksi Brute Force SSH, Ban Fail2ban, dll   "
echo " Tekan Ctrl+C untuk berhenti                              "
echo "=========================================================="
tail -n 25 -F /var/log/remote/*/*.log /var/log/syslog 2>/dev/null | grep --line-buffered -E "Failed password|Accepted password|Ban|Unban|Invalid user|POSSIBLE BREAK-IN"
EOF

chmod +x /usr/local/bin/monitor-serangan

echo "=========================================================="
echo " [SELESAI] Node 4 Siap Menerima Log!"
echo " IP Node 4: $(hostname -I | awk '{print $1}')"
echo ""
echo " CATATAN UNTUK NODE 2 & NODE 3:"
echo " Agar log dikirim ke Node 4, tambahkan baris berikut di /etc/rsyslog.conf Node 2 & 3:"
echo " *.* @$(hostname -I | awk '{print $1}'):514"
echo " lalu jalankan: sudo systemctl restart rsyslog"
echo ""
echo " Untuk memantau serangan secara real-time saat demo:"
echo " Jalankan perintah: sudo monitor-serangan"
echo "=========================================================="
