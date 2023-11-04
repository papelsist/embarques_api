from ..reports import asignacion_embarque, sugerencia_ruta


def imprimir_reporte_asignacion(embarque):
    reporte = asignacion_embarque(embarque)
    return reporte

def imprimir_reporte_test_group(embarque):
    reporte = asignacion_embarque(embarque)
    return reporte


def imprimir_reporte_ruta(ruta):
   reporte = sugerencia_ruta(ruta)
   return reporte