import modulos.conexionDB as con
from io import BytesIO
from reportlab.pdfgen import canvas
from zk import ZK
from datetime import time

#Funcion para insertar usuarios
def UsuarioIn(users):
	cursor = con.conexion.cursor()
	for user in users:
		consulta = "INSERT INTO usuarios(id_user, Nombre) VALUES (%s, %s);"
		cursor.execute(consulta, (user.user_id, user.name))
		cursor.commit()
	cursor.close()
		
#Funcion para Insertar marcaciones a la BD
def Marcados(marcaciones, nombre_ZK, tipo, detalle):

    cursor = con.conexion.cursor()
    for marca in marcaciones:
        consulta = "INSERT INTO marcados(marcacion, tipo, FK_empleado, FK_dispositivos, detalle) VALUES (%s, %s, %s, %s, %s);"
        cursor.execute(consulta, (marca.timestamp, tipo, marca.user_id, nombre_ZK, detalle))
        cursor.connection.commit()
    cursor.close()
        
#Funcion para obtener usuarios de la BD
def obtener_usuarios():
    usuarios = []
    conexion = con.conexion
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id_user, Nombre FROM usuarios")
        usuarios = cursor.fetchall()
    conexion.close()
    return usuarios

#Funcion para obtener todos los dispositivos de la BD
def obtener_dispositivos():
    dispositivos = []
    conexion = con.conexion
    with conexion.cursor() as cursor:
        cursor.execute("SELECT * FROM dispositivos WHERE activo =  1")
        dispositivos = cursor.fetchall()
    conexion.close()
    return dispositivos

#Funcion para obtener todos los horarios de la BD
def obtener_horarios_TODOS():
    horarios = []
    conexion = con.conexion
    with conexion.cursor() as cursor:
        cursor.execute("SELECT * FROM horarios")
        horarios = cursor.fetchall()
    conexion.close()
    return horarios

def obtener_horarios(id):
    horarios = []
    conexion = con.conexion
    with conexion.cursor() as cursor:
        cursor.execute(f"SELECT * FROM horarios WHERE id_horario = {id}")
        horarios = cursor.fetchall()
    conexion.close()
    return horarios




#Funcion para obtener todos los departamentos de la BD
def obtener_departamentos_TODOS():
    departamentos = []
    conexion = con.conexion
    with conexion.cursor() as cursor:
        cursor.execute("SELECT * FROM departamentos")
        departamentos = cursor.fetchall()
    conexion.close()
    return departamentos


def obtener_departamentos(id):
    departamentos = []
    conexion = con.conexion
    with conexion.cursor() as cursor:
        cursor.execute(f"SELECT * FROM departamentos WHERE id_departamento = {id}")
        departamentos = cursor.fetchall()
    conexion.close()
    return departamentos

#Funcion para obtener todos los empleados de la BD
def obtener_empleados_TODOS():
    empleados = []
    conexion = con.conexion
    with conexion.cursor() as cursor:
        cursor.execute("SELECT * FROM empleados")
        empleados = cursor.fetchall()
    conexion.close()
    return empleados




def obtener_empleados(id):
    empleados = []
    conexion = con.conexion
    with conexion.cursor() as cursor:
        cursor.execute(f"SELECT * FROM empleados WHERE id_empleado_marcador = {id}")
        empleados = cursor.fetchall()
    conexion.close()
    return empleados







#Funcion para obtener un dispositivo por su ID
def obtener_dispositivo_ID(id):
    dispositivoID = []
    conexion = con.conexion
    with conexion.cursor() as cursor:
        cursor.execute(f"SELECT * FROM dispositivos WHERE id_dispositivo = {id}")
        dispositivoID = cursor.fetchall()
    conexion.close()
    return dispositivoID


#Funcion para obtener las marcaciones de la BD
def obtener_marcacion():
    cursor = con.conexion.cursor()
    marcacion = []
    with cursor.connection.cursor() as cursor:
        cursor.execute("SELECT id_marcado, id_marcacion, marcacion FROM marcados")
        marcacion = cursor.fetchall()
    con.conexion.close()
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

#Funcion para conectar al dispositivo ZK para capturar los datos
def Capturar_DatosZK():
    dispositivos = obtener_dispositivos()
    for dispositivo in dispositivos:
        zk = ZK(dispositivo['IP_dispositivo'], port=dispositivo['puerto'], timeout=5)

        conn = zk.connect()
        conn.disable_device()
        users = conn.get_users()
        marcaciones = conn.get_attendance()
        conn.enable_device()
        conn.disconnect()
        nombre_ZK = dispositivo['id_dispositivo']
        tipo, detalle = EntradaoSalida(marcaciones)
        UsuarioIn(users)
        Marcados(marcaciones, nombre_ZK, tipo, detalle)
    

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
def EntradaoSalida(marcaciones): 

    for marca in marcaciones:
        empleado = obtener_empleados(marca.user_id)
        departamento = obtener_departamentos(empleado['FK_departamento'])
        horarios = obtener_horarios(departamento['FK_horarios'])
        hora = marca.timestamp.time()
        if horarios['entrada_manana'] >= hora  or horarios['entrada_manana'] <= hora  and hora  <= horarios['tolerancia_manana']:
            tipo = 'entrada'
        else:
            tipo = 'entrada'    
            detalle = 'tarde'
        
        if horarios['salida_manana'] >= hora:
            horas_trabajadas = horarios['salida_manana'] - horarios['entrada_manana']
            tipo = 'salida'
        else:
            horas_trabajadas = horarios['salida_manana'] - horarios['entrada_manana']
            tipo = 'salida'
            detalle ='temprana'

        if horarios['entrada_tarde'] >= hora  or horarios['entrada_tarde'] <= hora and hora <= horarios['tolerancia_tarde']:
            tipo = 'entrada'
        else:
            tipo = 'entrada'
            detalle ='tarde'

        if horarios['salida_tarde'] >= hora:
            horas_trabajadas = horarios['salida_tarde'] - horarios['entrada_tarde']
            tipo = 'salida'
        else:
            horas_trabajadas = horarios['salida_tarde'] - horarios['entrada_salida']
            tipo = 'entrada'
            detalle ='temprana'
    return tipo, detalle, horas_trabajadas











               

def Capturar_Horario_Departamento(FK_horario):
    horario_departamento = []
    conexion = con.conexion
    with conexion.cursor() as cursor:
        cursor.execute(f"SELECT * FROM horarios WHERE id_horario = {FK_horario} ")
        horario_departamento = cursor.fetchall()
    conexion.close()
    return horario_departamento


def obtener_departamentos_FK():
    departamentos_FK = []
    conexion = con.conexion
    with conexion.cursor() as cursor:
        cursor.execute("SELECT FK_horarios FROM departamentos")
        departamentos_FK = cursor.fetchall()
    conexion.close()
    return departamentos_FK




def prueba():
    departamentos_FK = []
    conexion = con.conexion
    with conexion.cursor() as cursor:
        cursor.execute("SELECT * FROM departamentos D INNER JOIN horarios H ON D.")
        departamentos_FK = cursor.fetchall()
    conexion.close()
    return departamentos_FK