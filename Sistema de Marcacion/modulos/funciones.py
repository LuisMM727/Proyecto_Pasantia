
from modulos.conexionDB import obtener_conexion
from zk import ZK
from datetime import  datetime, timedelta, time
from modulos.generate_zk_testdata import data
from werkzeug.security import generate_password_hash


# Funcion para convertir una contraseña a hash
def PasswordHash(password):
    hash = generate_password_hash(password)
    return hash

#Funcion para obtener los id y nombre de los departamentos
def Departamentos():
    conexion = obtener_conexion()
    departamentos = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id_departamento, nombre_departamento FROM departamentos")
        departamentos = cursor.fetchall()
    conexion.close()
    return departamentos

#Funcion para insertar usuarios a la BD
def UsuarioIn(users):
	cursor = obtener_conexion()
	for user in users:
		consulta = "INSERT INTO usuarios(id_user, Nombre) VALUES (%s, %s);"
		cursor.execute(consulta, (user.user_id, user.name))
		cursor.commit()
	cursor.close()

#Funcion para obtener todas las ID de todos los empleados
def obtener_empleados_TODOS():
    conexion = obtener_conexion()
    empleados_TODOS = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id_empleado FROM empleado")
        empleados_TODOS= cursor.fetchall()
    conexion.close()
    return empleados_TODOS

#Funcion para obtener la ultima marcacion de un empleado cuya marcacion es entrada
def ultima_marcacion_empleado(id_empleado, id_dispositivo, fecha_marcacion):
    conexion = obtener_conexion()
    tipo_salida = 'entrada'
    with conexion.cursor() as cursor:
        cursor.execute("SELECT marcacion FROM marcados WHERE FK_empleado = %s AND FK_dispositivos = %s  AND tipo = %s AND DATE(marcacion) = %s ORDER BY marcacion DESC LIMIT 1", (id_empleado, id_dispositivo, tipo_salida, fecha_marcacion))
        ultima_marcacion_empleado = cursor.fetchone()
    conexion.close()

    if ultima_marcacion_empleado:
        return ultima_marcacion_empleado['marcacion']
    return None

#Funcion para obtener el ultimo empleado de la BD
def obtener_ultimo_empleado(id_empleado):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id_empleado FROM empleado WHERE id_empleado = %s",(id_empleado))
        ultimo_empleado = cursor.fetchone()
    conexion.close()
    return ultimo_empleado

#Funcion para Insertar empleados a la BD
def Empleados(empleado, departamento_unico):
    activo = True
    conexion = obtener_conexion()
    cursor = conexion.cursor() 

    consulta = "INSERT INTO empleado(id_empleado, nombre_empleado, activo, FK_departamento) VALUES (%s, %s, %s, %s);"
    cursor.execute(consulta, (empleado.user_id, empleado.name, activo, departamento_unico ))
    conexion.commit()

    cursor.close()
    conexion.close()

#Funcion para Insertar dispositivos a la BD
def dispositivo_formulario(descripcion, nombre, puerto, ip):
    activo = True
    conexion = obtener_conexion()
    cursor = conexion.cursor() 

    consulta = "INSERT INTO dispositivos(descripcion_dispositivo, nombre_dispositivo, activo, puerto, IP_dispositivo) VALUES (%s, %s, %s, %s, %s);"
    cursor.execute(consulta, (descripcion, nombre, activo, puerto, ip ))
    conexion.commit()

    cursor.close()
    conexion.close()

#Funcion para Insertar horarios a la BD
def horarios_formulario(descripcion, entrada_manana, salida_manana, tolerancia_manana, entrada_tarde, salida_tarde, tolerancia_tarde):
    activo = True
    conexion = obtener_conexion()
    cursor = conexion.cursor() 

    consulta = "INSERT INTO horarios(descripcion, entrada_manana, salida_manana, tolerancia_manana, entrada_tarde, salida_tarde, tolerancia_tarde, activo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
    cursor.execute(consulta, (descripcion, entrada_manana, salida_manana, tolerancia_manana, entrada_tarde, salida_tarde, tolerancia_tarde, activo ))
    conexion.commit()

    cursor.close()
    conexion.close() 

#Funcion para Insertar departamentos a la BD
def departamento_formulario(nombre, horario):
    activo = True
    conexion = obtener_conexion()
    cursor = conexion.cursor() 

    consulta = "INSERT INTO departamentos(nombre_departamento, activo, FK_horario) VALUES (%s, %s, %s);"
    cursor.execute(consulta, (nombre, activo, horario ))
    conexion.commit()

    cursor.close()
    conexion.close()

#Funcion para Insertar usuario a la BD
def usuario_formulario(nombre, password, rol):
    activo = True
    conexion = obtener_conexion()
    cursor = conexion.cursor() 

    consulta = "INSERT INTO usuarios(nombre_usuario, password_usuario, activo, rol) VALUES (%s, %s, %s, %s);"
    cursor.execute(consulta, (nombre, password, activo, rol ))
    conexion.commit()

    cursor.close()
    conexion.close()    

#Funcion para Insertar empleados a la BD
def empleados_formulario(id, nombre, departamento):
    activo = True
    conexion = obtener_conexion()
    cursor = conexion.cursor() 

    consulta = "INSERT INTO empleado(id_empleado, nombre_empleado, activo, FK_departamento) VALUES (%s, %s, %s, %s);"
    cursor.execute(consulta, (id, nombre, activo, departamento ))
    conexion.commit()

    cursor.close()
    conexion.close()   	

#Funcion para Insertar marcaciones a la BD
def Marcados(marca, nombre_ZK, tipo, detalle, horas_trabajadas):
    conexion = obtener_conexion()
    cursor = conexion.cursor() 

    consulta = "INSERT INTO marcados(marcacion, tipo, detalle, horas_trabajadas, FK_empleado, FK_dispositivos) VALUES (%s, %s, %s, %s, %s, %s);"
    cursor.execute(consulta, (marca.timestamp, tipo, detalle, horas_trabajadas, marca.user_id, nombre_ZK))
    conexion.commit()

    cursor.close()
    conexion.close()
        
#Funcion para obtener usuarios de la BD
def obtener_usuarios():
    usuarios = []
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT  * FROM usuarios")
        usuarios = cursor.fetchall()
    conexion.close()
    return usuarios

#Funcion para obtener horarios de la BD
def obtener_horarios_Departamentos():
    horarios = []
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT  id_horario, descripcion FROM horarios")
        horarios = cursor.fetchall()
    conexion.close()
    return horarios

#Funcion para obtener usuario Roles de la BD
def obtener_Usuario_rol(id):
    usuarios = []
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT  id_usuario, rol FROM usuarios")
        usuarios = cursor.fetchall()
    conexion.close()
    return usuarios


#Funcion para obtener todos los dispositivos de la BD los que estan activos
def obtener_dispositivos_activos():
    dispositivos = []
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT * FROM dispositivos WHERE activo =  1")
        dispositivos = cursor.fetchall()
    conexion.close()
    return dispositivos

#Funcion para obtener todos los dispositivos de la BD
def obtener_dispositivos():
    dispositivos = []
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT * FROM dispositivos")
        dispositivos = cursor.fetchall()
    conexion.close()
    return dispositivos

#Funcion para obtener la ID de un dispositivo en base a los paramentros de IP y Puerto
def obtener_dispositivos_ZK(ip, puerto):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute(f"SELECT id_dispositivo FROM dispositivos WHERE IP_dispositivo =  {ip} WHERE puerto = {puerto}")
        dispositivos_ZK = cursor.fetchone()
    conexion.close()
    return dispositivos_ZK

#Funcion para obtener especificamente un dispositivo que prueba para uso si no se dispone de un dispositivo real
def obtener_dispositivos_Prueba():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id_dispositivo FROM dispositivos WHERE id_dispositivo = 2")
        dispositivosPrueba = cursor.fetchone()
    conexion.close()
    return dispositivosPrueba

#Funcion para obtener un horario de la BD a traves de la FK  de departamento
def obtener_horario(id):
    horarios = []
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute(f"SELECT * FROM horarios WHERE id_horario = {id}")
        horarios = cursor.fetchall()
    conexion.close()
    return horarios

#Funcion para obtener todos los horarios de la BD
def obtener_horarios():
    horarios = []
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute(f"SELECT * FROM horarios")
        horarios = cursor.fetchall()
    conexion.close()
    return horarios


#Funcion para obtener un departamento de la BD a traves de la FK del empleado
def obtener_departamento(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT FK_horarios FROM departamentos WHERE id_departamento = %s", (id))
        departamentos = cursor.fetchone()
    conexion.close()
    return departamentos

#Funcion para obtener departamentos para mostrar en la tabla web del sistema
def obtener_departamentos():
    departamentos = []
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""SELECT 
	                        d.id_departamento, 
                            d.nombre_departamento, 
                            d.activo, 
                            h.descripcion
                        FROM departamentos AS d
                        JOIN horarios AS h ON d.FK_horarios = h.id_horario""")
        departamentos = cursor.fetchall()
    conexion.close()
    return departamentos

#Funcion para obtener  un empleado de la BD a traves de su id del marcador
def obtener_empleado(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute(f"SELECT FK_departamento FROM empleado WHERE id_empleado = {id}")
        empleados = cursor.fetchone()
    conexion.close()
    return empleados

#Funcion para obtener empleados para el formulario para editar empleados
def obtener_empleado_Formulario(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute(f"SELECT * FROM empleado WHERE id_empleado = {id}")
        empleados = cursor.fetchone()
    conexion.close()
    return empleados

#Funcion para obtener horarios para el formulario para editar horarios
def obtener_horario_Formulario(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute(f"SELECT * FROM horarios WHERE id_horario = {id}")
        horarios = cursor.fetchone()
    conexion.close()
    return horarios

#Funcion para obtener departamentos para el formulario para editar horarios
def obtener_departamento_Formulario(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute(f"SELECT * FROM departamentos WHERE id_departamento = {id}")
        departamentos = cursor.fetchone()
    conexion.close()
    return departamentos

#Funcion para obtener usuarios para el formulario para editar horarios
def obtener_usuarios_Formulario(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute(f"SELECT * FROM usuarios WHERE id_usuario = {id}")
        usuarios = cursor.fetchone()
    conexion.close()
    return usuarios

#Funcion para obtener dispositivos para el formulario para editar dispositivos
def obtener_dispositivo_Formulario(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute(f"SELECT * FROM dispositivos WHERE id_dispositivo = {id}")
        dispositivos = cursor.fetchone()
    conexion.close()
    return dispositivos

#Funcion para Actualizar empleados de la tabla a de la BD
def actualizar_empleado(id, nombre, activo, departamento):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""UPDATE empleado SET nombre_empleado = %s, activo = %s, FK_departamento = %s WHERE id_empleado = %s""", (nombre, activo, departamento, id))
    conexion.commit()
    conexion.close()

#Funcion para Actualizar dispositivos de la tabla a de la BD
def actualizar_dispositivo(descripcion, nombre, activo, puerto, ip):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""UPDATE dispositivos SET descripcion_dispositivo = %s, nombre_dispositivo = %s, activo = %s, puerto = %s""", (descripcion, nombre, activo, puerto, ip))
    conexion.commit()
    conexion.close()

#Funcion para Actualizar horarios de la tabla a de la BD
def actualizar_horarios(id, descripcion, entrada_manana, salida_manana, tolerancia_manana, entrada_tarde, salida_tarde, tolerancia_tarde, activo):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""UPDATE dispositivos SET descripcion = %s, entrada_manana = %s, salida_manana = %s, tolerancia_manana = %s, SET entrada_tarde = %s, SET salida_tarde = %s, SET tolerancia_tarde = %s,  SET activo = %s""", (descripcion, entrada_manana, salida_manana, tolerancia_manana, entrada_tarde, salida_tarde, tolerancia_tarde, activo))
    conexion.commit()
    conexion.close()


#Funcion para Actualizar departamentos de la tabla a de la BD
def actualizar_departamentos(nombre, activo, horario):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""UPDATE departamentos SET nombre = %s, activo = %s, FK_horario = %s""", (nombre, activo, horario))
    conexion.commit()
    conexion.close()


#Funcion para Actualizar usuarios de la tabla a de la BD
def actualizar_usuarios(nombre, password, activo, rol):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""UPDATE usuarios SET nombre_usuario = %s, password = %s, activo = %s , rol = %s""", (nombre, password, activo, rol))
    conexion.commit()
    conexion.close()

#Funcion para obtener las empleados de la BD
def obtener_empleados():
    empleados = []
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute(("""SELECT 
	                        e.id_empleado, 
                            e.nombre_empleado, 
                            e.activo, 
                            d.nombre_departamento
                        FROM empleado AS e
                        JOIN departamentos AS d ON e.FK_departamento = d.id_departamento"""))
        empleados = cursor.fetchall()
    conexion.close()
    return empleados

#Funcion para obtener las marcaciones de la BD
def obtener_marcacion():
    cursor = obtener_conexion()
    marcacion = []
    with cursor.cursor() as cursor:
        cursor.execute("""SELECT 
	                        m.id_marcacion, 
                            m.marcacion, 
                            m.tipo,
                            m.detalle,
                            m.horas_trabajadas,
                            e.nombre_empleado, 
                            d.nombre_dispositivo 
                        FROM marcados AS m 
                        JOIN empleado AS e ON m.FK_empleado = e.id_empleado 
                        JOIN dispositivos AS d ON  m.FK_dispositivos = d.id_dispositivo""")
        marcacion = cursor.fetchall()
    obtener_conexion().close()
    return marcacion

#Funcion para captuar los datos de todos los dispositivos uno a uno
def Capturar_DatosZK():
        try:
            dispositivos = obtener_dispositivos()
            for dispositivo in dispositivos:
                zk = ZK(dispositivo['IP_dispositivo'], port=dispositivo['puerto'], timeout=5)

                conn = zk.connect()
                conn.disable_device()
                empleados = conn.get_users()
                marcaciones = conn.get_attendance()
                conn.enable_device()
                conn.disconnect()
                Actualizar_Datos_Empleados(empleados)
                nombre_ZK = dispositivo['id_dispositivo']
                Actualizar_Datos(nombre_ZK, marcaciones)

        except Exception as e:
            print(f"Error: {e}")
            dipositivoPrueba = obtener_dispositivos_Prueba()
            generador_marcaciones = data
            nombre_ZK = dipositivoPrueba['id_dispositivo']
            Actualizar_Datos(nombre_ZK,generador_marcaciones)

#Funcion que obtiene los datos del formulario de dipositivos para hacer la conexion y tomar los datos
def dispositivo_ZK(ip, puerto):
        zk = ZK(ip, port=int(puerto), timeout=5)
        conn = zk.connect()
        conn.disable_device()
        empleados =  conn.get_users
        marcaciones = conn.get_attendance()
        conn.enable_device()
        conn.disconnect()
        Actualizar_Datos_Empleados(empleados)
        nombre_ZK = obtener_dispositivos_ZK(ip, puerto)
        Actualizar_Datos(nombre_ZK, marcaciones)

#Funcion para convertir un valor a time
def asegurar_time(valor):
    if isinstance(valor, timedelta):
        return (datetime.min + valor).time()
    return valor

#Funcion para saber si la marcacion es de tipo Entrada o Salida y cuantas horas trabajo y que en condiciones llego al trabajo
def EntradaoSalida(marcacion, id_dispositivo):
    empleado = obtener_empleado(marcacion.user_id)

    departamento = obtener_departamento(empleado['FK_departamento'])

    horarios_lista = obtener_horario(departamento['FK_horarios'])
    horarios = horarios_lista[0]
    fecha_marcacion = marcacion.timestamp.date()
    hora_marcacion = marcacion.timestamp
    ultima_marcacion = ultima_marcacion_empleado(marcacion.user_id, id_dispositivo, fecha_marcacion)

    entrada_manana = datetime.combine(fecha_marcacion, asegurar_time(horarios['entrada_manana']))
    tolerancia_manana = datetime.combine(fecha_marcacion, asegurar_time(horarios['tolerancia_manana']))
    salida_manana = datetime.combine(fecha_marcacion, asegurar_time(horarios['salida_manana']))

    entrada_tarde = datetime.combine(fecha_marcacion, asegurar_time(horarios['entrada_tarde']))
    tolerancia_tarde = datetime.combine(fecha_marcacion, asegurar_time(horarios['tolerancia_tarde']))
    salida_tarde = datetime.combine(fecha_marcacion, asegurar_time(horarios['salida_tarde']))

    tipo = ''
    detalle = ''
    horas_trabajadas = timedelta(0)
    horas_trabajadas_decimales = None

    # Salida mañana (verificar antes de entrada tarde para evitar conflictos)
    if salida_manana - timedelta(minutes=10) <= hora_marcacion < entrada_tarde:
        tipo = 'salida'
        detalle = None
        if ultima_marcacion: 
            horas_trabajadas = hora_marcacion - ultima_marcacion
            horas_trabajadas_decimales = timedelta(hours=(horas_trabajadas.total_seconds() / 3600))
        else:
            horas_trabajadas = hora_marcacion - entrada_manana
            horas_trabajadas_decimales = timedelta(hours=(horas_trabajadas.total_seconds() / 3600))

    # Entrada mañana
    elif entrada_manana <= hora_marcacion <= tolerancia_manana:
        tipo = 'entrada'
        detalle = 'a tiempo'
    elif tolerancia_manana < hora_marcacion < salida_manana:
        tipo = 'entrada'
        detalle = 'tarde'

    # Salida tarde ( verifica antes que cualquier otra entrada por la tarde)
    elif salida_tarde - timedelta(minutes=10) <= hora_marcacion:
        tipo = 'salida'
        detalle = None
        if ultima_marcacion: 
            horas_trabajadas = hora_marcacion - ultima_marcacion
            horas_trabajadas_decimales = timedelta(hours=(horas_trabajadas.total_seconds() / 3600))
        else:
            horas_trabajadas = hora_marcacion - entrada_tarde
            horas_trabajadas_decimales = timedelta(hours=(horas_trabajadas.total_seconds() / 3600))

    # Entrada tarde
    elif entrada_tarde <= hora_marcacion <= tolerancia_tarde:
        tipo = 'entrada'
        detalle = 'a tiempo'
    elif tolerancia_tarde < hora_marcacion < salida_tarde:
        tipo = 'entrada'
        detalle = 'tarde'

    return tipo, detalle, horas_trabajadas_decimales

#Funcion para filtrar marcaciones, cuyas marcaciones filtran si estan realacionadas con los empleados de la BD
def Filtrados(marcaciones):
        empleados_id = obtener_empleados_TODOS()
        ids_validos = {e['id_empleado']for e in empleados_id}
    
        marcas_filtradas = [m for m in marcaciones if int(m.user_id) in ids_validos]
        return marcas_filtradas

#Funcion que toma los datos de la marcacion en bruto, antes de capturar mira si no son iguales y despues devuelve ese valor para que pase por la sgte funcion
def Actualizar_Datos(id_dispositivo, marcacion):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute(
                "SELECT marcacion FROM marcados WHERE FK_dispositivos = %s ORDER BY marcacion DESC LIMIT 1",(id_dispositivo,))
            ultima_marcacion = cursor.fetchone()
        conexion.commit()
    finally:
        conexion.close()

    for marca in marcacion:
        if ultima_marcacion is None or marca.timestamp >= ultima_marcacion['marcacion']:   
            tipo, detalle, horas_trabajadas = EntradaoSalida(marca, id_dispositivo)
            Marcados(marca, id_dispositivo, tipo, detalle, horas_trabajadas)  

#Funcion que toma los datos de los empleados en bruto, antes de enviarlo a la BD mira si no es un empleado que ya existe en la tabla en la BD
def Actualizar_Datos_Empleados(empleados):

    for empleado in empleados:
        ultimo_empleado = obtener_ultimo_empleado(empleado.user_id)
        if ultimo_empleado is None:
            Empleados(empleado,1)
