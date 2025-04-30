from flask import Flask, render_template, send_file
import pymysql

app = Flask(__name__)

def obtener_conexion():
    return pymysql.connect(host='localhost', user='root', password='', db='marcador')


@app.route("/")
@app.route("/inicio")
def usuarios():
    usuarios = obtener_usuarios()
    return render_template("index.html", usuarios=usuarios)

def obtener_usuarios():
    conexion = obtener_conexion()
    usuarios = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id_user, Nombre FROM usuarios")
        usuarios = cursor.fetchall()
    conexion.close()
    return usuarios


@app.route("/marcados")
def marcados():
    marcacion = obtener_marcacion()
    return render_template("marcacion.html", marcacion=marcacion)


def obtener_marcacion():
    conexion = obtener_conexion()
    marcacion = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id_marcacion, marcacion FROM marcados")
        marcacion = cursor.fetchall()
    conexion.close()
    return marcacion






if __name__ == "__main__":
    app.run(debug=True)