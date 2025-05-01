#Generar un usuario con un password con hash
from werkzeug.security import generate_password_hash
import pymysql

conexion = pymysql.connect(
    host='localhost',
    user='tu_usuario_mysql',
    password='tu_contraseña_mysql',
    db='nombre_de_tu_base',
    cursorclass=pymysql.cursors.DictCursor
)

cursor = conexion.cursor()
usuario = 'admin'
password = generate_password_hash('123456')  # hash seguro
cursor.execute("INSERT INTO usuarios (usuario, password) VALUES (%s, %s)", (usuario, password))
conexion.commit()
conexion.close()