from modulos.conexionZK import zk
from modulos.funciones import Marcados, UsuarioIn

#try:
conn = zk.connect()
conn.disable_device()
users = conn.get_users()
marcaciones = conn.get_attendance()
Marcados(marcaciones)
UsuarioIn(users)

	



    
# except (conn) as e:
# 	print("Ocurrió un error al conectar: ", e)