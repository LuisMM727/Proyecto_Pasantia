from flask import Flask, render_template, request, redirect, session, url_for, flash
from modulos.conexionDB import conexion as con
from werkzeug.security import check_password_hash
from modulos.funciones import obtener_marcacion, Capturar_DatosZK, dispositivo_ZK, obtener_dispositivos, obtener_empleados, obtener_horarios, obtener_departamentos, obtener_usuarios
from modulos.generate_zk_testdata import data
app = Flask(__name__)
app.secret_key = 'clave'

#Pantalla login
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        password = request.form['password']

        cursor = con.cursor()
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

        con.close()

    return render_template('login.html')

#Pantalla index-Home
@app.route('/index', methods=['GET', 'POST'])
def index():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        accion = request.form.get('accion')
        if accion == 'conectar':    
            ip = request.form.get('ip_dispositivo')
            puerto = request.form.get('puerto_dispositivo')
            dispositivo_ZK(ip, puerto)
            flash("Conectado al dispositivo")

        elif accion == 'actualizar_todo':
            Capturar_DatosZK(data)
            flash("Todos los dispositivos actualizados correctamente.")

    return render_template("index.html")


#Pantalla de dispositivos
@app.route('/dispositivos')
def dispositivos():
    dispositivos = obtener_dispositivos()
    if 'usuario' not in session:
        return redirect(url_for('login'))
    return render_template("dispositivos.html", dispositivos=dispositivos)


#Pantalla de marcacion
@app.route('/marcacion')
def marcacion():
    marcacion = obtener_marcacion()
    if 'usuario' not in session:
        return redirect(url_for('login'))
    return render_template("marcacion.html", marcacion=marcacion)

#Pantalla de empleados
@app.route('/empleados')
def empleados():
    empleados = obtener_empleados()
    if 'usuario' not in session:
        return redirect(url_for('login'))
    return render_template("empleados.html", empleados=empleados)

#Pantalla de horarios
@app.route('/horarios')
def horarios():
    horarios = obtener_horarios()
    if 'usuario' not in session:
        return redirect(url_for('login'))
    return render_template("horarios.html", horarios=horarios)

#Pantalla de departamentos
@app.route('/departamentos')
def departamentos():
    departamentos = obtener_departamentos()
    if 'usuario' not in session:
        return redirect(url_for('login'))
    return render_template("departamentos.html", departamentos=departamentos)

#Pantalla de usuarios
@app.route('/usuarios')
def usuarios():
    usuarios = obtener_usuarios()
    if 'usuario' not in session:
        return redirect(url_for('login'))
    return render_template("usuarios.html", usuarios=usuarios)

#Pantalla logout
@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)


