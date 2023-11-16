from .report_pdf import ReportPDF
from .report_dao import ReportDao
from datetime import datetime


def sugerencia_ruta(ruta):

    pdf = ReportPDF('P','mm','Letter','PAPEL S.A. DE C.V','SUGERENCIA RUTA')
    pdf.add_page()
    pdf.set_font('helvetica', 'B', 10)
    pdf.cell(30, 5, 'DOCUMENTO',align="C" )
    pdf.cell(50, 5, 'FECHA',align="C" )
    pdf.cell(70, 5, 'CLIENTE',align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.line(10,31,206,31)
    #print(ruta['destinos'])
    entregas_so = ruta['destinos']
    entregas = sorted(entregas_so, key  = lambda x: x['instruccion']['sector'])
    for entrega in entregas:
        print(entrega)
        pdf.ln(3)
        pdf.set_font('helvetica', '', 10)
        instruccion = entrega['instruccion']
        direccion = f"""{
                instruccion['direccion_calle']} {instruccion['direccion_numero_exterior']} {"" if instruccion['direccion_numero_interior'] == None else  instruccion['direccion_numero_interior']  } {instruccion['direccion_colonia']}"""
        pdf.cell(30, 5, entrega['documento'],align="C" )
        pdf.cell(50, 5, datetime.fromisoformat(entrega['fecha_documento']).strftime("%d-%m-%Y"),align="C" )
        pdf.cell(70, 5, entrega['destinatario'],align="L", new_x="LMARGIN", new_y="NEXT")
        pdf.cell(120, 5, direccion ,align="L", new_x="LMARGIN", new_y="NEXT" )
        pdf.cell(70, 5,f"Distancia: {instruccion['distancia']} Km.",align="L" )
        pdf.cell(120, 5, f"Sector: {instruccion['sector']}" ,align="L", new_x="LMARGIN", new_y="NEXT" )
        pdf.ln(3)
        if pdf.get_y() > 250: 
            print("Agregando una página al reporte")
            pdf.add_page() 
            pdf.set_font('helvetica', 'B', 10)
            pdf.cell(30, 5, 'DOCUMENTO',align="C" )
            pdf.cell(50, 5, 'FECHA',align="C" )
            pdf.cell(70, 5, 'CLIENTE',align="C", new_x="LMARGIN", new_y="NEXT")
            pdf.line(10,31,206,31)

        detalles = entrega['detalles']
        pdf.set_x(30)
        y_position = pdf.get_y()
        pdf.line(30,y_position,186,y_position)
        pdf.set_font('helvetica', 'B', 10)
        pdf.cell(30, 5, "CLAVE",align="L")
        pdf.cell(90, 5,"DESCRIPCION",align="L")
        pdf.cell(20, 5, "CANTIDAD",align="L")
        pdf.cell(20, 5, "KILOS",align="L", new_x="LMARGIN", new_y="NEXT") 
        y_position = pdf.get_y()
        pdf.line(30,y_position,186,y_position)
        for detalle in detalles:
            pdf.set_x(30)
            pdf.set_font('helvetica', '', 10)
            pdf.cell(30, 5, detalle['clave'],align="L")
            pdf.cell(90, 5, detalle['me_descripcion'],align="L")
            pdf.cell(20, 5, detalle['me_cantidad'],align="L")
            pdf.cell(20, 5, detalle['me_kilos'],align="L", new_x="LMARGIN", new_y="NEXT") 
         
            if pdf.get_y() > 250: 
                pdf.add_page() 
                pdf.set_font('helvetica', 'B', 10)
                pdf.cell(30, 5, 'DOCUMENTO',align="C" )
                pdf.cell(50, 5, 'FECHA',align="C" )
                pdf.cell(70, 5, 'CLIENTE',align="C", new_x="LMARGIN", new_y="NEXT")
                pdf.line(10,31,206,31)
        
        pdf.ln(3)
        y_position = pdf.get_y()
        pdf.line(10,y_position,206,y_position)

        

    
   

   




    reporte = bytes(pdf.output())
    return reporte
