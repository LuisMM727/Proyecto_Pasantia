from flask import Flask, render_template, request, redirect, session, url_for, flash
from modulos.conexionDB import conexion
from werkzeug.security import check_password_hash
from modulos.funciones import obtener_marcacion
app = Flask(__name__)
app.secret_key = 'clave'


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        password = request.form['password']

        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE nombre_usuario = %s", (usuario))
        datos = cursor.fetchone()

        if datos:
            if check_password_hash(datos['password_usuario'], password):
                session['usuario'] = datos['nombre_usuario']
                return redirect(url_for('index'))
            else:
                flash('Contraseña incorrecta')
        else:
            flash('Usuario no encontrado')

        conexion.close()

    return render_template('login.html')

@app.route('/index')
def index():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    return render_template("index.html")

@app.route('/marcacion')
def marcacion():
    marcacion = obtener_marcacion()
    if 'usuario' not in session:
        return redirect(url_for('login'))
    return render_template("marcacion.html", marcacion=marcacion)



@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)


