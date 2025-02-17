from .report_pdf import ReportPDF
from .report_dao import ReportDao
from .report_utils import get_grouped_data
from datetime import date
from decimal import Decimal

def asignacion_embarque(embarque):
    query = """
            select 
            e.id as embarque_id,e.documento ,e.fecha,e .or_fecha_hora_salida ,o.nombre, e.comentario
            ,e2.envio_id, e2.paquetes,e2.id as entrega_id,e2.sucursal ,e2.destinatario, e2.documento as documento_envio 
            ,e2.origen ,e2.entidad,e2.fecha_documento,e2.valor,e2.kilos
            ,i.fecha_de_entrega,CONCAT(direccion_calle, "  #",direccion_numero_exterior,"  ", direccion_colonia," C.P."
            ,direccion_codigo_postal,"  ", direccion_municipio,"  ",direccion_estado) as direccion
            from embarques e join entrega e2  on (e.id = e2.embarque_id) join operador o on (e.operador_id  = o.id)
            join instruccion_de_envio i on (i.envio_id = e2.envio_id)
            where e.id = %s
            order by e2.id
            """
    dao = ReportDao()
    embarque = dao.get_data(query,[embarque])
    fecha_embarque = embarque[0]['fecha']
    parametros = {
        'fecha' : fecha_embarque.strftime("%d-%m-%Y"),
        'sucursal1':'BOLIVAR',
        'sucursal3':'BOLIVAR',
        'sucursal2':'BOLIVAR',    
    }
    pdf = ReportPDF('P','mm','Letter','PAPEL S.A. DE C.V','Reporte de Asignación',parametros= parametros )
    pdf.add_page()
    # Encabezados Reporte
    pdf.set_font('helvetica', 'B', 10)
    pdf.cell(15, 5,'ORIGEN',align="C")
    pdf.cell(25, 5, 'DOCUMENTO',align="C" )
    pdf.cell(80, 5, 'CLIENTE',align="C" )
    pdf.cell(20, 5, 'FECHA',align="C" )
    pdf.cell(20, 5, 'IMPORTE',align="C" )
    pdf.cell(20, 5, 'KILOS',align="C", new_x="LMARGIN", new_y="NEXT")


    current_y = pdf.get_y()
    pdf.line(10,current_y,205,current_y)

    total_kilos = Decimal(0.00)
    total_importe = Decimal(0.00)

    for entrega in embarque:
        current_y = pdf.get_y()
        pdf.set_font('helvetica', '', 10)
        pdf.cell(15, 5, entrega['origen'],align="C")
        pdf.cell(25, 5, str(entrega['documento_envio']),align='C' )
        pdf.truncated_cell(80, 5, entrega['destinatario'],align="L")
        pdf.cell(20, 5, entrega['fecha_documento'].strftime("%d-%m-%Y"),align="C")
        
        pdf.cell(20, 5, "{:,.2f}".format(entrega['valor']),align="C")
        pdf.cell(20, 5, "{:,.2f}".format(entrega['kilos']),align="C" , new_x="LMARGIN", new_y="NEXT")

        pdf.cell(15, 5, "PAQUETES= " ,align="L")
        pdf.cell(30, 5, str(entrega['paquetes'] if  entrega['paquetes'] else "0"),align="C" , new_x="LMARGIN", new_y="NEXT")

        pdf.cell(23, 5, "DIR_ENVIO= " ,align="L")
        direccion = ''
        if entrega['direccion'] != None:
            direccion = entrega['direccion']
            
        pdf.cell(60, 5, direccion, new_x="LMARGIN", new_y="NEXT")

        pdf.cell(25, 5, "F_ENTREGA= " ,align="L")
        pdf.cell(15, 5, entrega['fecha_de_entrega'].strftime("%d-%m-%Y") ,align="L")
        pdf.cell(30, 5, "",align="C" , new_x="LMARGIN", new_y="NEXT")

        pdf.line(10,current_y+20,205,current_y+20)

        total_kilos += 0 if entrega.get('kilos') == None else entrega.get('kilos')
        total_importe += 0 if entrega.get('valor') == None else entrega.get('valor')
    
    pdf.set_x(130)
    pdf.cell(20, 5,'TOTAL: ', align='R',border=0)
    pdf.cell(20, 5, "{:,.2f}".format(total_importe), align='C',border=0)
    pdf.cell(15, 5, "{:,.2f}".format(total_kilos), align='C',border=0, new_x="LMARGIN", new_y="NEXT")
 
    reporte = bytes(pdf.output())
    return reporte
