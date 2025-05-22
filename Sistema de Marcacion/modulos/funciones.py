
from conexionDB import obtener_conexion
from io import BytesIO
from reportlab.pdfgen import canvas
from zk import ZK
from datetime import  datetime, timedelta, time
from generate_zk_testdata import data


#Funcion para insertar usuarios
def UsuarioIn(users):
	cursor = obtener_conexion()
	for user in users:
		consulta = "INSERT INTO usuarios(id_user, Nombre) VALUES (%s, %s);"
		cursor.execute(consulta, (user.user_id, user.name))
		cursor.commit()
	cursor.close()
		
#Funcion para Insertar marcaciones a la BD
def Marcados(marca, nombre_ZK, tipo):
    conexion = obtener_conexion()
    cursor = conexion.cursor() 

    consulta = "INSERT INTO marcados(marcacion, tipo, FK_empleado, FK_dispositivos) VALUES (%s, %s, %s, %s);"
    cursor.execute(consulta, (marca.timestamp, tipo, marca.user_id, nombre_ZK))
    conexion.commit()

    cursor.close()
    conexion.close()
        
#Funcion para obtener usuarios de la BD
def obtener_usuario():
    usuarios = []
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id_user, Nombre FROM usuarios")
        usuarios = cursor.fetchall()
    conexion.close()
    return usuarios

#Funcion para obtener todos los dispositivos de la BD
def obtener_dispositivos():
    dispositivos = []
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT * FROM dispositivos WHERE activo =  1")
        dispositivos = cursor.fetchall()
    conexion.close()
    return dispositivos

def obtener_dispositivos_Prueba():
    conexion = obtener_conexion()
    #dispositivosPrueba = []
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


#Funcion para obtener un departamento de la BD a traves de la FK del empleado
def obtener_departamento(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT FK_horarios FROM departamentos WHERE id_departamento = %s", (id,))
        departamentos = cursor.fetchone()
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



#Funcion para obtener las marcaciones de la BD
def obtener_marcacion():
    cursor = obtener_conexion()
    marcacion = []
    with cursor.connection.cursor() as cursor:
        cursor.execute("SELECT id_marcado, id_marcacion, marcacion FROM marcados")
        marcacion = cursor.fetchall()
    obtener_conexion().conexion.close()
    return marcacion

#Funcion para convertir html a PDF
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


def Capturar_DatosZK(data):
    #  try:
    #      dispositivos = obtener_dispositivos()
    #      for dispositivo in dispositivos:
    #          zk = ZK(dispositivo['IP_dispositivo'], port=dispositivo['puerto'], timeout=5)

    #          conn = zk.connect()
    #          conn.disable_device()
    #          #users = conn.get_users()
    #          marcaciones = conn.get_attendance()
    #          conn.enable_device()
    #          conn.disconnect()
    #          nombre_ZK = dispositivo['id_dispositivo']
    #          Actualizar_Datos(nombre_ZK, marcaciones)

    #  except Exception as e:
        #print(f"Error: {e}")
        dipositivoPrueba = obtener_dispositivos_Prueba()
        marcaciones = data
        nombre_ZK = dipositivoPrueba['id_dispositivo']
        Actualizar_Datos(nombre_ZK,marcaciones)

#Funcion que obtiene los datos del formulario de dipositivos para hacer la conexion y tomar los datos
def dispositivo_ZK(ip, puerto):
        zk = ZK(ip, port=int(puerto), timeout=5)
        conn = zk.connect()
        conn.disable_device()
        users =  conn.get_users
        marcaciones = conn.get_attendance()
        conn.enable_device()
        conn.disconnect()
        UsuarioIn(users)
        Marcados(marcaciones)



#Funcion para saber si la marcacion es de tipo Entrada o Salida y cuantas horas trabajo 
def EntradaoSalida(marca):
    empleado = obtener_empleado(marca.user_id)
    departamento = obtener_departamento(empleado['FK_departamento'])
    horarios = obtener_horario(departamento['FK_horarios'])
    hora = marca.timestamp.time()

    def to_time(val):
        # Convierte val a datetime.time, soporta string, timedelta, o time
        if isinstance(val, time):
            return val
        elif isinstance(val, timedelta):
            # Convertir timedelta a time asumiendo que es tiempo desde 00:00
            total_seconds = val.total_seconds()
            horas = int(total_seconds // 3600)
            minutos = int((total_seconds % 3600) // 60)
            segundos = int(total_seconds % 60)
            return time(horas, minutos, segundos)
        elif isinstance(val, str):
            return datetime.strptime(val, "%H:%M:%S").time()
        else:
            raise ValueError(f"Tipo inesperado para convertir a time: {type(val)}")

    def to_timedelta(val):
        # Convierte string a timedelta o devuelve si ya es timedelta
        if isinstance(val, timedelta):
            return val
        elif isinstance(val, str):
            h, m, s = map(int, val.split(':'))
            return timedelta(hours=h, minutes=m, seconds=s)
        else:
            raise ValueError(f"Tipo inesperado para convertir a timedelta: {type(val)}")

    entrada_manana = to_time(horarios[0]['entrada_manana'])
    tolerancia_manana = to_timedelta(horarios[0]['tolerancia_manana'])
    salida_manana = to_time(horarios[0]['salida_manana'])

    entrada_tarde = to_time(horarios[0]['entrada_tarde'])
    tolerancia_tarde = to_timedelta(horarios[0]['tolerancia_tarde'])
    salida_tarde = to_time(horarios[0]['salida_tarde'])

    detalle = None
    tipo = None
    horas_trabajadas = None

    limite_entrada_manana = (datetime.combine(datetime.today(), entrada_manana) + tolerancia_manana).time()

    if entrada_manana <= hora <= limite_entrada_manana:
        tipo = 'entrada'
    elif hora > limite_entrada_manana:
        tipo = 'entrada'
        detalle = 'tarde'

    if hora <= salida_manana:
        horas_trabajadas = datetime.combine(datetime.today(), hora) - datetime.combine(datetime.today(), entrada_manana)
        tipo = 'salida'
    elif hora > salida_manana:
        horas_trabajadas = datetime.combine(datetime.today(), hora) - datetime.combine(datetime.today(), entrada_manana)
        tipo = 'salida'
        detalle = 'temprana'

    limite_entrada_tarde = (datetime.combine(datetime.today(), entrada_tarde) + tolerancia_tarde).time()

    if entrada_tarde <= hora <= limite_entrada_tarde:
        tipo = 'entrada'
    elif hora > limite_entrada_tarde:
        tipo = 'entrada'
        detalle = 'tarde'

    if hora <= salida_tarde:
        horas_trabajadas = datetime.combine(datetime.today(), hora) - datetime.combine(datetime.today(), entrada_tarde)
        tipo = 'salida'
    elif hora > salida_tarde:
        horas_trabajadas = datetime.combine(datetime.today(), hora) - datetime.combine(datetime.today(), entrada_tarde)
        tipo = 'salida'
        detalle = 'temprana'

    return tipo, detalle, horas_trabajadas



#Funcion que toma los datos de la marcacion en bruto, tantes de capturar mira si no son iguales y despues devuelve ese valor para que pase por la sgte funcion
def Actualizar_Datos(id_dispositivo, marcacion):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute(
                "SELECT marcacion FROM marcados WHERE FK_dispositivos = %s ORDER BY marcacion DESC LIMIT 1",
                (id_dispositivo,)
            )
            ultima_marcacion = cursor.fetchone()
        conexion.commit()
    finally:
        conexion.close()

    for marca in marcacion:
        if ultima_marcacion is None or marca.timestamp >= ultima_marcacion['marcacion']:
            tipo, _, _ = EntradaoSalida(marca)
            Marcados(marca, id_dispositivo, tipo)

Capturar_DatosZK(data)
#EntradaoSalida(Actualizar_Datos_Prueba)
#obtener_empleado(1001)