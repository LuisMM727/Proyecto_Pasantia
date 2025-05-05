from flask import Flask, render_template, send_file
from modulos.funciones import obtener_marcacion, obtener_usuarios, generate_pdf_file

app = Flask(__name__)

@app.route("/")
@app.route("/inicio")
def usuarios():
    usuarios = obtener_usuarios()
    return render_template("index.html", usuarios=usuarios)


@app.route('/generate-pdf')
def generate_pdf():

    usuarios = obtener_usuarios()

    pdf_file = generate_pdf_file(usuarios)
    return send_file(pdf_file, as_attachment=True, download_name='reporte_usuarios.pdf')


@app.route("/marcados")
def marcados():
    marcacion = obtener_marcacion()

    return render_template("marcacion.html", marcacion=marcacion)




if __name__ == "__main__":
    app.run(debug=True)