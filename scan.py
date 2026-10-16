import socket
ip = input("IP: ")
print(f"\n--- Escaneando {ip} ---")
try:
    host = socket.gethostbyaddr(ip)[0]
    print(f"Hostname: {host}")
except:
    print("Hostname: no tiene")

puertos = [21,22,23,25,53,80,110,135,139,443,445,3306,8080]
for p in puertos:
    s = socket.socket()
    s.settimeout(0.5)
    try:
        s.connect((ip, p))
        print(f"[ABIERTO] {p}")
        s.close()
    except:
        pass
print("--- Fin ---")
