from flask import Flask, request
import os, requests
from datetime import datetime

app = Flask(__name__)
BASE = os.path.abspath("paginas")

def get_geo(ip):
    if ip.startswith("127.") or ip.startswith("192.168."):
        return "Local-Test"
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}?fields=country,city", timeout=3).json()
        return f"{r.get('country','?')} / {r.get('city','?')}"
    except:
        return "Geo-No-Disponible"

def log_ip():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0].strip()
    device = request.headers.get('User-Agent', 'Desconocido')[:90]
    ruta = request.full_path
    hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    geo = get_geo(ip)
    es_ataque = '..' in ruta or 'etc/passwd' in ruta or '%2e' in ruta.lower()
    prefijo = f"[{hora}] {'[ALERTA ATAQUE LFI]' if es_ataque else '[ACCESO NORMAL]'}"
    linea = f"{prefijo} IP: {ip} ({geo}) - Ruta: {ruta} - Device: {device}\n"
    print(linea.strip())
    with open("/data/data/com.termux/files/home/ip_log.txt", "a") as f:
        f.write(linea)

@app.before_request
def before():
    log_ip()

@app.route('/')
def index():
    page = request.args.get('page', 'inicio.txt')
    if '..' in page or page.startswith('/'):
        return "<h2>Bloqueado</h2><p>Intento LFI detectado y registrado</p>"
    ruta = os.path.join(BASE, page)
    try:
        with open(ruta, 'r') as f:
            contenido = f.read()
    except:
        contenido = "No existe"
    return f"<h2>Lab SEGURO v4 - GeoIP Activo</h2><p>{contenido}</p><form><input name=page><input type=submit></form>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8083)
