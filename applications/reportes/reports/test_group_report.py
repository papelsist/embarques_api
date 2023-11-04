from .report_pdf import ReportPDF
from .report_dao import ReportDao
from .report_utils import get_grouped_data
from datetime import date

def test_report():
    
    parametros = {
        'fecha' : '2021-10-11',
        'sucursal1':'BOLIVAR',
        'sucursal3':'BOLIVAR',
        'sucursal2':'BOLIVAR',    
    }

    query = """
            select 
            e.id as embarque_id,e.documento ,e.fecha,e .or_fecha_hora_salida ,o.nombre, e.comentario 
            ,e2.id as entrega_id,e2.sucursal ,e2.destinatario, e2.documento as documento_envio ,e2.origen ,e2.entidad,e2.fecha_documento 
            ,ed.id as entrega_det_id,ed.clave,ed.descripcion, ed.cantidad,ed .valor 
            from embarques e join entrega e2  on (e.id = e2.embarque_id) join entrega_det ed on (ed.entrega_id =e2.id) join operador o on (e.operador_id  = o.id)
            where e.id = 66
            order by e2.id;
            """
    pdf = ReportPDF('P','mm','Letter','PAPEL S.A. DE C.V','Reporte de Asignación',parametros= parametros )
    dao = ReportDao()
    pdf.add_page()
    data = dao.get_data(query)
    print("_"*50)
    data_embarque = get_grouped_data(data,"documento_envio")
    print(data_embarque)
    for key in data_embarque:

        data_list_entrega = data_embarque[key]
        current_y = pdf.get_y()
        pdf.line(10,current_y,206,current_y)
        pdf.set_font('helvetica', 'B', 12)
        pdf.cell(20, 8, str(data_list_entrega[0]['documento_envio']) )
        pdf.cell(25, 8, (data_list_entrega[0]['fecha_documento']).strftime("%d-%m-%Y"), )
        pdf.cell(50, 8, str(data_list_entrega[0]['destinatario']) , new_x="LMARGIN", new_y="NEXT")
        pdf.set_font('helvetica', '', 10)
        current_y = pdf.get_y()
        pdf.line(10,current_y,206,current_y)

        data_entrega = get_grouped_data(data_list_entrega,"documento_envio")
        print("*"*50)
        print(data_entrega)


        for key in data_entrega:

            data_list_entrega= data_entrega[key]
            pdf.set_font('helvetica', 'B', 10)
            pdf.cell(20, 8, str(data_list_entrega[0]['documento_envio']) )
            pdf.cell(25, 8, (data_list_entrega[0]['fecha_documento']).strftime("%d-%m-%Y"), )
            pdf.cell(50, 8, str(data_list_entrega[0]['destinatario']) , new_x="LMARGIN", new_y="NEXT")
            pdf.set_font('helvetica', '', 10)
            current_y = pdf.get_y()
            pdf.line(10,current_y,206,current_y)

            acum_importe = 0 

                
            with pdf.table(first_row_as_headings=False,borders_layout="NONE", col_widths=(50,80,30,30,30), text_align=("LEFT", "LEFT", "RIGHT","RIGHT","RIGHT"),align='CENTER') as table:

                for item in data_list_entrega:

                    #acum_importe += item['importe']
                    row = table.row()
                    row.cell(item['clave'])
                    row.cell(item['descripcion'])
                    row.cell(str(item['cantidad']))
                    row.cell(str(item['valor']))
                    row.cell("")
                    #row.cell(str(item['cliente']))
                    #row.cell(item['suc'])
                    #row.cell(date.strftime(item['fecha'],"%d-%m-%Y"))
                    #row.cell("{:,.2f}".format(item['importe']))
                    #row.cell("{:,.2f}".format(acum_importe)) 

                pdf.set_font('helvetica', 'B', 10)
                row = table.row()
                row.cell("")
                row.cell("")
                row.cell("Total: ")
                row.cell("{:,.2f}".format(acum_importe))
                row.cell("")
                pdf.set_font('helvetica', '', 10) 
                


    reporte = bytes(pdf.output())
    
   
    return reporte