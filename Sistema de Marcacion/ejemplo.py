from flask import Flask, render_template
from modulos.funciones import obtener_marcacion, obtener_usuarios
app = Flask(__name__)


@app.route("/")
@app.route("/inicio")
def usuarios():
    usuarios = obtener_usuarios()
    return render_template("index.html", usuarios=usuarios)


@app.route("/marcados")
def marcados():
    marcacion = obtener_marcacion()
    return render_template("marcacion.html", marcacion=marcacion)




if __name__ == "__main__":
    app.run(debug=True)