from datetime import time
import pymysql
def obtener_conexion():
    return pymysql.connect(host='localhost', user='root', password='', db='marcador', cursorclass=pymysql.cursors.DictCursor)

conexion = obtener_conexion()

def obtener_marcacion():
    cursor = conexion.cursor()
    marcacion = []
    with cursor.connection.cursor() as cursor:
        cursor.execute("SELECT *  FROM marcados")
        marcacion = cursor.fetchall()
    conexion.close()
    return marcacion

marcacion = obtener_marcacion()

for marca in marcacion:
    print(marca)






















# def EntradaoSalida(marcaciones): 

#     for marca in marcaciones:
#         empleado = obtener_empleados(marca.user_id)
#         departamento = obtener_departamentos(empleado['FK_departamento'])
#         horarios = obtener_horarios(departamento['FK_horarios'])
#         hora = marca.timestamp.time()
#         if horarios['entrada_manana'] >= hora  or horarios['entrada_manana'] <= hora  and hora  <= horarios['tolerancia_manana']:
#             tipo = 'entrada'
#         else:
#             tipo = 'entrada'    
#             detalle = 'tarde'
        
#         if horarios['salida_manana'] >= hora:
#             horas_trabajadas = horarios['salida_manana'] - horarios['entrada_manana']
#             tipo = 'salida'
#         else:
#             horas_trabajadas = horarios['salida_manana'] - horarios['entrada_manana']
#             tipo = 'salida'
#             detalle ='temprana'

#         if horarios['entrada_tarde'] >= hora  or horarios['entrada_tarde'] <= hora and hora <= horarios['tolerancia_tarde']:
#             tipo = 'entrada'
#         else:
#             tipo = 'entrada'
#             detalle ='tarde'

#         if horarios['salida_tarde'] >= hora:
#             horas_trabajadas = horarios['salida_tarde'] - horarios['entrada_tarde']
#             tipo = 'salida'
#         else:
#             horas_trabajadas = horarios['salida_tarde'] - horarios['entrada_salida']
#             tipo = 'entrada'
#             detalle ='temprana'
#     return tipo, detalle, horas_trabajadas