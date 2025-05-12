from zk import ZK
from modulos.funciones import obtener_dispositivos

def Capturar_DatosZK():
    dispositivos = obtener_dispositivos()
    for dispositivo in dispositivos:
        zk = ZK(dispositivo['IP_dispositivo'], port=dispositivo['puerto'], timeout=5)
        nombre_ZK = dispositivo['nombre_dispositivo']
        conn = zk.connect()
        conn.disable_device()
        users = conn.get_users()
        marcaciones = conn.get_attendance()
        conn.enable_device()
        conn.disconnect()
        UsuarioIn(users)
        Marcados(marcaciones,nombre_ZK)
