# from zk import ZK
# from modulos.funciones import obtener_dispositivos

# def Capturar_DatosZK():
#     dispositivos = obtener_dispositivos()
#     for dispositivo in dispositivos:
#         zk = ZK(dispositivo['IP_dispositivo'], port=dispositivo['puerto'], timeout=5)
#         nombre_ZK = dispositivo['nombre_dispositivo']
#         conn = zk.connect()
#         conn.disable_device()
#         users = conn.get_users()
#         marcaciones = conn.get_attendance()
#         conn.enable_device()
#         conn.disconnect()
#         UsuarioIn(users)
#         Marcados(marcaciones,nombre_ZK)



from datetime import timedelta

def inferir_tipo_marcacion(fecha_hora_marcacion, horarios):
    hora_marcacion = fecha_hora_marcacion.time()
    tipo_inferido = None

    for horario in horarios:
        # Comparar con hora de entrada de la mañana
        if horario.get('hora_entrada_manana'):
            delta_entrada_manana = abs(hora_marcacion - horario['hora_entrada_manana'])
            if delta_entrada_manana < timedelta(minutes=30):  # Ajusta la ventana de tiempo según necesites
                return "ENTRADA"

        # Comparar con hora de entrada de la tarde
        if horario.get('hora_entrada_tarde'):
            delta_entrada_tarde = abs(hora_marcacion - horario['hora_entrada_tarde'])
            if delta_entrada_tarde < timedelta(minutes=30):  # Ajusta la ventana de tiempo según necesites
                return "ENTRADA"

    return "DESCONOCIDO"

def Marcados(marcaciones, nombre_ZK):
    empleados_dict = {emp['id_empleado']: emp for emp in obtener_empleados()}
    cursor = con.conexion.cursor()

    for marca in marcaciones:
        id_empleado = marca.user_id
        timestamp_marcacion = marca.timestamp
        tipo_marcacion = "DESCONOCIDO"

        if id_empleado in empleados_dict:
            empleado = empleados_dict[id_empleado]
            id_departamento = empleado.get('FK_departamento')

            if id_departamento:
                horarios_del_departamento = obtener_horarios_por_departamento(id_departamento)
                if horarios_del_departamento:
                    tipo_inferido = inferir_tipo_marcacion(timestamp_marcacion, horarios_del_departamento)
                    if tipo_inferido:
                        tipo_marcacion = tipo_inferido

        consulta = "INSERT INTO marcados(marcacion, tipo, FK_empleado, FK_dispositivos) VALUES (%s, %s, %s, %s);"
        cursor.execute(consulta, (timestamp_marcacion, tipo_marcacion, id_empleado, nombre_ZK))

    cursor.connection.commit()
    cursor.close()

