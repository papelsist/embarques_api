from .report_pdf import ReportPDF
from .report_dao import ReportDao
from datetime import datetime



def reporte_incidencia(envio_id):
    query = """
            select 
            ei.envio_id, ei.id,sucursal,operador, embarque, documento,ei.fecha_documento,entidad,origen,tipo_documento,destinatario,valor,ei.fecha,clave,descripcion,cantidad, img1, img2, img3,
            ei.comentario,
            es.*
            from entrega_incidencia ei left join entrega_incidencia_seguimiento es on (ei.id = es.incidencia_id)
            where envio_id = %s
            """
    dao = ReportDao()
    incidencias = dao.get_data(query,[envio_id])