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