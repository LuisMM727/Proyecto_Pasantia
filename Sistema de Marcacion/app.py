from flask import Flask, render_template, request, redirect, session, url_for, flash
from modulos.conexionDB import conexion as con
from werkzeug.security import check_password_hash, generate_password_hash
from modulos.funciones import (
    obtener_marcacion, Capturar_DatosZK, dispositivo_ZK, obtener_dispositivos,
    obtener_empleados, obtener_horarios, obtener_departamentos, obtener_usuarios,
    obtener_empleado_Formulario, actualizar_empleado, empleados_formulario, dispositivo_formulario, 
    obtener_dispositivo_Formulario, actualizar_dispositivo, horarios_formulario, obtener_horario_Formulario,
    actualizar_horarios, obtener_horarios_Departamentos, departamento_formulario, obtener_departamento_Formulario,
    actualizar_departamentos, PasswordHash, usuario_formulario, actualizar_usuarios, obtener_usuarios_Formulario,
    Departamentos
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
                session['rol'] = bool(datos['rol'])  
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
            flash("Todos los dispositivos actualizados correctamente.", 'success')

    return render_template("index.html")

# Pantalla de dispositivos
@app.route('/dispositivos')
def dispositivos():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    dispositivos = obtener_dispositivos()
    return render_template("dispositivos.html", dispositivos=dispositivos)

# Pantalla agregar dispositivos
@app.route('/agregar_dispositivo', methods=['GET', 'POST'])
def agregar_dispositivo():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        descripcion = request.form['descripcion']
        nombre = request.form['nombre']
        puerto = request.form['puerto']
        ip = request.form['ip']
        dispositivo_formulario(descripcion, nombre, puerto, ip)
        flash('Dispositivo agregado correctamente', 'success')
        return redirect(url_for('dispositivos'))

    return render_template('agregar_dispositivos.html')

# Pantalla para editar dispositivos
@app.route('/editar_dispositivo/<int:id>', methods=['GET', 'POST'])
def editar_dispositivo(id):
    if 'usuario' not in session:
        return redirect(url_for('login'))

    dispositivos = obtener_dispositivo_Formulario(id)

    if request.method == 'POST':
        descripcion = request.form['descripcion']
        nombre = request.form['nombre']
        activo = 1 if 'activo' in request.form else 0
        puerto = request.form['puerto']
        ip = request.form['ip']
        actualizar_dispositivo(id, descripcion, nombre, activo, puerto, ip, )
        flash('Dispositivo actualizado correctamente', 'success')
        return redirect(url_for('dispositivos'))

    return render_template('editar_dispositivos.html', dispositivos=dispositivos)

# Pantalla de marcacion
@app.route('/marcacion')
def marcacion():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    
    usuario = session['usuario']
    marcacion = obtener_marcacion()
    return render_template("marcacion.html", marcacion=marcacion, usuario=usuario)

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

    departamentos = Departamentos()

    if request.method == 'POST':
        id_empleado = request.form['id']
        nombre = request.form['nombre']
        departamento = int(request.form['departamento'])

        empleados_formulario(id_empleado, nombre, departamento)
        flash('Empleado agregado correctamente', 'success')
        return redirect(url_for('empleados'))

    return render_template('agregar_empleados.html', departamentos=departamentos)

# Pantalla para editar empleados
@app.route('/editar_empleado/<int:id>', methods=['GET', 'POST'])
def editar_empleado(id):
    if 'usuario' not in session:
        return redirect(url_for('login'))

    empleado = obtener_empleado_Formulario(id)
    departamentos = Departamentos()

    if request.method == 'POST':
        nombre = request.form['nombre']
        activo = 1 if 'activo' in request.form else 0
        departamento = request.form['departamento']
        actualizar_empleado(id, nombre, activo, departamento)
        flash('Empleado actualizado correctamente', 'success')
        return redirect(url_for('empleados'))

    return render_template('editar_empleados.html', empleado=empleado, departamentos=departamentos)

# Pantalla de horarios
@app.route('/horarios')
def horarios():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    horarios = obtener_horarios()
    return render_template("horarios.html", horarios=horarios)

# Pantalla agregar horario
@app.route('/agregar_horario', methods=['GET', 'POST'])
def agregar_horario():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        descripcion = request.form['descripcion']
        entrada_manana = request.form['entrada_manana']
        salida_manana = request.form['salida_manana']
        tolerancia_manana = request.form['tolerancia_manana']
        entrada_tarde = request.form['entrada_tarde']
        salida_tarde = request.form['salida_tarde']
        tolerancia_tarde = request.form['tolerancia_tarde']
        horarios_formulario(descripcion, entrada_manana, salida_manana, tolerancia_manana,  entrada_tarde, salida_tarde, tolerancia_tarde)
        flash('Horario agregado correctamente', 'success')
        return redirect(url_for('horarios'))

    return render_template('agregar_horarios.html')

# Pantalla para editar horarios
@app.route('/editar_horario/<int:id>', methods=['GET', 'POST'])
def editar_horario(id):
    if 'usuario' not in session:
        return redirect(url_for('login'))

    horarios = obtener_horario_Formulario(id)

    if request.method == 'POST':
        descripcion = request.form['descripcion']
        entrada_manana = request.form['entrada_manana']
        salida_manana = request.form['salida_manana']
        tolerancia_manana = request.form['tolerancia_manana']
        entrada_tarde = request.form['entrada_tarde']
        salida_tarde = request.form['salida_tarde']
        tolerancia_tarde = request.form['tolerancia_tarde']
        activo = 1 if 'activo' in request.form else 0
        actualizar_horarios(id, descripcion, entrada_manana, salida_manana, tolerancia_manana, entrada_tarde, salida_tarde, tolerancia_tarde, activo)
        flash('Horario actualizado correctamente', 'success')
        return redirect(url_for('horarios'))

    return render_template('editar_horarios.html', horarios=horarios)

# Pantalla de departamentos
@app.route('/departamentos')
def departamentos():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    departamentos = obtener_departamentos()
    return render_template("departamentos.html", departamentos=departamentos)

# Pantalla agregar departamento
@app.route('/agregar_departamento', methods=['GET', 'POST'])
def agregar_departamento():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    
    horarios = obtener_horarios_Departamentos()

    if request.method == 'POST':
        nombre = request.form['nombre']
        horario = int(request.form['id_horario'])
        departamento_formulario(nombre, horario)
        flash('Departamento agregado correctamente', 'success')
        return redirect(url_for('departamentos'))

    return render_template('agregar_departamentos.html', horarios=horarios)

# Pantalla para editar departamentos
@app.route('/editar_departamento/<int:id>', methods=['GET', 'POST'])
def editar_departamento(id):
    if 'usuario' not in session:
        return redirect(url_for('login'))

    departamentos = obtener_departamento_Formulario(id)
    horarios = obtener_horarios_Departamentos()

    if request.method == 'POST':
        nombre = request.form['nombre']
        horario = int(request.form['id_horario'])
        activo = 1 if 'activo' in request.form else 0
        actualizar_departamentos(id, nombre, horario, activo)
        flash('Departamento actualizado correctamente', 'success')
        return redirect(url_for('departamentos'))

    return render_template('editar_departamentos.html', departamentos=departamentos, horarios=horarios)


# Pantalla de usuarios
@app.route('/usuarios')
def usuarios():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    usuarios = obtener_usuarios()
    return render_template("usuarios.html", usuarios=usuarios)


# Pantalla agregar usuario
@app.route('/agregar_usuario', methods=['GET', 'POST'])
def agregar_usuario():
    
    if 'usuario' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        nombre = request.form['nombre']
        password = request.form['password']
        rol = request.form['rol'] == 'True'

        if not password:
            flash('La contraseña no puede estar vacía.', 'danger')
            return redirect(url_for('agregar_usuario'))

        password_hash = generate_password_hash(password)

        usuario_formulario(nombre, password_hash, rol)
        flash('Usuario agregado correctamente', 'success')
        return redirect(url_for('usuarios'))

    return render_template('agregar_usuarios.html')


# Pantalla para editar usuarios
@app.route('/editar_usuario/<int:id>', methods=['GET', 'POST'])
def editar_usuario(id):
    if 'usuario' not in session:
        return redirect(url_for('login'))

    usuarios = obtener_usuarios_Formulario(id)

    if request.method == 'POST':
        nombre = request.form['nombre']
        password = request.form['password']
        password_hash = generate_password_hash(password)
        rol = request.form['rol'] == 'True' 
        activo = 1 if 'activo' in request.form else 0
        actualizar_usuarios(id,nombre, password_hash, activo, rol)
        flash('Usuario actualizado correctamente', 'success')
        return redirect(url_for('usuarios'))

    return render_template('editar_usuarios.html', usuarios=usuarios)



# Pantalla logout
@app.route('/logout')
def logout():
    session.pop('usuario', None)
    flash('Sesión cerrada correctamente', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
