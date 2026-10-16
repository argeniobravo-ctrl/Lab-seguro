from flask import Flask, request
import sqlite3
app = Flask(__name__)
DB="sqli.db"
@app.route("/")
def index():
    user = request.args.get('id', '1')
    con=sqlite3.connect(DB)
    # ARREGLADO - query parametrizada
    query = "SELECT * FROM users WHERE id = ?"
    print(f"[SQL SEGURO] {query} con valor [{user}]")
    try:
        res = con.execute(query, (user,)).fetchall()
    except Exception as e:
        res = [f"Error: {e}"]
    con.close()
    return f"""
    <h2>Lab ARREGLADO</h2>
    <p>Query: <code>{query}</code> valor = {user}</p>
    <p>Resultado: {res}</p>
    <p><i>Ahora con ? ya no ejecuta tu OR 1=1, lo toma como texto</i></p>
    <form><input name=id><input type=submit></form>
    """
app.run(host='0.0.0.0', port=8083)
