from modulos.conexionZK import zk
import modulos.funciones as a

try:
	conn = zk.connect()
	conn.disable_device()
	users = conn.get_users()
	marcaciones = conn.get_attendance()
	a.Marcados(marcaciones)

	



    
except (conn) as e:
	print("Ocurrió un error al conectar: ", e)