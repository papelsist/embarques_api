from ..reports import asignacion_envio, test_report


def imprimir_reporte_asignacion():
    reporte = asignacion_envio()
    return reporte

def imprimir_reporte_test_group():
    reporte = test_report()
    return reporte