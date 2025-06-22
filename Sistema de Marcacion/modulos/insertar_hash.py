#Generar un usuario con un password con hash
from werkzeug.security import generate_password_hash
import pymysql

conexion = pymysql.connect(host='localhost', user='root', password='', db='sistemamc', cursorclass=pymysql.cursors.DictCursor)

cursor = conexion.cursor()
usuario = 'usuario'
password = generate_password_hash('123456')
rol = False
activo = True 
cursor.execute("INSERT INTO usuarios (nombre_usuario, password_usuario, activo, rol) VALUES (%s, %s, %s, %s)", (usuario, password, activo, rol))
print("Se genero el usuario")
conexion.commit()
conexion.close()