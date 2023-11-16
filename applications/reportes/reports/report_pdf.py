from fpdf import FPDF
from fpdf.template import FlexTemplate, Template
from datetime import datetime




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
        # Logo
        #self.image('logo_pb.png', 10, 8, 33)
        # helvetica bold 15
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
            if(self.parametros.get('fecha')):
                # Fecha
                self.set_x(157)
                self.cell(30, 5,'FECHA: ', 0, 0, 'R')
                self.cell(20, 5,self.parametros.get('fecha'), 0, 0, 'C')
        if self.orientation == "P":
            self.line(10,26,206,26)
        else:
            self.line(10,26,272,26)
        self.set_y(26)
  
    # Page footer
    def footer(self):
        """Sobre escritura del metodo footer para personalizacion.
        """
        # Position at 1 cm from bottom
        self.set_y(-15)
        # helvetica italic 8
        self.set_font('helvetica', 'I', 6)
        # Page number
        self.cell(64.5, 10, 'SIIPAP', 'T', 0, 'C')
        self.cell(64.5, 10, 'Pagina ' + str(self.page_no()) + ' de {nb}', 'T', 0, 'C')
        self.cell(64.5, 10,'IMPRESO: ' + str(datetime.now().strftime("%d/%m/%Y %I:%M%p")), 'T', 0, 'C')

    
