import json
import requests
from .ruteo_dao import RuteoDao


def optimizacion_ruta_embarque(embarque_id):
    query = """ select 
                ifnull(CONCAT(direccion_calle," ",direccion_numero_exterior," ",direccion_colonia ," ",direccion_codigo_postal ," ",direccion_municipio ," ",direccion_estado," ", direccion_pais),"") as direccion,
                direccion_latitud, direccion_longitud
                from
                embarques e join entrega e2 on (e.id = e2.embarque_id)  join instruccion_de_envio ide on(ide.envio_id  = e2.envio_id)
                where e.id = %s
            """
    dao = RuteoDao()
    envios = dao.get_data(query,[embarque_id])
    coordenadas = ""
    for envio in envios:
        coordenadas = coordenadas+str(envio['direccion_longitud'])+","+str(envio['direccion_latitud'])+";"
    coordenadas = coordenadas[:-1]
    url = f"https://api.mapbox.com/optimized-trips/v1/mapbox/driving-traffic/-99.1068492,19.3598997;{coordenadas}?roundtrip=true&access_token=pk.eyJ1IjoibHF1aW50YW5pbGxhYiIsImEiOiJjbGxoNHQ2bTQwdzljM2ZxaG1lam4zd2h5In0.rWs48S5MkB8hdSnvBKWWqA"
    r = requests.get(url)
    respuesta = r.json()
    ruta_optimizada_json = json.dumps(respuesta,indent = 6)
    with open("ruta_optimizada.json","w") as ruta_optimizada:
        ruta_optimizada.write(ruta_optimizada_json)
    return respuesta

