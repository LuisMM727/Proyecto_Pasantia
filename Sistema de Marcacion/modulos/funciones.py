from flask import Flask, render_template, request, redirect, session, url_for, flash
import modulos.conexionDB as con
from io import BytesIO
from reportlab.pdfgen import canvas
from zk import ZK

#Funcion para insertar usuarios
def UsuarioIn(users):
	cursor = con.conexion.cursor()
	for user in users:
		consulta = "INSERT INTO usuarios(id_user, Nombre) VALUES (%s, %s);"
		cursor.execute(consulta, (user.user_id, user.name))
		cursor.commit()
	cursor.close()
		
#Funcion para Insertar marcaciones a la BD
def Marcados(marcaciones):
	cursor = con.conexion.cursor()
	for marca in marcaciones:
		consulta = "INSERT INTO marcados(id_marcacion, marcacion, tipo, FK_empleado, FK_dispositivos) VALUES (%s, %s, %s, %s, %s);"
		cursor.execute(consulta, (marca.user_id, marca.timestamp))
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
        print(zk,"hola")
        conn = zk.connect()
        conn.disable_device()
        users = conn.get_users()
        conn.enable_device()
        conn.disconnect()
        print(users)

#Funcion para conectar al dispositivo ZK para capturar los datos
def Capturar_DatosZK():
    dispositivos = obtener_dispositivos()
    for dispositivo in dispositivos:
        zk = ZK(dispositivo['IP_dispositivo'], port=dispositivo['puerto'], timeout=5)
        print(zk,"hola")
        conn = zk.connect()
        conn.disable_device()
        users = conn.get_users()
        conn.enable_device()
        conn.disconnect()
        print(users, "hola")
    

#Funcion que obtiene los datos del formulario de dipositivos para hacer la conexion y tomar los datos
def dispositivo_ZK(ip, puerto):
        zk = ZK(ip, port=int(puerto), timeout=5)
        print("hola")
        conn = zk.connect()
        conn.disable_device()
        users =  conn.get_users
        conn.enable_device()
        conn.disconnect()
        print(users)




#dispositivo_ZK('192.168.150.34', 4370)

#Capturar_DatosZK()