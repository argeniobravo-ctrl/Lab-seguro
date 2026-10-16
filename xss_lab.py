from flask import Flask, request, render_template_string
app = Flask(__name__)
comentarios = []
@app.route("/", methods=['GET','POST'])
def index():
    if request.method == 'POST':
        comentarios.append(request.form.get('msg',''))
    html = """
    <h2>Deja un comentario</h2>
    <form method=POST><input name=msg><input type=submit></form>
    <h3>Comentarios:</h3>
    {% for c in coms %}<p>{{c|safe}}</p>{% endfor %}
    """
    return render_template_string(html, coms=comentarios)
app.run(host='0.0.0.0', port=8083)
