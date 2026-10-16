from flask import Flask, request
import sqlite3, os
app = Flask(__name__)
DB="sqli.db"
if os.path.exists(DB): os.remove(DB)
con=sqlite3.connect(DB)
con.execute("CREATE TABLE users (id INT, username TEXT, password TEXT)")
con.execute("INSERT INTO users VALUES (1,'admin','admin123')")
con.execute("INSERT INTO users VALUES (2,'dany','pass123')")
con.commit()
con.close()

@app.route("/")
def index():
    user = request.args.get('id', '1')
    con=sqlite3.connect(DB)
    # VULNERABLE - concatenando directo
    query = f"SELECT * FROM users WHERE id = {user}"
    print(f"[SQL] {query}")
    try:
        res = con.execute(query).fetchall()
    except Exception as e:
        res = [f"Error SQL: {e}"]
    con.close()
    return f"""
    <h2>SQLi Lab Vulnerable</h2>
    <p>Query: <code>{query}</code></p>
    <p>Resultado: {res}</p>
    <hr>
    <p>Prueba:</p>
    <ul>
    <li><a href='/?id=1'>/?id=1 (normal)</a></li>
    <li><a href='/?id=1 OR 1=1'>/?id=1 OR 1=1 (inyección)</a></li>
    <li><a href='/?id=0 UNION SELECT 1,2,3'>/?id=0 UNION SELECT 1,2,3</a></li>
    </ul>
    <form><input name=id placeholder="pon tu payload"><input type=submit></form>
    """

app.run(host='0.0.0.0', port=8083)
