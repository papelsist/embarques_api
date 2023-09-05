from datetime import datetime,date

class DateUtils():

    CFDI_DATE_FORMAT= "%Y-%m-%dT%H:%M:%S"

    meses ={
        'January':{'nombre': 'Enero', 'clave': 0},
        'February':{'nombre': 'Febrero', 'clave': 1},
        'March':{'nombre': 'Marzo', 'clave': 3},
        'April':{'nombre': 'Abril', 'clave': 4},
    }

    @classmethod
    def get_time_lapse_now(cls,fecha): 
        duration = datetime.now() - fecha
        dias = duration.days
        horas = int(duration.seconds / 60 /60)
        minutos = int(((duration.seconds / 60 /60) - horas) * 60)
        dias_txt= ""
        horas_txt = ""
        minutos_txt=""
        if dias == 1: 
            dias_txt = f"{dias} dia"
        if dias >1:
            dias_txt = f"{dias} dias"
        if horas == 1: 
            horas_txt = f"{horas} hora"
        if horas >1:
            horas_txt = f"{horas} horas"
        if minutos == 1: 
            minutos_txt = f"{minutos} minuto"
        if minutos >1 :
            minutos_txt = f"{minutos} minutos"
        res_txt =f"{dias_txt} {horas_txt} {minutos_txt} "
        return res_txt

    @classmethod
    def getNowFormatted(cls):
        now = datetime.now()
        return now.strftime(cls.CFDI_DATE_FORMAT)
    
    @classmethod
    def cfdiDate(cls,fecha):
        return fecha.strftime(cls.CFDI_DATE_FORMAT)

    @staticmethod 
    def cfdiDateToDate(cfdiDate):
        return datetime.fromisoformat(cfdiDate)

    @classmethod
    def toDate(cls, fecha):
        return date.fromisoformat(fecha)
       
    @classmethod
    def periodoDays(cls,fechaInicial, fechaFinal):
        d1 = datetime.strptime(str(fechaInicial), "%Y-%m-%d")
        d2 = datetime.strptime(str(fechaFinal), "%Y-%m-%d")
        return abs((d2 - d1).days)

    @classmethod
    def getMonth(cls,fecha):
        return f"{cls.meses[fecha.strftime('%B')]['nombre']}"

    @classmethod
    def getCurrentMonth(cls):
        return f"{cls.meses[date.today().strftime('%B')]['nombre']}"
       
    @classmethod
    def getCurrentMonthYear(cls):
        return f"{cls.meses[date.today().strftime('%B')]['nombre']} - {date.today().strftime('%Y')}"

    @classmethod
    def periodoMonthLabel(cls,fechaInicial, fechaFinal):   
	    return f"{cls.meses[fechaInicial.strftime('%B')]['nombre']} - {cls.meses[fechaFinal.strftime('%B')]['nombre']}"



    




    
   