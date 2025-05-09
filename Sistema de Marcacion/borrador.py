from zk import ZK
from modulos.funciones import obtener_dispositivos
#Funcion para conectar al dispositivo ZK para capturar los datos
def Capturar_DatosZK():
    dispositivos = obtener_dispositivos()
    for dispositivo in dispositivos:
        zk = ZK('192.168.150.34', port=4370, timeout=5)
        print(zk,"hola")
        conn = zk.connect()
        conn.disable_device()
        users = conn.get_attendance()
        conn.enable_device()
        conn.disconnect()
        print(users)



# def dispositivo_ZK(ip, puerto):

#     zk = ZK(ip, port=puerto, timeout=5)
#     conn = zk.connect()
#     conn.disable_device()
#     conn.enable_device()
#     conn.disconnect()
#Capturar_DatosZK()

zk = ZK('192.168.150.34', port=4370, timeout=5)
print(zk,"hola")
conn = zk.connect()
conn.disable_device()
users = conn.get_attendance()
conn.enable_device()
conn.disconnect()
print(type(users))