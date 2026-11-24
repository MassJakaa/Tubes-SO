#!/bin/bash
# ==============================================================================
# SKRIP MULTI-NODE CYBERSHIELD SOC WEB DASHBOARD
# Untuk Laptop 1, Laptop 2, Laptop 3, dan Laptop 4
# ==============================================================================

ROLE=$1

if [ -z "$ROLE" ]; then
    clear
    echo "=========================================================="
    echo "   CYBERSHIELD MULTI-NODE WEB DASHBOARD LAUNCHER          "
    echo "=========================================================="
    echo " Pilih peran untuk laptop ini:"
    echo "  1) Laptop 1: Attacker Control Center (Red Team)"
    echo "  2) Laptop 2: Hardened Target Console (Blue Team)"
    echo "  3) Laptop 3: Unhardened Baseline Monitor"
    echo "  4) Laptop 4: Centralized SIEM & Log Hub"
    echo "=========================================================="
    read -p "Masukkan pilihan Anda [1-4] (default: 2): " ROLE
    ROLE=${ROLE:-2}
fi

echo "=========================================================="
echo " [1/2] Menyiapkan Dependensi Web Dashboard..."
echo "=========================================================="

sudo apt update -y > /dev/null 2>&1
sudo apt install -y python3-flask python3-psutil > /dev/null 2>&1

# Buka firewall port 5000 jika UFW aktif
sudo ufw allow 5000/tcp comment 'CyberShield Web Dashboard' > /dev/null 2>&1

IP_LOCAL=$(hostname -I | awk '{print $1}')

echo "=========================================================="
echo " [2/2] Menyalakan Dashboard Node $ROLE..."
echo "=========================================================="
echo ""
echo "🚀 WEB DASHBOARD BERHASIL AKTIF DI LAPTOP INI!"
echo ""
echo "Buka Google Chrome atau Microsoft Edge di laptop Anda:"
echo "👉 http://$IP_LOCAL:5000?role=$ROLE"
echo ""
echo "Catatan: Di browser, Anda juga bisa mengklik tab di bagian atas"
echo "untuk melihat tampilan layar milik Laptop 1, 2, 3, atau 4!"
echo "=========================================================="
echo "Tekan Ctrl+C untuk mematikan dashboard jika sudah selesai."
echo "=========================================================="

export NODE_ROLE=$ROLE
python3 app.py
