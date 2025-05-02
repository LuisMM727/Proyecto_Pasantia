from conexionDB import conexion


#Funcion para insertar usuarios
def UsuarioIn(users):
	cursor = conexion.cursor()
	for user in users:
		consulta = "INSERT INTO usuarios(id_user, Nombre) VALUES (%s, %s);"
		cursor.execute(consulta, (user.user_id, user.name))
		cursor.commit()
	cursor.close()
		

#Funcion para Insertar marcaciones
def Marcados(marcaciones):
	cursor = conexion.cursor()
	for marca in marcaciones:
		consulta = "INSERT INTO marcados(marcacion) VALUES (%s);"
		cursor.execute(consulta, (marca.timestamp))
		cursor.commit()
	cursor.close()