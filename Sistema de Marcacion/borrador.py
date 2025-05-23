def EntradaoSalida(marcacion):
    empleado = obtener_empleado(marcacion.user_id)
    departamento = obtener_departamento(empleado['FK_departamento'])
    
    horarios_lista = obtener_horario(departamento['FK_horarios'])
    if not horarios_lista:
        raise ValueError("No se encontró un horario para el departamento.")
    horarios = horarios_lista[0]  

    hora_marcacion = marcacion.timestamp.time()
    hora_dt = datetime.combine(datetime.today(), hora_marcacion)

    entrada_mañana = datetime.combine(datetime.today(), asegurar_time(horarios['entrada_manana']))
    tolerancia_mañana = datetime.combine(datetime.today(), asegurar_time(horarios['tolerancia_manana']))
    salida_manana = datetime.combine(datetime.today(), asegurar_time(horarios['salida_manana']))

    entrada_tarde = datetime.combine(datetime.today(), asegurar_time(horarios['entrada_tarde']))
    tolerancia_tarde = datetime.combine(datetime.today(), asegurar_time(horarios['tolerancia_tarde']))
    salida_tarde = datetime.combine(datetime.today(), asegurar_time(horarios['salida_tarde']))

    tipo = ''
    detalle = ''
    horas_trabajadas = timedelta(0)

    # Evaluar entrada mañana
    if entrada_mañana <= hora_dt <= tolerancia_mañana:
        tipo = 'entrada'
        detalle = 'None'
    elif hora_dt < entrada_mañana:
        tipo = 'entrada'
        detalle = 'temprano'
    elif tolerancia_mañana < hora_dt:
        tipo = 'entrada'
        detalle = 'tarde'

    # Evaluar salida mañana
    if tipo == '':
        if hora_dt <= salida_manana or hora_dt >= salida_manana:
            tipo = 'salida'
            detalle = 'None'
            horas_trabajadas = hora_dt - entrada_mañana


    # Evaluar entrada tarde
    if tipo == '':
        if entrada_tarde <= hora_dt <= tolerancia_tarde:
            tipo = 'entrada'
            detalle = 'None'
        elif hora_dt < entrada_tarde:
            tipo = 'entrada'
            detalle = 'temprano'
        elif tolerancia_tarde < hora_dt:
            tipo = 'entrada'
            detalle = 'tarde'

    # Evaluar salida tarde
    if tipo == '':
        if hora_dt <= salida_tarde or hora_dt >= salida_tarde:
            tipo = 'salida'
            detalle = 'None'
            horas_trabajadas = hora_dt - entrada_tarde


    # Si no se determinó tipo, se marca como entrada irregular
    if tipo == '':
        tipo = 'entrada'
        detalle = 'Irregular'

    horas_decimales = horas_trabajadas.total_seconds() / 3600

    return tipo, detalle, horas_decimales