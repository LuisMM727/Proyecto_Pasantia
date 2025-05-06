import modulos.conexionDB as conn
from io import BytesIO
from reportlab.pdfgen import canvas

#Funcion para insertar usuarios
def UsuarioIn(users):
	cursor = conexion.cursor()
	for user in users:
		consulta = "INSERT INTO usuarios(id_user, Nombre) VALUES (%s, %s);"
		cursor.execute(consulta, (user.user_id, user.name))
		cursor.commit()
	cursor.close()
		
#Funcion para Insertar marcaciones a la BD
def Marcados(marcaciones):
	cursor = conn.conexion.cursor()
	for marca in marcaciones:
		consulta = "INSERT INTO marcados(id_marcacion, marcacion) VALUES (%s, %s);"
		cursor.execute(consulta, (marca.user_id, marca.timestamp))
		cursor.connection.commit()
	cursor.close()
      
#Funcion para obtener usuarios de la BD
def obtener_usuarios():
    usuarios = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id_user, Nombre FROM usuarios")
        usuarios = cursor.fetchall()
    conexion.close()
    return usuarios

#Funcion para obtener las marcaciones de la BD
def obtener_marcacion():
    cursor = conn.conexion.cursor()
    marcacion = []
    with cursor.connection.cursor() as cursor:
        cursor.execute("SELECT id_marcacion, marcacion FROM marcados")
        marcacion = cursor.fetchall()
    conn.conexion.close()
    return marcacion

#Funcion para convertir html a PDF
def generate_pdf_file(usuarios):

    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    p.drawString(100, 750, "reporte")
    y = 700

    for book in usuarios:
        p.drawString(100, y, f"usuarios: {book}")

        y -= 60
 
    p.showPage()
    p.save()
 
    buffer.seek(0)
    return buffer