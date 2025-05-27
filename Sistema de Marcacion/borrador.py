# Pantalla de empleados
# @app.route('/empleados')
# def empleados():
#     if 'usuario' not in session:
#         return redirect(url_for('login'))

#     empleados = obtener_empleados()
#     return render_template("empleados.html", empleados=empleados, usuario=session['usuario'])






horas_trabajadas = None
horas_trabajadas_decimales = round(horas_trabajadas.total_seconds() / 3600, 1)
print(horas_trabajadas_decimales)





def EntradaoSalida(marcacion):
    empleado = obtener_empleado(marcacion.user_id)
    departamento = obtener_departamento(empleado['FK_departamento'])
    horarios_lista = obtener_horario(departamento['FK_horarios'])
    horarios = horarios_lista[0]

    fecha_marcacion = marcacion.timestamp.date()
    hora_marcacion = marcacion.timestamp

    entrada_manana = datetime.combine(fecha_marcacion, asegurar_time(horarios['entrada_manana']))
    tolerancia_manana = datetime.combine(fecha_marcacion, asegurar_time(horarios['tolerancia_manana']))
    salida_manana = datetime.combine(fecha_marcacion, asegurar_time(horarios['salida_manana']))

    entrada_tarde = datetime.combine(fecha_marcacion, asegurar_time(horarios['entrada_tarde']))
    tolerancia_tarde = datetime.combine(fecha_marcacion, asegurar_time(horarios['tolerancia_tarde']))
    salida_tarde = datetime.combine(fecha_marcacion, asegurar_time(horarios['salida_tarde']))

    tipo = ''
    detalle = ''
    horas_trabajadas = timedelta(0)
    horas_trabajadas_decimales = None

    # Salida mañana (verificar antes de entrada tarde para evitar conflictos)
    if salida_manana - timedelta(minutes=10) <= hora_marcacion < entrada_tarde:
        tipo = 'salida'
        detalle = None
        horas_trabajadas = hora_marcacion - entrada_manana 
        horas_trabajadas_decimales = timedelta(hours=round(horas_trabajadas.total_seconds() / 3600, 0))

    # Entrada mañana
    elif entrada_manana <= hora_marcacion <= tolerancia_manana:
        tipo = 'entrada'
        detalle = 'a tiempo'
    elif tolerancia_manana < hora_marcacion < salida_manana:
        tipo = 'entrada'
        detalle = 'tarde'

    # Salida tarde (se verifica antes que cualquier otra entrada por la tarde)
    elif salida_tarde - timedelta(minutes=10) <= hora_marcacion:
        tipo = 'salida'
        detalle = None
        horas_trabajadas = hora_marcacion - entrada_tarde
        horas_trabajadas_decimales = timedelta(hours=round(horas_trabajadas.total_seconds() / 3600, 0))

    # Entrada tarde
    elif entrada_tarde <= hora_marcacion <= tolerancia_tarde:
        tipo = 'entrada'
        detalle = 'a tiempo'
    elif tolerancia_tarde < hora_marcacion < salida_tarde:
        tipo = 'entrada'
        detalle = 'tarde'

    return tipo, detalle, horas_trabajadas_decimales
