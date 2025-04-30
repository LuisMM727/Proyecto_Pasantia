from flask import Flask 
import pymysql
from zk import ZK


zk = ZK('192.168.150.34', port=4370, timeout=5)
conexion = pymysql.connect(host='localhost',user='root',password='', db='marcador')





#Funcion para insertar usuarios
def UsuarioIn():
	for user in users:
		consulta = "INSERT INTO usuarios(id_user, Nombre) VALUES (%s, %s);"
		cursor.execute(consulta, (user.user_id, user.name))
		conexion.commit()
		

#Funcion para Insertar marcaciones
def Marcados(marcaciones):
	for marca in marcaciones:
		consulta = "INSERT INTO marcados(marcacion) VALUES (%s);"
		cursor.execute(consulta, (marca.timestamp))
		conexion.commit()

try:
	conn = zk.connect()
	conn.disable_device()
	users = conn.get_users()
	marcaciones = conn.get_attendance()
	cursor = conexion.cursor()

	Marcados(marcaciones)









    
	
	

        
	cursor.close()
	conexion.close()
except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
	print("Ocurrió un error al conectar: ", e)