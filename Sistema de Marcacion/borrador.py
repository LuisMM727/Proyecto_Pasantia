#Funcion para saber si la marcacion es de tipo Entrada o Salida y cuantas horas trabajo 
def EntradaoSalida(marca):
    print("gfvgcffc")
    empleado = obtener_empleado(marca.user_id)
    departamento = obtener_departamento(empleado['FK_departamento'])
    horarios = obtener_horario(departamento['FK_horarios'])


    horario = horarios[0]
    hora = marca.timestamp.time()

    def to_time(val):
        if isinstance(val, time):
            return val
        elif isinstance(val, timedelta):
            total_seconds = val.total_seconds()
            horas = int(total_seconds // 3600)
            minutos = int((total_seconds % 3600) // 60)
            segundos = int(total_seconds % 60)
            return time(horas, minutos, segundos)
        elif isinstance(val, str):
            return datetime.strptime(val, "%H:%M:%S").time()
        else:
            raise ValueError(f"Tipo inesperado para convertir a time: {type(val)}")

    def to_timedelta(val):
        if isinstance(val, timedelta):
            return val
        elif isinstance(val, str):
            h, m, s = map(int, val.split(':'))
            return timedelta(hours=h, minutes=m, seconds=s)
        else:
            raise ValueError(f"Tipo inesperado para convertir a timedelta: {type(val)}")

    # Convertimos los datos del horario
    entrada_manana = to_time(horario['entrada_manana'])
    salida_manana = to_time(horario['salida_manana'])
    entrada_tarde = to_time(horario['entrada_tarde'])
    salida_tarde = to_time(horario['salida_tarde'])
    tolerancia_manana = to_timedelta(horario.get('tolerancia_manana', timedelta()))
    tolerancia_tarde = to_timedelta(horario.get('tolerancia_tarde', timedelta()))

    ahora = datetime.combine(datetime.today(), hora)
    entrada_m_dt = datetime.combine(datetime.today(), entrada_manana)
    salida_m_dt = datetime.combine(datetime.today(), salida_manana)
    entrada_t_dt = datetime.combine(datetime.today(), entrada_tarde)
    salida_t_dt = datetime.combine(datetime.today(), salida_tarde)
    print(entrada_m_dt)
    print(salida_m_dt)
    print(entrada_t_dt)
    print(salida_t_dt)
    print(tolerancia_manana)
    print(tolerancia_tarde)
    print(ahora)
    print("--------------------------------------------------")
    tipo = None
    detalle = None
    horas_trabajadas = None

    # Rango entrada mañana
    if entrada_m_dt <= ahora <= entrada_m_dt:
        tipo = 'entrada'
    # Rango salida mañana
    elif salida_m_dt - timedelta(minutes=30) <= ahora <= salida_m_dt + timedelta(minutes=30):
        tipo = 'salida'
        horas_trabajadas = salida_m_dt - entrada_m_dt
    # Rango entrada tarde
    elif entrada_t_dt <= ahora <= entrada_t_dt + tolerancia_tarde:
        tipo = 'entrada'
    # Rango salida tarde
    elif salida_t_dt - timedelta(minutes=30) <= ahora <= salida_t_dt + timedelta(minutes=30):
        tipo = 'salida'
        horas_trabajadas = salida_t_dt - entrada_t_dt
    else:
        # Fuera de horario conocido
        tipo = 'entrada'
        detalle = 'fuera de horario'

    return tipo, detalle, horas_trabajadas