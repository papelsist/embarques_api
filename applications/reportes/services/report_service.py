from ..reports import asignacion_embarque, sugerencia_ruta, reporte_asignacion_embarque


def imprimir_reporte_asignacion(embarque):
    reporte = asignacion_embarque(embarque)
    return reporte

def imprimir_reporte_test_group(embarque):
    reporte = asignacion_embarque(embarque)
    return reporte


def imprimir_reporte_ruta(ruta):
   reporte = sugerencia_ruta(ruta)
   return reporte


def imprimir_reporte_asignacion_embarque(embarque):
    reporte = reporte_asignacion_embarque(embarque)
    return reporte