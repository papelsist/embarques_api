from .report_pdf import ReportPDF
from .report_dao import ReportDao





def asignacion_envio():

    parametros = {
        'fecha' : '2021-10-11',
        'sucursal1':'BOLIVAR',
        'sucursal3':'BOLIVAR',
        'sucursal2':'BOLIVAR',    
    }

    query = "Select * from sucursal_bi"
    pdf = ReportPDF('P','mm','Letter','PAPEL S.A. DE C.V','SUCURSALES',query,parametros= parametros)
    dao = ReportDao()
    pdf.add_page()
    data = dao.get_data(query)

    with pdf.table(borders_layout="NONE", col_widths=(15,30,30), text_align=("LEFT", "LEFT", "RIGHT"),align='CENTER') as table:
        row = table.row()
        row.cell('CLAVE')
        row.cell('NOMBRE')
        pdf.line(10,32,206,32)

        for item in data:
            print(item)
            row = table.row()
            row.cell(str(item['clave']))
            row.cell(item['nombre'])

        if(data):
            row = table.row()
            row.cell('TOT_CLAVE')
            row.cell('TOT_NOMBRE')
    reporte = bytes(pdf.output())
    return reporte