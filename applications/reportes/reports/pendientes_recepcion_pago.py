from fpdf import FPDF
from django.db.models import Q
from datetime import datetime
from decimal import Decimal
from applications.embarques.models import Entrega



class ReportPDF(FPDF):
    """Clase template para generar reportes en PDF.
    """
    def __init__(self, orientation = 'P', unit= 'mm', format= 'Letter', empresa = 'Empresa', titulo = 'Reporte',parametros = None):
        super().__init__(orientation, unit, format)
        
        self.empresa = empresa
        self.titulo = titulo
        self.parametros = parametros 
        self.coord_x = 10
        self.width_detail = 0 
        self.orientation = orientation
        self.data = []
       
    def header(self):
        """Sobre escritura del metodo header de FPDF para personalizacion.
        """
        self.set_font('helvetica', 'B', 12)
        # Empresa
        self.cell(0, 5, self.empresa, 0, 1, 'R')
        # Parametros Izquierda
        self.set_font('helvetica', '', 10)
        # Titulo Reporte
        #width_titulo = self.get_string_width(self.titulo.upper())
        #self.set_x(206 - width_titulo )
        self.cell(0, 5,self.titulo, 0, 1, 'R')
        # Paramteros
        if self.parametros:
            self.cell(140, 5, f"CHOFER: {self.parametros['operador']}", 0, 0, 'L')
            fecha_dt = datetime.strptime(self.parametros['fecha'], "%Y-%m-%d")
            fecha = fecha_dt.strftime("%d/%m/%Y")
            self.cell(56, 5, f"FECHA: {fecha}", 0, 1, 'R')

        current_y = self.get_y()
        if self.orientation == "P":
            self.line(10,current_y,206,current_y)
        else:
            self.line(10,current_y,272,current_y)
             
        self.set_font('helvetica', 'B', 8)
        self.cell(20, 5,'DOCUMENTO',align="C")
        self.cell(20, 5, 'FECHA',align="C" )
        self.cell(20, 5, 'EMBARQUE',align="C" )
        self.cell(70, 5, 'CHOFER',align="C" )
        self.cell(20, 5, 'SALIDA',align="C" )
        self.cell(20, 5, 'RECEPCION',align="C" )
        self.cell(30, 5, 'IMPORTE',align="C", new_x="LMARGIN", new_y="NEXT")

        current_y = self.get_y()
        
        if self.orientation == "P":
            self.line(10,current_y,206,current_y)
        else:
            self.line(10,current_y,272,current_y)
        
    # Page footer
    def footer(self):
        """
            Sobre escritura del metodo footer para personalizacion.
        """
        # Position at 1 cm from bottom
        self.set_y(-15)

        # helvetica italic 8
        self.set_font('helvetica', 'I', 6)
        size_footer = 64.5
        if self.orientation == "L":
             size_footer = 87  
   
        # Page number
        self.cell(size_footer, 10, 'SIIPAP', 'T', 0, 'C')
        self.cell(size_footer, 10, 'Pagina ' + str(self.page_no()) + ' de {nb}', 'T', 0, 'C')
        self.cell(size_footer, 10,'IMPRESO: ' + str(datetime.now().strftime("%d/%m/%Y %I:%M%p")), 'T', 0, 'C')


def reporte_pendientes_recepcion_pago(sucursal):
    
    pendientes = Entrega.objects.filter(~Q(operador = 'CLIENTE PASAN'),recepcion_pago__isnull=True, tipo_documento='COD', sucursal=sucursal).order_by('documento')


    pdf = ReportPDF('P','mm','Letter','PAPEL S.A. DE C.V',f"FACTURAS COD PENDIENTES DE RECEPCION DE PAGO ( {sucursal} )" )
    pdf.add_page()

    for pendiente in pendientes:
        pdf.set_font('helvetica', '', 8)
        pdf.cell(20, 5, str(pendiente.documento),align="C")
        pdf.cell(20, 5, str(pendiente.fecha_documento.strftime("%d/%m/%Y")),align="C")
        pdf.cell(20, 5, str(pendiente.embarque.documento),align="C")
        pdf.cell(50, 5, str(pendiente.operador),align="L")
        pdf.cell(35, 5, str(pendiente.salida.strftime("%d/%m/%Y %H:%M:%S") if pendiente.salida != None else '' ),align="C")
        pdf.cell(35, 5, str(pendiente.recepcion.strftime("%d/%m/%Y %H:%M:%S") if pendiente.recepcion != None else ''),align="C")
        pdf.cell(15, 5, str(pendiente.envio.total_documento),align="R", new_x="LMARGIN", new_y="NEXT")

        

    reporte = bytes(pdf.output())
    return reporte
    