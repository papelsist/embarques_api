from .report_pdf import ReportPDF
from .report_dao import ReportDao



def sugerencia_ruta(ruta):
    print(ruta)
    pdf = ReportPDF('P','mm','Letter','PAPEL S.A. DE C.V','SUGERENCIA RUTA')
    pdf.add_page()
    reporte = bytes(pdf.output())
    return reporte
