from flask import Flask, render_template, request, Response, send_file
from io import BytesIO
from reportlab.pdfgen import canvas
import pymysql

app = Flask(__name__)

def obtener_conexion():
    return pymysql.connect(host='localhost', user='root', password='', db='marcador')

def generate_pdf_file(usuarios):

    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    p.drawString(100, 750, "reporte")
    y = 700

    for book in usuarios:
        p.drawString(100, y, f"usuarios: {book}")

        y -= 60
 
    p.showPage()
    p.save()
 
    buffer.seek(0)
    return buffer

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
    cursor.close()
    conexion.close()
    return usuarios

@app.route('/generate-pdf')
def generate_pdf():

    usuarios = obtener_usuarios()

    pdf_file = generate_pdf_file(usuarios)
    return send_file(pdf_file, as_attachment=True, download_name='reporte_usuarios.pdf')


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
    cursor.close()
    conexion.close()
    return marcacion





if __name__ == "__main__":
    app.run(debug=True)