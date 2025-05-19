import pyodbc  # Asegúrate de tener la librería para tu conexión a la base de datos

def prueba():
    datos_combinados = []
    conexion_str = "DRIVER={Tu Driver};SERVER=TuServidor;DATABASE=SistemaMC;UID=TuUsuario;PWD=TuContraseña"  # Reemplaza con tus datos de conexión
    conexion = None
    try:
        conexion = pyodbc.connect(conexion_str)
        with conexion.cursor() as cursor:
            cursor.execute("""
                SELECT
                    e.id_empleado,
                    e.id_empleado_marcador,
                    e.nombre_empleado,
                    e.FK_departamento,
                    d.id_departamento,
                    d.nombre_departamento,
                    h.id_horario,
                    h.descripcion AS descripcion_horario,
                    h.entrada_manana,
                    h.salida_manana,
                    h.tolerancia_manana,
                    h.entrada_tarde,
                    h.salida_tarde,
                    h.tolerancia_tarde
                FROM empleado e
                INNER JOIN departamentos d ON e.FK_departamento = d.id_departamento
                INNER JOIN horarios h ON d.FK_horarios = h.id_horario;
            """)
            datos_combinados = cursor.fetchall()

            # Convertir las filas a diccionarios para facilitar el acceso por nombre de columna
            column_names = [column[0] for column in cursor.description]
            empleados_departamentos_horarios = [dict(zip(column_names, row)) for row in datos_combinados]

    except pyodbc.Error as ex:
        sqlstate = ex.args[0]
        print(f"Error al conectar o ejecutar la consulta: {sqlstate}")
    finally:
        if conexion:
            conexion.close()
    return empleados_departamentos_horarios

# Ejemplo de cómo usar las funciones
if __name__ == "__main__":
    datos_empleados = prueba()
    # Suponiendo que tienes una marcación específica y el ID del empleado asociado
    from datetime import datetime, timedelta, time
    marcacion_ejemplo = datetime(2025, 5, 19, 7, 30, 0) # Ejemplo de una marcación timestamp
    empleado_id_ejemplo = 1 # Suponiendo que esta marcación pertenece al empleado con ID 1

    def EntradaoSalida(marcacion_timestamp, empleado_id, datos_empleados):
        marcacion_hora = marcacion_timestamp.time()
        tipo = None
        entrada_tardia = None

        # Buscar la información del empleado, departamento y horario correspondiente
        empleado_info = next((item for item in datos_empleados if item['id_empleado'] == empleado_id), None)

        if empleado_info:
            hora_entrada_manana = empleado_info.get('entrada_manana')
            tolerancia_manana = empleado_info.get('tolerancia_manana')
            hora_entrada_tarde = empleado_info.get('entrada_tarde')
            tolerancia_tarde = empleado_info.get('tolerancia_tarde')

            if hora_entrada_manana and tolerancia_manana:
                hora_entrada_manana_time = hora_entrada_manana if isinstance(hora_entrada_manana, time) else hora_entrada_manana.to_pytime()
                tolerancia_manana_time = tolerancia_manana if isinstance(tolerancia_manana, time) else tolerancia_manana.to_pytime()

                if hora_entrada_manana_time <= marcacion_hora <= tolerancia_manana_time:
                    tipo = 'entrada_manana'
                elif marcacion_hora > tolerancia_manana_time:
                    tipo = 'entrada_manana'
                    entrada_tardia = 'tarde_manana'

            if hora_entrada_tarde and tolerancia_tarde:
                hora_entrada_tarde_time = hora_entrada_tarde if isinstance(hora_entrada_tarde, time) else hora_entrada_tarde.to_pytime()
                tolerancia_tarde_time = tolerancia_tarde if isinstance(tolerancia_tarde, time) else tolerancia_tarde.to_pytime()

                if hora_entrada_tarde_time <= marcacion_hora <= tolerancia_tarde_time:
                    tipo = 'entrada_tarde'
                elif marcacion_hora > tolerancia_tarde_time:
                    tipo = 'entrada_tarde'
                    entrada_tardia = 'tarde_tarde'

        return {'tipo': tipo, 'tardanza': entrada_tardia}

    resultado = EntradaoSalida(marcacion_ejemplo, empleado_id_ejemplo, datos_empleados)
    print(f"Para la marcación a las {marcacion_ejemplo.strftime('%H:%M:%S')} del empleado {empleado_id_ejemplo}:")
    print(f"Tipo: {resultado['tipo']}, Tarde: {resultado['tardanza']}")




import pyodbc
from datetime import datetime, time

# ... (Tu función para establecer la conexión a la base de datos 'con' debería estar definida)

def obtener_id_dispositivo(cursor, nombre_ZK):
    cursor.execute("SELECT id_dispositivo FROM dispositivos WHERE nombre_dispositivo = ?;", (nombre_ZK,))
    resultado = cursor.fetchone()
    if resultado:
        return resultado[0]
    else:
        print(f"Advertencia: No se encontró el dispositivo con nombre '{nombre_ZK}'.")
        return None

def Marcados(marcaciones, nombre_ZK, tipo_marcacion):
    conexion = con.conexion
    cursor = conexion.cursor()
    try:
        id_dispositivo = obtener_id_dispositivo(cursor, nombre_ZK)
        if id_dispositivo is not None:
            for marca in marcaciones:
                consulta = "INSERT INTO marcados(marcacion, tipo, FK_empleado, FK_dispositivos) VALUES (?, ?, ?, ?);"
                cursor.execute(consulta, (datetime.fromtimestamp(marca.timestamp), tipo_marcacion, marca.user_id, id_dispositivo))
            conexion.commit()
        else:
            print(f"No se insertaron marcaciones debido a un dispositivo no válido: {nombre_ZK}")
            conexion.rollback()
    except pyodbc.Error as ex:
        sqlstate = ex.args[0]
        print(f"Error al insertar marcaciones: {sqlstate}")
        conexion.rollback()
    finally:
        cursor.close()

def determinar_tipo_marcacion(marcacion_timestamp, empleado_id, datos_empleados):
    marcacion_hora = marcacion_timestamp.time()
    tipo = None
    entrada_tardia = None

    empleado_info = next((item for item in datos_empleados if item['id_empleado'] == empleado_id), None)

    if empleado_info:
        hora_entrada_manana = empleado_info.get('entrada_manana')
        tolerancia_manana = empleado_info.get('tolerancia_manana')
        hora_entrada_tarde = empleado_info.get('entrada_tarde')
        tolerancia_tarde = empleado_info.get('tolerancia_tarde')

        if hora_entrada_manana and tolerancia_manana:
            hora_entrada_manana_time = hora_entrada_manana if isinstance(hora_entrada_manana, time) else hora_entrada_manana.to_pytime()
            tolerancia_manana_time = tolerancia_manana if isinstance(tolerancia_manana, time) else tolerancia_manana.to_pytime()

            if hora_entrada_manana_time <= marcacion_hora <= tolerancia_manana_time:
                tipo = 'entrada_manana'
            elif marcacion_hora > tolerancia_manana_time:
                tipo = 'entrada_manana_tarde'

        if hora_entrada_tarde and tolerancia_tarde:
            hora_entrada_tarde_time = hora_entrada_tarde if isinstance(hora_entrada_tarde, time) else hora_entrada_tarde.to_pytime()
            tolerancia_tarde_time = tolerancia_tarde if isinstance(tolerancia_tarde, time) else tolerancia_tarde.to_pytime()

            if hora_entrada_tarde_time <= marcacion_hora <= tolerancia_tarde_time:
                tipo = 'entrada_tarde'
            elif marcacion_hora > tolerancia_tarde_time:
                tipo = 'entrada_tarde_tarde'
        elif tipo is None:
            tipo = 'salida' # Lógica de salida (debes refinarla)

    return tipo

# Ejemplo de uso:
if __name__ == "__main__":
    class MockMarcacion:
        def __init__(self, timestamp, user_id):
            self.timestamp = timestamp
            self.user_id = user_id

    marcaciones_ejemplo = [
        MockMarcacion(datetime(2025, 5, 19, 7, 0, 0).timestamp(), 1),
        MockMarcacion(datetime(2025, 5, 19, 9, 15, 0).timestamp(), 2),
        MockMarcacion(datetime(2025, 5, 19, 14, 35, 0).timestamp(), 1),
    ]
    nombre_dispositivo_ejemplo = "ZK_1"

    # Suponemos que ya tienes los datos de empleados cargados
    # (podrías llamar a 'prueba()' o 'obtener_datos_empleados()' aquí)
    # Para este ejemplo, simulamos los datos:
    datos_empleados_simulado = [
        {'id_empleado': 1, 'entrada_manana': time(6, 0, 0), 'tolerancia_manana': time(6, 10, 0), 'entrada_tarde': time(14, 0, 0), 'tolerancia_tarde': time(14, 5, 0)},
        {'id_empleado': 2, 'entrada_manana': time(8, 0, 0), 'tolerancia_manana': time(8, 5, 0), 'entrada_tarde': time(13, 0, 0), 'tolerancia_tarde': time(13, 10, 0)},
    ]

    tipos_marcaciones = []
    for marca in marcaciones_ejemplo:
        tipo = determinar_tipo_marcacion(datetime.fromtimestamp(marca.timestamp), marca.user_id, datos_empleados_simulado)
        tipos_marcaciones.append(tipo)

    Marcados(marcaciones_ejemplo, nombre_dispositivo_ejemplo, tipos_marcaciones)
    print("Marcaciones insertadas con tipos determinados.")