from flask import Flask, request
import os
app = Flask(__name__)
os.makedirs("paginas", exist_ok=True)
open("paginas/inicio.txt","w").write("Bienvenido al inicio")
open("paginas/contacto.txt","w").write("Email: test@test.com")
open("secreto.txt","w").write("ESTO ES SECRETO - no deberias leerlo")

@app.route("/")
def index():
    pagina = request.args.get('page', 'inicio')
    ruta = f"paginas/{pagina}.txt"
    print(f"[LFI] Intentando leer: {ruta}")
    try:
        contenido = open(ruta).read()
    except Exception as e:
        contenido = f"Error: {e}"
    return f"""
    <h2>LFI Lab Vulnerable</h2>
    <p>Leyendo: <code>{ruta}</code></p>
    <p>Contenido: {contenido}</p>
    <hr>
    <a href='/?page=inicio'>inicio</a> | <a href='/?page=contacto'>contacto</a><br><br>
    <p>Prueba atacante: /?page=../../secreto</p>
    <form><input name=page><input type=submit></form>
    """
app.run(host='0.0.0.0', port=8083)
