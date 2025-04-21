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
        self.cell(0, 5,self.titulo, 0, 1, 'R')
        # Paramteros
        if self.parametros:
            if(self.parametros.get('fecha')):
                # Fecha
                if self.orientation == "P":
                     self.set_x(157)
                else:
                    self.set_x(218)
                
                self.cell(30, 5,'FECHA: ', 0, 0, 'R')
                self.cell(20, 5,self.parametros.get('fecha'), 0, 1, 'C')
               
            if(self.parametros.get('operador')):
                self.set_x(126)
                self.cell(30, 5,'OPERADOR: ', 0, 0, 'R')
                self.cell(20, 5,self.parametros.get('operador'), 0, 1, 'L')
     

    def truncated_cell(self, width, height, text, border=1, ln=0, align="L"):
        """
        Crea una celda con texto truncado si excede el ancho de la celda.
        """
        while self.get_string_width(text) > width:
            text = text[:-1]  # Elimina el último carácter

        self.cell(width, height, text , 0, ln, align)
  
    # Page footer
    def footer(self):
        """Sobre escritura del metodo footer para personalizacion.
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

    
