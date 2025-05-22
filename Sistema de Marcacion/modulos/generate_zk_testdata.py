import random
import datetime
from zk.attendance import Attendance

# Función auxiliar para generar hora de entrada realista
def get_realistic_check_in_time(base_time):
    # Minutos desde -3 (temprano) a +30 (tarde)
    minute_range = list(range(-3, 31))

    weights = []
    for minute in minute_range:
        if minute <= 3:
            weights.append(85)  # 85% de probabilidad de llegar entre 06:53 y 07:58
        elif -5 <= minute <= 5:
            weights.append(10)  # Algunos llegan un poco más temprano o tarde
        else:
            weights.append(1)   # Casos raros

    selected_minute = random.choices(minute_range, weights=weights, k=1)[0]
    selected_second = random.randint(0, 59)
    return base_time + datetime.timedelta(minutes=selected_minute, seconds=selected_second)

# Función auxiliar para generar hora de salida realista
def get_realistic_check_out_time(base_time):
    # Minutos desde -1 (salida anticipada) a +60 (salida tardía)
    minute_range = list(range(-1, 61))

    weights = []
    for minute in minute_range:
        if minute <= 5:
            weights.append(80)  # La mayoría sale entre 17:55 y 18:05
        elif -10 <= minute <= 10:
            weights.append(10)  # Salidas razonablemente cerca
        else:
            weights.append(1)   # Salidas muy fuera de lo normal

    selected_minute = random.choices(minute_range, weights=weights, k=1)[0]
    selected_second = random.randint(0, 59)
    return base_time + datetime.timedelta(minutes=selected_minute, seconds=selected_second)

# Función principal para generar los datos de asistencia
def generate_realistic_Attendance(num_employees=5, days=10, start_date=None):
    if start_date is None:
        start_date = datetime.date.today() - datetime.timedelta(days=days)

    Attendance_records = []
    employee_ids = [f"{1000 + i}" for i in range(num_employees)]

    for day in range(days):
        date = start_date + datetime.timedelta(days=day)

        # Saltar fines de semana
        if date.weekday() >= 5:
            continue

        for emp_id in employee_ids:
            # 10% de probabilidad de que el empleado falte completamente
            if random.random() < 0.05:
                continue

            # 5% de probabilidad de olvidar marcar entrada
            if random.random() > 0.025:
                base_check_in = datetime.datetime.combine(date, datetime.time(6, 55))
                check_in_time = get_realistic_check_in_time(base_check_in)
                Attendance_records.append(Attendance(user_id=emp_id, timestamp=check_in_time, status=0))

            # 5% de probabilidad de olvidar marcar salida
            if random.random() > 0.025:
                base_check_out = datetime.datetime.combine(date, datetime.time(18, 0))
                check_out_time = get_realistic_check_out_time(base_check_out)
                Attendance_records.append(Attendance(user_id=emp_id, timestamp=check_out_time, status=1))

    # Ordenar registros por fecha y usuario
    return sorted(Attendance_records, key=lambda x: (x.timestamp, x.user_id))


# Generar los datos
data = generate_realistic_Attendance(num_employees=1, days=2)

# Imprimir los registros generados
# i = 1
# for record in data:
#     print(i, record)

#     i += 1
