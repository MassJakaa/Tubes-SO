@echo off
:: ==============================================================================
:: SKRIP INSTALASI OTOMATIS KALI LINUX (LAPTOP 1 - ATTACKER)
:: Mata Kuliah: Sistem Operasi
:: ==============================================================================

title Setup Kali Linux - Laptop 1 Attacker

echo ================================================================
echo     SETUP KALI LINUX (LAPTOP 1: ATTACKER / RED TEAM)
echo ================================================================
echo.
echo Skrip ini akan mengaktifkan WSL dan menginstal Kali Linux resmi
echo dari Microsoft Store langsung ke laptop ini.
echo.

:: Cek apakah dijalankan sebagai Administrator
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [!] PERHATIAN:
    echo Skrip ini membutuhkan hak Administrator untuk mengaktifkan fitur WSL.
    echo.
    echo CARA MENJALANKANNYA:
    echo 1. Tutup jendela ini.
    echo 2. Klik KANAN pada file 'setup_laptop1_wsl.bat'
    echo 3. Pilih "Run as administrator" (Jalankan sebagai administrator).
    echo.
    pause
    exit /b
)

echo [*] Hak Administrator terdeteksi. Memulai instalasi Kali Linux...
echo [*] Proses ini akan mengunduh dan mengonfigurasi Kali Linux otomatis...
echo.

wsl --install -d kali-linux

if %errorLevel% equ 0 (
    echo.
    echo ================================================================
    echo [SUKSES] Kali Linux berhasil dipasang!
    echo.
    echo LANGKAH SELANJUTNYA:
    echo 1. Jika Windows meminta restart, silakan RESTART laptop Anda.
    echo 2. Setelah menyala, buka Start Menu dan cari "Kali Linux".
    echo 3. Masukkan username dan password baru yang Anda inginkan.
    echo 4. Jalankan perintah berikut di dalam terminal Kali Linux:
    echo    sudo apt update ^&^& sudo apt install -y nmap hydra
    echo ================================================================
) else (
    echo.
    echo [!] Terjadi kendala saat instalasi otomatis.
    echo Silakan coba jalankan perintah manual di PowerShell (Run as Administrator):
    echo wsl --install -d kali-linux
)

echo.
pause
