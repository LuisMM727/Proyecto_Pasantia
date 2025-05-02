from flask import Flask, render_template, request, redirect, session, url_for, flash
import pymysql
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.secret_key = 'clave_super_secreta'

def conectar_bd():
    return pymysql.connect(host='localhost', user='root', password='', db='sistemamc', cursorclass=pymysql.cursors.DictCursor
    )

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        password = request.form['password']

        conexion = conectar_bd()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE nombre_usuario = %s", (usuario,))
        datos = cursor.fetchone()

        if datos:
            if check_password_hash(datos['password_usuario'], password):
                session['usuario'] = datos['nombre_usuario']
                return redirect(url_for('inicio'))
            else:
                flash('Contraseña incorrecta')
        else:
            flash('Usuario no encontrado')

        conexion.close()

    return render_template('login.html')

@app.route('/inicio')
def usuario():
    if 'usuario' in session:
        usuarios = obtener_usuarios()
        return f"Bienvenido, {session['usuario']} <br><a href='/logout'>Cerrar sesion</a>"
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)


