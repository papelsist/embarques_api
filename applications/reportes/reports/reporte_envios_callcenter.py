
from fpdf import FPDF
from .report_dao import ReportDao
from .report_utils import get_grouped_data
from datetime import date, datetime
from decimal import Decimal


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
    
            self.set_font('helvetica', '', 10)

            if 'fecha_inicial' in self.parametros:
                fecha = f"FECHA EMBARQUE DEL : {self.parametros.get('fecha_inicial')} AL:  {self.parametros.get('fecha_final')}"
                len_fecha = len(fecha)
                self.set_x(272 - (len_fecha + 45) )
                self.cell(0, 5,fecha , 0, 1, 'L')

        current_y = self.get_y()
    
        self.set_y(current_y)      
                
        
        current_y = self.get_y()
        if self.orientation == "P":
            self.line(10,current_y,206,current_y)
        else:
            self.line(10,current_y,272,current_y)
        

             
        self.set_font('helvetica', 'B', 10)
        self.cell(25, 5, 'FECHA',align="C" )
        self.cell(35, 5, 'ATENDIO',align="C" ) 
        self.cell(25, 5, 'FACTURA',align="C" )
        self.cell(75, 5, 'CLIENTE',align="C" )
        self.cell(25, 5,'SUCURSAL',align="C")
        self.cell(30, 5, 'ENTREGA',align="C" )
        self.cell(40, 5, 'CHOFER',align="C", new_x="LMARGIN", new_y="NEXT")

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



def reporte_envios_callcenter(fecha_inicial, fecha_final):
    query = """
            select n.documento,e.documento ,e.fecha_documento , e.destinatario ,e.sucursal  
            ,n.arribo ,n.recepcion , n.recibio, o.nombre as chofer, e.create_user ,e.update_user 
            from envio e  join entrega n on (e.id= n.envio_id)   join embarques m on (n.embarque_id= m.id)   join operador o  on (m.operador_id = o.id)
            where callcenter  is not null and m.fecha between %s and %s
            """
    dao = ReportDao()
    envios = dao.get_data(query,[fecha_inicial, fecha_final])

    parametros = {
        'fecha_inicial' : fecha_inicial , 
        'fecha_final' : fecha_final,

    }
 
    pdf = ReportPDF('L','mm','Letter','PAPEL S.A. DE C.V',titulo="ENVIOS DE CALL CENTER",parametros=parametros)
    pdf.add_page()

    for envio in envios:

        pdf.set_font('helvetica', '', 10)
        pdf.cell(25, 5, str(envio.get('fecha_documento','').strftime("%d/%m/%Y")),align="C" )
        pdf.cell(35, 5, str(envio.get('create_user','')).upper(),align="L" )
        pdf.cell(25, 5, str(envio.get('documento','')),align="R" )
        pdf.cell(75, 5, envio.get('destinatario',''),align="L" )
        pdf.cell(25, 5, envio.get('sucursal',''),align="L" )
        if envio.get('recepcion','') is not None:
            pdf.cell(30, 5, str(envio.get('recepcion','').strftime("%d/%m/%Y %I:%M%p")),align="R" )
        else:
            pdf.cell(30, 5, "",align="L" )
        chofer = str(envio.get('chofer',''))[:20]
        pdf.cell(30, 5, chofer,align="L")
        pdf.cell(1, 5, "",align="L", new_x="LMARGIN", new_y="NEXT")
   




 
    reporte = bytes(pdf.output())
    return reporte


