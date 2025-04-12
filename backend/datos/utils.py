from datetime import datetime

def obtener_inicio_y_fin_del_dia():
    """
    Retorna el inicio del día (00:00:00) y la hora actual como fin del día.
    """
    fecha_actual = datetime.now()
    inicio_dia = fecha_actual.replace(hour=0, minute=0, second=0, microsecond=0)
    fin_dia = fecha_actual
    return inicio_dia, fin_dia
