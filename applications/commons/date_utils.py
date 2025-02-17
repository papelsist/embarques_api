from datetime import datetime,date
import calendar

class DateUtils():

    CFDI_DATE_FORMAT= "%Y-%m-%dT%H:%M:%S"

    meses ={
        'January':{'nombre': 'Enero', 'clave': 0},
        'February':{'nombre': 'Febrero', 'clave': 1},
        'March':{'nombre': 'Marzo', 'clave': 3},
        'April':{'nombre': 'Abril', 'clave': 4},
        'May':{'nombre': 'Mayo', 'clave': 5},
        'June':{'nombre': 'Junio', 'clave': 6},
        'July':{'nombre': 'Julio', 'clave': 7},
        'August':{'nombre': 'Agosto', 'clave': 8},
        'September':{'nombre': 'Septiembre', 'clave': 9},
        'October':{'nombre': 'Octubre', 'clave': 10},
        'November':{'nombre': 'Noviembre', 'clave': 11},
        'December':{'nombre': 'Diciembre', 'clave': 12}
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
    def get_name_month(cls,month_number):
        month = calendar.month_name[month_number]
        month_name = cls.meses[month]['nombre']
        return month_name

    
    @classmethod
    def periodoMonthLabel(cls,fechaInicial, fechaFinal):   
        pass
    
    @classmethod
    def getCurrentMonthYear(cls):
        return f"{cls.meses[date.today().strftime('%B')]['nombre']} - {date.today().strftime('%Y')}"
    
    @classmethod
    def get_current_month_year(cls):
        year = date.today().year
        month = date.today().month
        return month, year


    @staticmethod
    def get_month_year(fecha_str):
        fecha = datetime.strptime(fecha_str, "%Y-%m-%d")
        year = fecha.year
        month = fecha.month

        return  month, year
    
    @staticmethod
    def get_day_ini_month(month, year):
        return datetime(year, month, 1)
    
    @staticmethod
    def get_day_ini_year(year):
        return datetime(year, 1, 1)
    
    @staticmethod
    def get_day_end_month(month, year):
        last_day = calendar.monthrange(year, month)[1]
        return datetime(year, month, last_day)

    @staticmethod
    def get_current_week():
        return datetime.now().isocalendar()[1]
    
    @staticmethod
    def get_current_day_of_week():
        return datetime.now().isocalendar()[2]

    @staticmethod
    def get_worked_days(days_of_week = 7):
        current_week = datetime.now().isocalendar()[1]
        current_day_of_week = datetime.now().isocalendar()[2]
        return (current_week -1) * days_of_week + current_day_of_week

    


    
    




    
   