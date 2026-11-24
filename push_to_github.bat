@echo off
title Upload Tugas Besar ke GitHub

echo ================================================================
echo       UPLOAD TUGAS BESAR SISTEM OPERASI KE GITHUB
echo ================================================================
echo.
echo Pastikan Anda sudah membuat repository baru di https://github.com/new
echo (Beri nama misal: TugasBesar-SistemOperasi-Hardening dan pilih Public).
echo.
set /p REPO_URL="Masukkan URL Repository GitHub Anda (contoh: https://github.com/MassJakaa/TugasBesar-SistemOperasi-Hardening.git): "

if "%REPO_URL%"=="" (
    echo [!] URL tidak boleh kosong!
    pause
    exit /b
)

echo.
echo [*] Menghubungkan ke GitHub...
git remote remove origin >nul 2>&1
git remote add origin %REPO_URL%
git branch -M main

echo [*] Mengunggah semua berkas (scripts, dashboard, laporan, panduan)...
git push -u origin main

if %errorlevel% equ 0 (
    echo.
    echo ================================================================
    echo [SUKSES] Seluruh proyek berhasil di-upload ke GitHub!
    echo Cek halaman repository Anda di browser.
    echo ================================================================
) else (
    echo.
    echo [!] Terjadi kendala saat push. Pastikan repository sudah dibuat di GitHub
    echo dan akun Anda memiliki izin akses.
)

echo.
pause
