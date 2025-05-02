import pymysql
def obtener_conexion():
    return pymysql.connect(host='localhost', user='root', password='', db='sistemamc')

conexion = obtener_conexion()
