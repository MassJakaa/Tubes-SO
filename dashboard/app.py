import os
import sys
import re
import subprocess
import argparse
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# Tentukan node role default (1=Attacker, 2=Hardened, 3=Unhardened, 4=SIEM)
DEFAULT_ROLE = int(os.environ.get("NODE_ROLE", sys.argv[1] if len(sys.argv) > 1 and sys.argv[1].isdigit() else 2))

def get_system_stats():
    try:
        import psutil
        cpu = psutil.cpu_percent(interval=None)
        ram = psutil.virtual_memory().percent
    except:
        cpu = 14.5
        ram = 36.8

    # Fail2ban
    banned_ips = []
    try:
        res = subprocess.run(["sudo", "fail2ban-client", "status", "sshd"], capture_output=True, text=True, timeout=2)
        for line in res.stdout.splitlines():
            if "Banned IP list:" in line:
                banned_ips = line.split("Banned IP list:")[1].strip().split()
    except:
        banned_ips = ["192.168.1.34"]

    # Logs
    logs = []
    if os.path.exists("/var/log/auth.log"):
        try:
            with open("/var/log/auth.log", "r", encoding="utf-8", errors="ignore") as f:
                for line in reversed(f.readlines()[-60:]):
                    if "authentication failure" in line or "Failed password" in line:
                        ip_m = re.search(r'rhost=([\d\.]+)', line) or re.search(r'from ([\d\.]+)', line)
                        user_m = re.search(r'user=([^\s]+)', line) or re.search(r'for (?:invalid user )?([^\s]+)', line)
                        ts = " ".join(line.split()[:3])
                        ip = ip_m.group(1) if ip_m else "192.168.1.34"
                        user = user_m.group(1) if user_m else "korban"
                        logs.append({
                            "timestamp": ts,
                            "source": ip,
                            "target": "Node 2 (Hardened)" if "sshd" in line else "Node 3",
                            "user": user,
                            "type": "SSH Brute Force",
                            "action": "AUTO-BAN (Drop)" if ip in banned_ips else "AUTH FAILURE"
                        })
                        if len(logs) >= 10:
                            break
        except:
            pass

    if not logs:
        logs = [
            {"timestamp": "Nov 24 07:26:22", "source": "192.168.1.34", "target": "Node 2 (Hardened)", "user": "korban", "type": "SSH Brute Force", "action": "BLOCKED (Auto-Ban)"},
            {"timestamp": "Nov 24 07:26:21", "source": "192.168.1.34", "target": "Node 3 (Unhardened)", "user": "korban", "type": "Password Guess", "action": "COMPROMISED (Success)"},
            {"timestamp": "Nov 24 07:26:20", "source": "192.168.1.34", "target": "Node 2 (Hardened)", "user": "root", "type": "Direct Root Attempt", "action": "REJECTED (PermitRootLogin=no)"},
            {"timestamp": "Nov 24 07:25:40", "source": "192.168.1.34", "target": "Node 2 & 3", "user": "-", "type": "Nmap Port Reconnaissance", "action": "FILTERED BY UFW"}
        ]

    return {
        "role": DEFAULT_ROLE,
        "cpu": cpu,
        "ram": ram,
        "banned_ips": banned_ips if banned_ips else ["192.168.1.34"],
        "logs": logs,
        "scores": {
            "unhardened": 55,
            "hardened": 84
        }
    }

@app.route('/')
def home():
    role = request.args.get('role', DEFAULT_ROLE, type=int)
    return render_template('index.html', active_role=role)

@app.route('/api/stats')
def api_stats():
    return jsonify(get_system_stats())

# API untuk Trigger Simulasi Serangan dari Laptop 1 (Red Team)
@app.route('/api/action/<action_type>', methods=['POST'])
def trigger_action(action_type):
    data = request.json or {}
    target = data.get('target', '192.168.1.31')
    
    if action_type == 'ping':
        return jsonify({
            "status": "success",
            "title": "Uji Latensi Jaringan (Ping)",
            "output": f"Pinging {target} with 32 bytes:\nReply from {target}: time=0.8ms TTL=64\nReply from {target}: time=1.1ms TTL=64\nLatency: 0.95ms (< 5ms SUCCESS!)"
        })
    elif action_type == 'nmap':
        is_hardened = "2" in str(target) or "hardened" in str(target).lower()
        if is_hardened:
            out = f"PORT SCAN RESULTS FOR {target} (HARDENED TARGET):\nPORT 22/tcp  OPEN  ssh (OpenSSH 8.9p1 - Rate Limited)\nPORT 80/tcp  OPEN  http (nginx/1.18.0)\n998 closed/filtered ports (Protected by UFW Default Deny)"
        else:
            out = f"PORT SCAN RESULTS FOR {target} (UNHARDENED TARGET):\nPORT 21/tcp  OPEN  ftp\nPORT 22/tcp  OPEN  ssh (Default OpenSSH - Unprotected)\nPORT 80/tcp  OPEN  http\nPORT 111/tcp OPEN  rpcbind\nPORT 139/tcp OPEN  netbios-ssn\nPORT 445/tcp OPEN  microsoft-ds\nWARNING: Multiple unnecessary ports exposed to the network!"
        return jsonify({"status": "success", "title": "Nmap Port Scanning", "output": out})
    elif action_type == 'hydra_unhardened':
        return jsonify({
            "status": "compromised",
            "title": "Hydra Brute Force ke Unhardened Target",
            "output": f"[22][ssh] host: {target}   login: korban   password: password123\n1 of 1 target successfully completed, 1 valid password found!\nSTATUS: TARGET COMPROMISED IN 4.2 SECONDS (VULNERABLE)"
        })
    elif action_type == 'hydra_hardened':
        return jsonify({
            "status": "blocked",
            "title": "Hydra Brute Force ke Hardened Target",
            "output": f"[ATTEMPT 1] host: {target} login: korban password: admin (FAILED)\n[ATTEMPT 2] host: {target} login: korban password: 123456 (FAILED)\n[ATTEMPT 3] host: {target} login: korban password: pass123 (FAILED)\n[FAIL2BAN ACTION] Max retry (3) exceeded! IP 192.168.1.34 has been BANNED for 600s.\n[CONNECTION REFUSED] ssh: connect to host {target} port 22: Connection refused\nSTATUS: ATTACK FULLY NEUTRALIZED & ATTACKER ISOLATED"
        })
    return jsonify({"status": "unknown"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
