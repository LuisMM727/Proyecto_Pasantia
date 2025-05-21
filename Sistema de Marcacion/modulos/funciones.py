import conexionDB as con
from io import BytesIO
from reportlab.pdfgen import canvas
from zk import ZK
from datetime import  datetime, time

from generate_zk_testdata import data


#Funcion para insertar usuarios
def UsuarioIn(users):
	cursor = con.conexion.cursor()
	for user in users:
		consulta = "INSERT INTO usuarios(id_user, Nombre) VALUES (%s, %s);"
		cursor.execute(consulta, (user.user_id, user.name))
		cursor.commit()
	cursor.close()
		
#Funcion para Insertar marcaciones a la BD
def Marcados(marcaciones, nombre_ZK, tipo):

    cursor = con.conexion.cursor()
    for marca in marcaciones:
        consulta = "INSERT INTO marcados(marcacion, tipo, FK_empleado, FK_dispositivos) VALUES (%s, %s, %s, %s);"
        cursor.execute(consulta, (marca.timestamp, tipo, marca.user_id, nombre_ZK))
        cursor.connection.commit()
    cursor.close()
        
#Funcion para obtener usuarios de la BD
def obtener_usuario():
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

def obtener_dispositivos_Prueba():
    conexion = con.conexion
    dispositivosPrueba = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id_dispositivo FROM dispositivos WHERE id_dispositivo = 2")
        dispositivosPrueba = cursor.fetchall()
    conexion.close()
    return dispositivosPrueba

#Funcion para obtener un horario de la BD a traves de la FK  de departamento
def obtener_horario(id):
    horarios = []
    conexion = con.conexion
    with conexion.cursor() as cursor:
        cursor.execute(f"SELECT * FROM horarios WHERE id_horario = {id}")
        horarios = cursor.fetchall()
    conexion.close()
    return horarios


#Funcion para obtener un departamento de la BD a traves de la FK del empleado
def obtener_departamento(id):
    departamentos = []
    conexion = con.conexion
    with conexion.cursor() as cursor:
        cursor.execute(f"SELECT * FROM departamentos WHERE id_departamento = {id}")
        departamentos = cursor.fetchall()
    conexion.close()
    return departamentos

#Funcion para obtener  un empleado de la BD a traves de su id del marcador
def obtener_empleado(id):
    empleados = []
    conexion = con.conexion
    with conexion.cursor() as cursor:
        cursor.execute(f"SELECT * FROM empleados WHERE id_empleado_marcador = {id}")
        empleados = cursor.fetchall()
    conexion.close()
    return empleados



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


def Capturar_DatosZK(data):
    # try:
    #     dispositivos = obtener_dispositivos()
    #     for dispositivo in dispositivos:
    #         zk = ZK(dispositivo['IP_dispositivo'], port=dispositivo['puerto'], timeout=5)

    #         conn = zk.connect()
    #         conn.disable_device()
    #         #users = conn.get_users()
    #         marcaciones = conn.get_attendance()
    #         conn.enable_device()
    #         conn.disconnect()
    #         #nombre_ZK = dispositivo['id_dispositivo']
    #         #Actualizar_Datos(nombre_ZK, marcaciones)
    #         for marca in marcaciones:
    #              print(marca)
    # except Exception as e:
        #print(f"Error: {e}")
        dipositivoPrueba = obtener_dispositivos_Prueba()
        marcaciones = data
        nombre_ZK = dipositivoPrueba[0]
        Actualizar_Datos(nombre_ZK, marcaciones)



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
        empleado = obtener_empleado(marca.user_id)
        departamento = obtener_departamento(empleado['FK_departamento'])
        horarios = obtener_horario(departamento['FK_horarios'])
        hora = marca.timestamp.time()
        detalle = []
        tipo = []
        horas_trabajadas = []
        if horarios['entrada_manana'] >= hora  or horarios['entrada_manana'] <= hora  and hora  <= horarios['tolerancia_manana']:
            tipo = 'entrada'
        else:
            tipo = 'entrada'    
            detalle = 'tarde'
        
        if horarios['salida_manana'] >= hora:
            horas_trabajadas = hora - horarios['entrada_manana']
            tipo = 'salida'
        else:
            horas_trabajadas = hora - horarios['entrada_manana']
            tipo = 'salida'
            detalle ='temprana'

        if horarios['entrada_tarde'] >= hora  or horarios['entrada_tarde'] <= hora and hora <= horarios['tolerancia_tarde']:
            tipo = 'entrada'
        else:
            tipo = 'entrada'
            detalle ='tarde'

        if horarios['salida_tarde'] >= hora:
            horas_trabajadas = hora - horarios['entrada_tarde']
            tipo = 'salida'
        else:
            horas_trabajadas = hora - horarios['entrada_salida']
            tipo = 'entrada'
            detalle ='temprana'
    return tipo, detalle, horas_trabajadas




#Funcion para uso de pruebas
def prueba(data): 

    for marca in data:
        hora = marca.timestamp.time()
        tipo = []

        horario = datetime.strptime("06:45:00","%H:%M:%S").time()
        if horario >= hora  or horario <= hora  and hora  <= horario:
            tipo = 'entrada'
        else:
            tipo = 'salida'
    return tipo

#Funcion que toma los datos de la marcacion en bruto, tantes de capturar mira si no son iguales y despues devuelve ese valor para que pase por la sgte funcion
def Actualizar_Datos(id_dispositivo, marcacion):
    conexion = con.conexion
    with conexion.cursor() as cursor:
        #cursor.execute(f"SELECT marcacion FROM marcados WHERE FK_dispositivos = 1 ORDER BY  marcacion DESC LIMIT 1")
        #cursor.execute(f"SELECT 1 FROM DUMNY ")
        ultima_marcacion = cursor.fetchone()['marcacion']
    conexion.close()

    # for marca in marcacion:

    #     if marca.timestamp >= ultima_marcacion or ultima_marcacion is None:
    #         tipo, _, _ = EntradaoSalida(marca)
    #         Marcados(marca, id_dispositivo, tipo)
    print(ultima_marcacion)


Capturar_DatosZK(data)