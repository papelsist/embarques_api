from fpdf import FPDF
from datetime import datetime
from applications.embarques.models import Entrega
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
        self.cell(10, 5,'TIPO',align="C")
        self.cell(20, 5, 'EMBARQUE',align="C" )
        self.cell(20, 5, 'DOCUMENTO',align="C" )
        self.cell(20, 5, 'F.DOCTO',align="C" )
        self.cell(70, 5, 'CLIENTE',align="C" )
        self.cell(10, 5, 'TOT FAC',align="C" )
        self.cell(20, 5, 'KILOS',align="C" )
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

    
def reporte_entrega_doctos(operador_id, sucursal_id, fecha):

  

    entregas = Entrega.objects.filter(embarque__regreso__date = fecha, embarque__operador__id=operador_id, embarque__sucursal__id = sucursal_id).order_by('fecha_documento','tipo_documento','documento')

    operador = entregas[0].embarque.operador
    sucursal = entregas[0].embarque.sucursal

    print(operador.nombre)
    print(sucursal.nombre)

    contado = []
    credito = []
    for entrega in entregas:
        if entrega.tipo_documento == "CRE":
            credito.append(entrega)
        else:
            contado.append(entrega)
    parametros = {
        'operador': operador.nombre,
        'sucursal': sucursal.nombre,
        'fecha': fecha
    }

    pdf = ReportPDF('P','mm','Letter','PAPEL S.A. DE C.V',f"CONTROL DE EMBARQUES (ENTREGA DE DOCTOS)  {sucursal.nombre}" ,parametros=parametros)
    pdf.add_page()


    
    paquetes_contado = 0
    kilos_contado = Decimal(0.00)
    importe_contado = Decimal(0.00)
    
    for entrega in contado:
        cantidad_envio = sum(det.me_cantidad for det in entrega.envio.detalles.all())
        cantidad_entrega = sum(det.cantidad for det in entrega.detalles.all())

        pdf.set_font('helvetica', '', 8)
        pdf.cell(10, 5, f"{entrega.tipo_documento}      {'#' if cantidad_envio != cantidad_entrega else ''}",align="C")
        pdf.cell(20, 5, str(entrega.embarque.documento),align="C" )
        pdf.cell(20, 5, entrega.documento,align="C" )
        pdf.cell(20, 5, entrega.fecha_documento.strftime("%d/%m/%Y"),align="C" )
        pdf.cell(70, 5, entrega.destinatario,align="L" )
        pdf.cell(10, 5, str(entrega.envio.total_documento),align="C" )
        pdf.cell(20, 5, str(entrega.kilos),align="C" )
        pdf.cell(20, 5, str(entrega.valor),align="C" )
        pdf.cell(5, 5, f"{'*' if entrega.envio.maniobra != 0  and  entrega.envio.maniobra != None else ''}",align="L", new_x="LMARGIN", new_y="NEXT")

        paquetes_contado += 0
        kilos_contado += entrega.kilos
        importe_contado += entrega.valor
    
    if kilos_contado > 0:
        pdf.set_font('helvetica', 'B', 8)
        pdf.set_x(150)
        pdf.cell(10, 5, "CONTADO: ",align="C")
        pdf.cell(20, 5, str(kilos_contado),align="C", border="T" )
        pdf.cell(30, 5, str(importe_contado),align="C", border="T", new_x="LMARGIN", new_y="NEXT")


    paquetes_credito = 0
    kilos_credito = Decimal(0.00)
    importe_credito = Decimal(0.00)

    pdf.ln()
    
    for entrega in credito:
        cantidad_envio = sum(det.me_cantidad for det in entrega.envio.detalles.all())
        cantidad_entrega = sum(det.cantidad for det in entrega.detalles.all())
        pdf.set_font('helvetica', '', 8)
        pdf.cell(10, 5, f"{entrega.tipo_documento}      {'#' if cantidad_envio != cantidad_entrega else ''}",align="C")
        pdf.cell(20, 5, str(entrega.embarque.documento),align="C" )
        pdf.cell(20, 5, entrega.documento,align="C" )
        pdf.cell(20, 5, entrega.fecha_documento.strftime("%d/%m/%Y"),align="C" )
        pdf.cell(70, 5, entrega.destinatario,align="L" )
        pdf.cell(10, 5, str(entrega.envio.total_documento),align="C" )
        pdf.cell(20, 5, str(entrega.kilos),align="C" )
        pdf.cell(20, 5, str(entrega.valor),align="C" )
        pdf.cell(5, 5, f"{'*' if entrega.envio.maniobra != 0  and  entrega.envio.maniobra != None else ''}",align="L", new_x="LMARGIN", new_y="NEXT")

        paquetes_credito += 0
        kilos_credito += entrega.kilos
        importe_credito += entrega.valor
    
   
    if kilos_credito > 0:
        pdf.set_font('helvetica', 'B', 8)
        pdf.set_x(150)
        pdf.cell(10, 5, "CREDITO : ",align="C")
        pdf.cell(20, 5, str(kilos_credito),align="C", border="T" )
        pdf.cell(30, 5, str(importe_credito),align="C", border="T" , new_x="LMARGIN", new_y="NEXT")

        pdf.ln()
        pdf.set_x(150)
        pdf.cell(10, 5, "TOTAL : ",align="C")
        pdf.cell(20, 5, str(kilos_credito + kilos_contado),align="C", border="T" )
        pdf.cell(30, 5, str(importe_credito + importe_contado),align="C",border="T", new_x="LMARGIN", new_y="NEXT")



    reporte = bytes(pdf.output())
    return reporte