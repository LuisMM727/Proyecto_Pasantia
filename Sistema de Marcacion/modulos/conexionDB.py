import pymysql
def obtener_conexion():
    return pymysql.connect(host='localhost', user='root', password='', db='marcador', cursorclass=pymysql.cursors.DictCursor)

conexion = obtener_conexion()
