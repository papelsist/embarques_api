from .report_pdf import ReportPDF
from .report_dao import ReportDao





def asignacion_envio(embarque):

    print(embarque)

    query = """
            select 
            e.id,e.documento ,e.fecha,e .or_fecha_hora_salida ,o.nombre, e.comentario 
            ,e2.id,e2.sucursal ,e2.destinatario, e2.documento as documento_envio ,e2.origen ,e2.entidad,e2.fecha_documento 
            ,ed.id,ed.clave,ed.descripcion, ed.cantidad,ed .valor 
            from embarques e join entrega e2  on (e.id = e2.embarque_id) join entrega_det ed on (ed.entrega_id =e2.id) join operador o on (e.operador_id  = o.id)
            where e.id = 66
            order by e2.id;
            """
    
    dao = ReportDao()
    data = dao.get_data(query)

    fecha_embarque = data[0]['fecha']
    parametros = {
        'fecha' : fecha_embarque.strftime("%d-%m-%Y"),
        'sucursal1':'BOLIVAR',
        'sucursal3':'BOLIVAR',
        'sucursal2':'BOLIVAR',    
    }

    pdf = ReportPDF('P','mm','Letter','PAPEL S.A. DE C.V','REPORTE DE ASIGNACION',parametros= parametros)
    pdf.add_page()
    

    with pdf.table(borders_layout="NONE", col_widths=(15,30,30), text_align=("LEFT", "LEFT", "RIGHT"),align='CENTER') as table:
        row = table.row()
        row.cell('DOCUMENTO')
        row.cell('FECHA')
        pdf.line(10,32,206,32)

        for item in data:
            row = table.row()
            row.cell(str(item['documento_envio']))
            row.cell((item['fecha_documento']).strftime("%d-%m-%Y"))

        if(data):
            row = table.row()
            row.cell('TOT_CLAVE')
            row.cell('TOT_NOMBRE')
    reporte = bytes(pdf.output())
    return reporte