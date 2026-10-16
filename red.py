import socket
base = "192.168.1."
for i in [1, 254, 100, 50]:
    ip = base + str(i)
    print(f"\n--- {ip} ---")
    for p in [22,80,443,8080,53]:
        s=socket.socket()
        s.settimeout(0.5)
        try:
            s.connect((ip,p))
            print(f"  ABIERTO {p}")
            s.close()
        except:
            pass
print("\n--- Fin ---")
