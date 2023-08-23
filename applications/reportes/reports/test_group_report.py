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

    query = """SELECT * from analisis_ventas_det avd  where fecha = '2023-07-27' order by suc limit 1000;"""
    pdf = ReportPDF('P','mm','Letter','PAPEL S.A. DE C.V','SUCURSALES',parametros= parametros )
    dao = ReportDao()
    pdf.add_page()
    data = dao.get_data(query)

    data_suc = get_grouped_data(data,"suc")

    for key in data_suc:

        data_list_suc = data_suc[key]
        current_y = pdf.get_y()
        pdf.line(10,current_y,206,current_y)
        pdf.set_font('helvetica', 'B', 12)
        pdf.cell(10, 8, key , new_x="LMARGIN", new_y="NEXT")
        pdf.set_font('helvetica', '', 10)
        current_y = pdf.get_y()
        pdf.line(10,current_y,206,current_y)

        data_origen = get_grouped_data(data_list_suc,"origen")

        for key in data_origen:

            data_list_origen= data_origen[key]
            pdf.set_font('helvetica', 'B', 10)
            pdf.cell(10, 8, key )
            pdf.set_x(100)
            pdf.cell(50, 8, key , new_x="LMARGIN", new_y="NEXT")
            pdf.set_font('helvetica', '', 10)
            current_y = pdf.get_y()
            pdf.line(10,current_y,206,current_y)

            acum_importe = 0

            with pdf.table(first_row_as_headings=False,borders_layout="NONE", col_widths=(50,30,30,30,30), text_align=("LEFT", "LEFT", "RIGHT","RIGHT","RIGHT"),align='CENTER') as table:

                for item in data_list_origen:

                    acum_importe += item['importe']
                    row = table.row()
                    row.cell(str(item['cliente']))
                    row.cell(item['suc'])
                    row.cell(date.strftime(item['fecha'],"%d-%m-%Y"))
                    row.cell("{:,.2f}".format(item['importe']))
                    row.cell("{:,.2f}".format(acum_importe)) 

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