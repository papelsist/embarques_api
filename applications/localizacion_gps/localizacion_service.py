from applications.embarques.models import TransporteEmbarques,Embarque, Operador
from .models import Tokens
from django.db.models import Q
import requests



def get_entregas():

    en_transito = Embarque.objects.filter( ~Q(or_fecha_hora_salida = None),regreso = None ).order_by('documento')
    entregas_transito = []
    for embarque in en_transito:
        imei = embarque.operador.transporte.imei if embarque.operador.transporte.imei is not None else ""
        entrega = {
            "imei":imei,
            "operador": embarque.operador.nombre,
            "transporte": embarque.operador.transporte,
            "embarque":embarque,
            "ubicacion": None
        }
        
        entregas_transito.append(entrega)   
        entregas_transito   

        imeis = [entrega['imei'] for entrega in entregas_transito]
        transportes = TransporteEmbarques.objects.filter(~Q(imei = None))
        sin_asignacion  = []
        for transporte in transportes:
            if transporte.imei not in imeis:
                operador = Operador.objects.get(transporte = transporte)
                entrega = {
                    "imei":  transporte.imei,
                    "operador": operador.nombre,
                    "transporte":  transporte,
                    "embarque":None,
                    "ubicacion":None
                    }
                sin_asignacion.append(entrega)
        
        imeis_sa = [entrega['imei'] for entrega in sin_asignacion]
        imeis = imeis + imeis_sa
        imeis_str = ",".join(imeis)

        token = Tokens.objects.get(servicio = 'gps')

        url =f"http://api.protrack365.com/api/track?access_token={token}&imeis={imeis_str}"

        response = requests.get(url)

        ubicaciones = entregas_transito + sin_asignacion

        for ubicacion in response.json()['record']:
            for ubi in ubicaciones:
                if ubi['imei'] == ubicacion['imei']:
                    ubi['ubicacion'] = ubicacion
	
        for ubicacion in ubicaciones:
            print(ubicacion)

      

