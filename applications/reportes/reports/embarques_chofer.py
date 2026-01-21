from fpdf import FPDF
from datetime import datetime
from applications.embarques.models import Embarque, Entrega, EntregaDet
from django.db.models import Prefetch
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

    
def reporte_embarques_chofer(operador_id, sucursal_id, fecha):

    detalles_prefetch = Prefetch(
        'detalles',
        queryset = EntregaDet.objects.all()
    )

    partidas_prefetch = Prefetch(
        'partidas',
        queryset = Entrega.objects.prefetch_related(detalles_prefetch).all()
    )

    embarques = Embarque.objects.select_related('operador').prefetch_related(partidas_prefetch).filter(
        operador__id=operador_id,
        regreso__date=fecha,
        sucursal__id=sucursal_id
    )
    operador = embarques[0].operador
    sucursal = embarques[0].sucursal

    parametros = {
        'operador': operador.nombre,
        'sucursal': sucursal.nombre,
        'fecha': fecha
    }

    pdf = ReportPDF('P','mm','Letter','PAPEL S.A. DE C.V',f"CONTROL DE EMBARQUES {sucursal.nombre}" ,parametros=parametros)
    pdf.add_page()

    for embarque in embarques:
        pdf.cell(15, 5, str(embarque.documento), align='C', border=0)
        dt = datetime.strptime(fecha, "%Y-%m-%d")
        fecha_embarque = dt.strftime("%d-%m-%Y")
        pdf.cell(20, 5, fecha_embarque , align='C',border=0)
        fecha_salida = embarque.or_fecha_hora_salida.strftime("%d-%m-%Y %H:%M")
        pdf.cell(25, 5, fecha_salida , align='C',border=0)
        fecha_regreso = embarque.regreso.strftime("%d-%m-%Y %H:%M")
        pdf.cell(25, 5, fecha_regreso , align='C',border=0)
        pdf.cell(15, 5, "" , align='C',border=0, new_x="LMARGIN", new_y="NEXT")
        partidas = embarque.partidas.all()
        for partida in partidas:
            pdf.cell(25, 5, partida.documento , align='C',border=0)
            pdf.cell(25, 5, partida.tipo_documento , align='C',border=0)
            fecha_docto = partida.fecha_documento.strftime("%d-%m-%Y")
            pdf.cell(20, 5, fecha_docto , align='C',border=0)
            pdf.cell(25, 5, partida.destinatario , align='C',border=0)
            arribo = partida.arribo.strftime("%d-%m-%Y %H:%M")
            pdf.cell(25, 5, arribo , align='C',border=0)
            recepcion = partida.recepcion.strftime("%d-%m-%Y %H:%M")
            pdf.cell(25, 5, recepcion , align='C',border=0)
            pdf.cell(15, 5, (partida.recibio if partida.recibio else "") , align='C',border=0)
            pdf.cell(15, 5, str(partida.valor) , align='C',border=0)
            pdf.cell(15, 5, str(partida.kilos) , align='C',border=0)
            pdf.cell(15, 5, "" , align='C',border=0, new_x="LMARGIN", new_y="NEXT")
            detalles = partida.detalles.all()
            for detalle in detalles:
                pdf.cell(15, 5, detalle.clave , align='C',border=0)
                pdf.cell(80, 5, detalle.descripcion , align='C',border=0)
                pdf.cell(15, 5, str(detalle.cantidad) , align='C',border=0)
                pdf.cell(15, 5, str(detalle.valor), align='C',border=0)
                pdf.cell(15, 5, str(detalle.kilos), align='C',border=0)
               
                pdf.cell(15, 5, "" , align='C',border=0, new_x="LMARGIN", new_y="NEXT")




    reporte = bytes(pdf.output())
    return reporte