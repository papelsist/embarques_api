from applications.embarques.models import TransporteEmbarques,Embarque, Operador
from applications.core.models import Empresa, Sucursal
from .models import Tokens
from django.db.models import Q
import hashlib
import time
from datetime import datetime
import requests




def calculate_signature(salt):
    md5_text = hashlib.md5("Chino2025@gps".encode('utf-8')).hexdigest()
    concatenated = md5_text + salt
    signature = hashlib.md5(concatenated.encode('utf-8')).hexdigest()
    return signature

def get_timestamp():
    current_timestamp = int(time.time())
    return current_timestamp

def get_token_gps():
    current_timestamp = str(get_timestamp())
    signature = calculate_signature(current_timestamp)
    url = f"http://api.protrack365.com/api/authorization?time={current_timestamp}&account=gpspapelsa&signature={signature}"
    response = requests.get(url)
    token = response.json()['record']['access_token']
    found = Tokens.objects.get(servicio = 'gps')
    if found:
        found.token = token
        found.save()
    else:
        Tokens.objects.create(servicio = 'gps', token = token)


def get_transporte_gps():
    transportes = TransporteEmbarques.objects.filter(~Q(imei = None))
    return transportes

def get_ubicacion_gps():
    transportes = get_transporte_gps()
    imeis = [transporte.imei for transporte in transportes]
    imeis_str = ",".join(imeis)
    token = Tokens.objects.get(servicio = 'gps')
    url =f"http://api.protrack365.com/api/track?access_token={token.token}&imeis={imeis_str}"
    print(url)
    response = requests.get(url)
    print(response.json())
    if response.json()['code'] == 10012:
        print('Token expirado')
        get_token_gps()
        token = Tokens.objects.get(servicio = 'gps')
        url =f"http://api.protrack365.com/api/track?access_token={token}&imeis={imeis_str}"
        response = requests.get(url)
    
    return response.json()


def get_ubicacion_transportes(suc):

    sucursal = Sucursal.objects.get(nombre = suc)
    
    en_transito = Embarque.objects.filter( ~Q(or_fecha_hora_salida = None),regreso = None, sucursal= sucursal ).order_by('documento')
    entregas_transito = []
    for embarque in en_transito:
        imei = embarque.operador.transporte.imei if embarque.operador.transporte.imei is not None else ""
        entrega = {
            "imei":imei,
            "operador": embarque.operador.nombre,
            "transporte": embarque.operador.transporte,
            "embarque":embarque,
            "latitud": None,
            "longitud": None,
            "speed": None,
            "course": None
        }
        
        entregas_transito.append(entrega)   
   

    imeis = [entrega['imei'] for entrega in entregas_transito]
    transportes = TransporteEmbarques.objects.filter(~Q(imei = None), sucursal = suc)
    sin_asignacion  = []
    for transporte in transportes:
        if transporte.imei not in imeis:
            operador = Operador.objects.get(transporte = transporte)
            entrega = {
                "imei":  transporte.imei,
                "operador": operador.nombre,
                "transporte":  transporte,
                "embarque":None,
                "latitud": None,
                "longitud": None,
                "speed": None,
                "course": None
                }
            sin_asignacion.append(entrega)
    
    imeis_sa = [entrega['imei'] for entrega in sin_asignacion]
    imeis = imeis + imeis_sa
    imeis_str = ",".join(imeis)

    token = Tokens.objects.get(servicio = 'gps')

    url =f"http://api.protrack365.com/api/track?access_token={token.token}&imeis={imeis_str}"

    response = requests.get(url)

    if response.json()['code'] == 10012:
        print('Token expirado')
        get_token_gps()
        token = Tokens.objects.get(servicio = 'gps')
        url =f"http://api.protrack365.com/api/track?access_token={token.token}&imeis={imeis_str}"
        response = requests.get(url)

    ubicaciones = entregas_transito + sin_asignacion

    for ubicacion in response.json()['record']:
        for ubi in ubicaciones:
            if ubi['imei'] == ubicacion['imei']:
                ubi['latitud'] = ubicacion['latitude']
                ubi['longitud'] = ubicacion['longitude']
                ubi['speed'] = ubicacion['speed']
                ubi['course'] = ubicacion['course']
    
    return ubicaciones
