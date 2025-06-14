#Generar un usuario con un password con hash
from werkzeug.security import generate_password_hash
import pymysql

conexion = pymysql.connect(host='localhost', user='root', password='', db='sistemamc', cursorclass=pymysql.cursors.DictCursor)

cursor = conexion.cursor()
usuario = 'admin'
password = generate_password_hash('123456')
activo = True 
cursor.execute("INSERT INTO usuarios (nombre_usuario, password_usuario, activo) VALUES (%s, %s, %s)", (usuario, password, activo))
print("Se genero el usuario")
conexion.commit()
conexion.close()

def PasswordHash(password):
    hash = generate_password_hash(password)
    return hash