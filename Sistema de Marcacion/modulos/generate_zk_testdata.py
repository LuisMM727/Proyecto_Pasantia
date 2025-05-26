import random
import datetime
from zk.attendance import Attendance

# Hora de entrada a las 06:55
def get_realistic_check_in_time(base_time):
    minute_range = list(range(-3, 31))
    weights = []
    for minute in minute_range:
        if minute <= 3:
            weights.append(85)
        elif -5 <= minute <= 5:
            weights.append(10)
        else:
            weights.append(1)
    selected_minute = random.choices(minute_range, weights=weights, k=1)[0]
    selected_second = random.randint(0, 59)
    return base_time + datetime.timedelta(minutes=selected_minute, seconds=selected_second)

# Hora de salida (18:00)
def get_realistic_check_out_time(base_time):
    minute_range = list(range(-1, 61))
    weights = []
    for minute in minute_range:
        if minute <= 5:
            weights.append(80)
        elif -10 <= minute <= 10:
            weights.append(10)
        else:
            weights.append(1)
    selected_minute = random.choices(minute_range, weights=weights, k=1)[0]
    selected_second = random.randint(0, 59)
    return base_time + datetime.timedelta(minutes=selected_minute, seconds=selected_second)

# Salida para almuerzo (12:00)
def get_realistic_lunch_out_time(base_time):
    minute_range = list(range(-2, 6))  # Salen entre 11:58 y 12:06
    weights = [80 if -1 <= m <= 2 else 10 for m in minute_range]
    selected_minute = random.choices(minute_range, weights=weights, k=1)[0]
    selected_second = random.randint(0, 59)
    return base_time + datetime.timedelta(minutes=selected_minute, seconds=selected_second)

# Entrada después del almuerzo (13:30)
def get_realistic_lunch_in_time(base_time):
    minute_range = list(range(-3, 6))  # Entran entre 13:27 y 13:36
    weights = [80 if 0 <= m <= 3 else 10 for m in minute_range]
    selected_minute = random.choices(minute_range, weights=weights, k=1)[0]
    selected_second = random.randint(0, 59)
    return base_time + datetime.timedelta(minutes=selected_minute, seconds=selected_second)

# Generador de asistencia
def generate_realistic_Attendance(num_employees=5, days=10, start_date=None):
    if start_date is None:
        start_date = datetime.date.today() - datetime.timedelta(days=days)

    Attendance_records = []
    employee_ids = [f"{1000 + i}" for i in range(num_employees)]

    for day in range(days):
        date = start_date + datetime.timedelta(days=day)

        # if date.weekday() >= 5:
        #     continue

        for emp_id in employee_ids:
            if random.random() < 0.05:
                continue  # Empleado ausente

            # Entrada en la mañana
            if random.random() > 0.025:
                base_check_in = datetime.datetime.combine(date, datetime.time(6, 55))
                check_in_time = get_realistic_check_in_time(base_check_in)
                Attendance_records.append(Attendance(user_id=emp_id, timestamp=check_in_time, status=0))

            # Salida para almuerzo
            if random.random() > 0.01:
                base_lunch_out = datetime.datetime.combine(date, datetime.time(12, 0))
                lunch_out_time = get_realistic_lunch_out_time(base_lunch_out)
                Attendance_records.append(Attendance(user_id=emp_id, timestamp=lunch_out_time, status=1))

            # Entrada después de almuerzo
            if random.random() > 0.01:
                base_lunch_in = datetime.datetime.combine(date, datetime.time(13, 30))
                lunch_in_time = get_realistic_lunch_in_time(base_lunch_in)
                Attendance_records.append(Attendance(user_id=emp_id, timestamp=lunch_in_time, status=0))

            # Salida final
            if random.random() > 0.025:
                base_check_out = datetime.datetime.combine(date, datetime.time(18, 0))
                check_out_time = get_realistic_check_out_time(base_check_out)
                Attendance_records.append(Attendance(user_id=emp_id, timestamp=check_out_time, status=1))

    return sorted(Attendance_records, key=lambda x: (x.timestamp, x.user_id))

# Generar los datos
data = generate_realistic_Attendance(num_employees=4, days=10)

# print(data)