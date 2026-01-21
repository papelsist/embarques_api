from ..reports import (asignacion_embarque, sugerencia_ruta, reporte_asignacion_embarque, reporte_entrega_doctos, reporte_pendientes_recepcion_pago,
                          reporte_pendientes_recepcion_doctos, reporte_envios_callcenter, reporte_embarques_chofer)


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

def imprimir_reporte_entrega(operador_id, sucursal_id, fecha):
    reporte = reporte_entrega_doctos(operador_id, sucursal_id, fecha)
    return reporte

def imprimir_reporte_pendientes_pago(sucursal):
    reporte = reporte_pendientes_recepcion_pago(sucursal)
    return reporte

def imprimir_reporte_pendientes_doctos(sucursal):
    reporte = reporte_pendientes_recepcion_doctos(sucursal)
    return reporte

def imprimir_reporte_callcenter(fecha_inicial, fecha_final):
    reporte = reporte_envios_callcenter(fecha_inicial, fecha_final)
    return reporte

def imprimir_reporte_embarques_chofer(operador_id, sucursal_id, fecha):
    reporte = reporte_embarques_chofer(operador_id, sucursal_id, fecha)
    return reporte  