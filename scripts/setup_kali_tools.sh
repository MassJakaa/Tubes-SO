#!/bin/bash
# ==============================================================================
# SKRIP PERSIAPAN TOOLS KALI LINUX DI LAPTOP 1
# ==============================================================================

echo "=========================================================="
echo " [1/2] Memperbarui Repositori & Menginstal Tools Attacker..."
echo "=========================================================="

sudo apt update -y
sudo apt install -y nmap hydra net-tools curl git

echo "=========================================================="
echo " [2/2] Menyiapkan Suite Serangan (03_attacker_suite.sh)..."
echo "=========================================================="

chmod +x 03_attacker_suite.sh

echo ""
echo "[+] Tools Attacker (Nmap & Hydra) SIAP DIGUNAKAN!"
echo ""
echo "Untuk memulai pengujian, jalankan:"
echo "  ./03_attacker_suite.sh"
echo "=========================================================="
