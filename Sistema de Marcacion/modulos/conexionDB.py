#Funcion para conectar con la BD
import pymysql
def obtener_conexion():
    return pymysql.connect(host='localhost', user='root', password='', db='sistemamc', cursorclass=pymysql.cursors.DictCursor)

conexion = obtener_conexion()
#cursorclass=pymysql.cursors.DictCursor