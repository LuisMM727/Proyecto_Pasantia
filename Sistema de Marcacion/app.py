from flask import Flask, render_template, request, redirect, session, url_for, flash
from modulos.conexionDB import conexion as con

from werkzeug.security import check_password_hash
from modulos.funciones import (
    obtener_marcacion, Capturar_DatosZK, dispositivo_ZK, obtener_dispositivos,
    obtener_empleados, obtener_horarios, obtener_departamentos, obtener_usuarios,
    obtener_empleado_Formulario, actualizar_empleado, empleados_formulario
)
from modulos.generate_zk_testdata import data

app = Flask(__name__)
app.secret_key = 'clave_super_secreta'

# Pantalla login
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        password = request.form['password']

        cursor = con.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE nombre_usuario = %s", (usuario,))
        datos = cursor.fetchone()
        cursor.close()

        if datos:
            if check_password_hash(datos['password_usuario'], password):
                session['usuario'] = datos['nombre_usuario']
                return redirect(url_for('index'))
            else:
                flash('Contraseña incorrecta', 'danger')
        else:
            flash('Usuario no encontrado', 'danger')

    return render_template('login.html')

# Pantalla index-Home
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
            flash("Conectado al dispositivo", 'success')

        elif accion == 'actualizar_todo':
            Capturar_DatosZK()
            #flash("Todos los dispositivos actualizados correctamente.", 'success')

    return render_template("index.html")

# Pantalla de dispositivos
@app.route('/dispositivos')
def dispositivos():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    dispositivos = obtener_dispositivos()
    return render_template("dispositivos.html", dispositivos=dispositivos)

# Pantalla de marcacion
@app.route('/marcacion')
def marcacion():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    marcacion = obtener_marcacion()
    return render_template("marcacion.html", marcacion=marcacion)

# Pantalla de empleados
@app.route('/empleados')
def empleados():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    empleados = obtener_empleados()
    return render_template("empleados.html", empleados=empleados)

# Pantalla agregar empleados
@app.route('/agregar_empleado', methods=['GET', 'POST'])
def agregar_empleado():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        id_empleado = request.form['id']
        nombre = request.form['nombre']
        departamento = request.form['departamento']
        empleados_formulario(id_empleado, nombre, departamento)
        flash('Empleado agregado correctamente', 'success')
        return redirect(url_for('empleados'))

    return render_template('agregar_empleados.html')

# Pantalla para editar empleados
@app.route('/editar_empleado/<int:id>', methods=['GET', 'POST'])
def editar_empleado(id):
    if 'usuario' not in session:
        return redirect(url_for('login'))

    empleado = obtener_empleado_Formulario(id)

    if request.method == 'POST':
        id_empleado = request.form['id']
        nombre = request.form['nombre']
        activo = 1 if 'activo' in request.form else 0
        departamento = request.form['departamento']
        actualizar_empleado(id_empleado, nombre, activo, departamento)
        flash('Empleado actualizado correctamente', 'success')
        return redirect(url_for('empleados'))

    return render_template('editar_empleados.html', empleado=empleado)

# Pantalla de horarios
@app.route('/horarios')
def horarios():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    horarios = obtener_horarios()
    return render_template("horarios.html", horarios=horarios)

# Pantalla de departamentos
@app.route('/departamentos')
def departamentos():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    departamentos = obtener_departamentos()
    return render_template("departamentos.html", departamentos=departamentos)

# Pantalla de usuarios
@app.route('/usuarios')
def usuarios():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    usuarios = obtener_usuarios()
    return render_template("usuarios.html", usuarios=usuarios)

#Pantalla de Reportes
@app.route('/reportes')
def reportes():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    return render_template("reportes.html")

#Pantalla de Reportes de empleados
@app.route('/reportes_empleados')
def reportes_empleados():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    return render_template("reportes_empleados.html")

#Pantalla de Reportes de Marcaciones
@app.route('/reportes_marcacion')
def reportes_marcacion():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    return render_template("reportes_marcacion.html")








# Pantalla logout
@app.route('/logout')
def logout():
    session.pop('usuario', None)
    flash('Sesión cerrada correctamente', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
