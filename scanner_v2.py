import requests
URL = "http://127.0.0.1:8083"
print(f"[+] Scanner V2 -> {URL}\n")

hallazgos = []

# 1. XSS - solo es vuln si el payload se REFLEJA sin escapar
try:
    payload = "<script>alert(1)</script>"
    r = requests.get(f"{URL}/?q={payload}", timeout=2)
    if payload in r.text:
        print("[!] XSS CONFIRMADO - El payload se refleja tal cual")
        hallazgos.append(("XSS Reflejado", f"/?q={payload}", "Usar escape HTML / textContent"))
    else:
        print("[-] XSS no vulnerable")
except: print("[x] No conecta")

# 2. LFI - solo si lee archivo fuera
try:
    r = requests.get(f"{URL}/?page=../secreto", timeout=2)
    if "secreto" in r.text.lower() and "bloqueado" not in r.text.lower():
        print("[!] LFI CONFIRMADO - Leyendo fuera del directorio")
        hallazgos.append(("LFI / Path Traversal", "/?page=../secreto", "Validar con abspath + whitelist"))
    else:
        print("[-] LFI no vulnerable (bloqueado)")
except: print("[x] No conecta")

# Reporte
print("\n--- REPORTE ---")
if not hallazgos:
    print("✅ 0 vulnerabilidades - Sistema seguro")
else:
    for v, p, fix in hallazgos:
        print(f"- {v} en {p} | Fix: {fix}")

# Guardar reporte
with open("reporte.txt","w") as f:
    f.write(f"Reporte Scan {URL}\n")
    if not hallazgos: f.write("0 vulns - Seguro\n")
    else:
        for v,p,fix in hallazgos: f.write(f"{v} - {p} - Fix: {fix}\n")
print("\n[+] Reporte guardado en reporte.txt")
