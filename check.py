import socket
for ip in ['192.168.1.1','192.168.1.254','192.168.0.1']:
    s=socket.socket()
    s.settimeout(1)
    r=s.connect_ex((ip,80))
    print(ip, 'ABIERTO' if r==0 else 'cerrado')
