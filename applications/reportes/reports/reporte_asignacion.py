from fpdf import FPDF
from .report_pdf import ReportPDF
from .report_dao import ReportDao
from .report_utils import get_grouped_data
from datetime import datetime
from decimal import Decimal






class ReporteAsignacionPDF(FPDF):
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
        self.cell(0, 5, self.empresa, align='R', new_x="LMARGIN", new_y="NEXT")
        # Parametros Izquierda
        self.set_font('helvetica', '', 9)
        # Titulo Reporte
        self.cell(0, 5,self.titulo,align='R' ,new_x="LMARGIN", new_y="NEXT")
        # Parametros
        if self.parametros:

            '''if(self.parametros.get('operador')):
                self.cell(27, 5,'OPERADOR: ', 0,0, 'L')
                self.cell(60, 5,self.parametros.get('operador'), 0,0, 'L')  
            '''
            x_params = 218
            if self.orientation == "P":
                 x_params= 157

            if(self.parametros.get('documento')):
                self.set_x(x_params)
                self.cell(30, 5,'EMBARQUE: ', 0,0, 'R')
                self.cell(20, 5,self.parametros.get('documento'), align='R',new_x="LMARGIN", new_y="NEXT")

            if(self.parametros.get('operador')):
                self.cell(27, 5,'OPERADOR: ', 0,0, 'L')
                self.cell(60, 5,self.parametros.get('operador'), align='L') 

            if(self.parametros.get('salida')):
                # Fecha
                self.set_x(x_params  )
                self.cell(20, 5,'SALIDA: ', align='R')
                self.cell(30, 5,self.parametros.get('salida'),align='R',new_x="LMARGIN", new_y="NEXT")       

        self.line(10,31,270,31)
        self.set_font('helvetica', '', 7)
        self.set_y(31) 
        #self.set_x(175)
        self.cell(165, 5, '', align='C',border=1)
        self.cell(95, 5, 'DESTINO', align='C',border=1, new_x="LMARGIN", new_y="NEXT")
        self.cell(10, 5, 'Pvs', align='C',border=1)
        self.cell(15, 5, 'TIPO', align='C',border=1)
        self.cell(25, 5, 'DOCUMENTO', align='C',border=1)
        self.cell(20, 5, 'FECHA', align='C',border=1)
        self.cell(60, 5, 'CLIENTE', align='C',border=1)
        self.cell(20, 5, 'IMPORTE', align='C',border=1)
        self.cell(15, 5, 'KILOS', align='C',border=1)
        self.cell(30, 5, 'LLEGADA', align='C',border=1)
        self.cell(30, 5, 'RECEPCION', align='C',border=1)
        self.cell(35, 5, 'COMENTARIO', align='C',border=1, new_x="LMARGIN", new_y="NEXT")

       
        

  
    # Page footer
    def footer(self):
        """Sobre escritura del metodo footer para personalizacion.
        """
        self.set_y(-15)
 
        self.set_font('helvetica', 'I', 6)
        size_footer = 64.5
        if self.orientation == "L":
             size_footer = 85  
   
        self.cell(size_footer, 10, 'SIIPAP', 'T', 0, 'C')
        self.cell(size_footer, 10, 'Pagina ' + str(self.page_no()) + ' de {nb}', 'T', 0, 'C')
        self.cell(size_footer, 10,'IMPRESO: ' + str(datetime.now().strftime("%d/%m/%Y %I:%M%p")), 'T', 0, 'C')


def reporte_asignacion_embarque(embarque):
    query = """ select 
                e.documento ,o.nombre as operador, e.or_fecha_hora_salida as salida,n.arribo, n.recepcion , n.recibio, e.regreso, n.tipo_documento ,n.documento as docto_envio ,n.destinatario,
                n.kilos, n.total_documento,n.comentario, s.nombre as sucursal,e.fecha, n.fecha_documento, i.fecha_de_entrega, i.tipo as tipo_envio,
                concat(i.direccion_calle,' ',ifnull(i.direccion_numero_exterior,''),' ',ifnull(i.direccion_numero_interior,''),', ',ifnull(i.direccion_colonia,''), ', ', ifnull(i.direccion_municipio,''),' ',ifnull(i.direccion_estado,'')) as direccion_entrega
                ,e.comentario as comentario_embarque
                from embarques e join entrega n  on ( e.id = n.embarque_id ) join instruccion_de_envio i on ( n.envio_id = i.envio_id ) 
                join operador o  on ( o.id = e.operador_id )  join sucursal s on ( e.sucursal_id = s.id )
                where e.id = %s 
            """
    dao = ReportDao()
    embarque = dao.get_data(query,[embarque])

    generales = embarque[0]

    campos = dao.get_fields(embarque[0])
    print("Campos")
    print(campos)

    parametros = {
        'salida' : generales['salida'].strftime("%d-%m-%Y %H:%M"), 
        'documento': str(generales['documento']),
        'operador': generales['operador'],
    }
  
    pdf = ReporteAsignacionPDF('L','mm','Letter','PAPEL S.A. DE C.V.',f"CONTROL DE EMBARQUES (ASIGNACIONES) {generales['sucursal']}",parametros= parametros )
    pdf.add_page()

    total_kilos = Decimal(0.00)
    total_importe = Decimal(0.00)

    for entrega in embarque:

        altura_disponible = pdf.h - pdf.get_y()
        print(altura_disponible)
        if altura_disponible < 30:
            print('Nueva pagina')
            pdf.add_page()
    
        pdf.cell(10, 5, 'No', align='C',border=0)
        pdf.cell(15, 5,entrega.get('tipo_documento'), align='C',border=0)
        pdf.cell(25, 5, entrega.get('docto_envio'), align='C',border=0)
        pdf.cell(20, 5, entrega.get('fecha_documento').strftime("%d-%m-%Y"), align='C',border=0)
        pdf.cell(60, 5, entrega.get('destinatario'), align='L',border=0)
        pdf.cell(20, 5, str( 0 if entrega.get('total') == None else entrega.get('total')), align='C',border=0)
        pdf.cell(15, 5, str(0 if entrega.get('kilos') == None else entrega.get('kilos') ), align='C',border=0)
        pdf.cell(30, 5, entrega.get('arribo').strftime("%d-%m-%Y %H:%M"), align='C',border=0)
        pdf.cell(30, 5, entrega.get('recepcion').strftime("%d-%m-%Y %H:%M"), align='C',border=0)
        pdf.cell(35, 5, 'COMENTARIO', align='C',border=0, new_x="LMARGIN", new_y="NEXT")

        pdf.cell(18, 5,'DIR_ENVIO: ', align='R',border=0)
        pdf.cell(150, 5, entrega.get('direccion_entrega'), align='L',border=0, new_x="LMARGIN", new_y="NEXT")
        
        pdf.cell(20, 5,'F_ENTREGA: ', align='R',border=0)
        pdf.cell(13, 5, entrega.get('fecha_de_entrega').strftime("%d-%m-%Y"), align='C',border=0)
        pdf.cell(10, 5,'Tipo: ', align='R',border=0)
        pdf.cell(15, 5, ("" if entrega.get('tipo_envio')== None else entrega.get('tipo_envio')) , align='C',border=0, new_x="LMARGIN", new_y="NEXT")
        pdf.line(10,pdf.get_y(),270,pdf.get_y())

        total_kilos += 0 if entrega.get('kilos') == None else entrega.get('kilos')
        total_importe += 0 if entrega.get('total') == None else entrega.get('total')

    pdf.cell(20, 5,'TOTAL: ', align='R',border=0)
    pdf.set_x(140)
    pdf.cell(20, 5, str(total_importe), align='C',border=0)
    pdf.cell(15, 5, str(total_kilos), align='C',border=0, new_x="LMARGIN", new_y="NEXT")

    pdf.cell(20, 5, "COMENTARIOS: ", align='C',border=0)
    pdf.cell(15, 5, ("" if entrega.get('comentario') == None else entrega.get('comentario')), align='C',border=0, new_x="LMARGIN", new_y="NEXT")


    reporte = bytes(pdf.output())
    return reporte
