from geopy import distance
import pandas as pd
import datetime
import numpy as np
import json 
from .ruteo_dao import RuteoDao
from applications.embarques.models import Embarque,Envio,Sucursal
from applications.commons.sql_dao import fix_id_to_sql



def obtener_diferencias(lista_a, lista_b):
    diferencias = [i for i in lista_a if i not in lista_b]
    return diferencias

def asignar_sector(centro, coord):
    """

    """
    coord_lat = coord[0]
    coord_lon = coord[1]
    cent_lat = centro[0]
    cent_lon = centro[1]
    if coord_lat > cent_lat  and coord_lon >  cent_lon :
        return 1
    if coord_lat > cent_lat  and coord_lon <  cent_lon :
        return 2
    if coord_lat < cent_lat  and coord_lon <  cent_lon :
        return 3
    if coord_lat < cent_lat  and coord_lon >  cent_lon :
        return 4

def calcular_tiempo_desde(tiempo):
    ahora = datetime.datetime.now()
    tiempo_transcurrido = ahora - tiempo
    return tiempo_transcurrido

def calcular_distancias(row, columna, df_coord):
    indice = row.name  # Obtener el índice del DataFrame
    valor_objetivo = row[columna]  # Obtener el valor objetivo en la fil
    diferencias = df_coord.apply(lambda row: (distance.distance(valor_objetivo, row['coord']).km), axis=1)
    df_coord[indice] = diferencias
    return df_coord

def set_cero(row, df_coord):
    indice = row.name  # Obtener el índice del DataFrame
    df_coord.loc[:indice,indice] = 0
    return df_coord

def calcular_costo(row,columna, df_coord):
    indice = row.name  # Obtener el índice del DataFrame
    punto = row[columna]  # Obtener el valor objetivo en la fil
    df_coord[indice] = (df_coord["distancia_km"]+ punto)-row
    return df_coord

def get_envios_fecha(sucursal,fecha):
    query = """
             select 
    e.id as envio_id,i.direccion_latitud , i.direccion_longitud,
    ifnull(CONCAT(direccion_calle," ",direccion_numero_exterior," ",direccion_colonia ," ",direccion_codigo_postal ," ",direccion_municipio ," ",direccion_estado," ", direccion_pais),"") as direccion,
    e.destinatario,e.date_created,e.kilos, i.id as instruccion_id,e.kilos
    from envio e join instruccion_de_envio i on (e.id = i.envio_id) left join entrega n on (e.id = n.envio_id)
    where i.direccion_latitud  <> 0 and n.id is null and e.sucursal = %s and date(i.fecha_de_entrega)  = %s 
    """
    dao = RuteoDao()
    envios = dao.get_data(query,[sucursal,fecha])
    return envios

def get_envios(envios):
    params = ""
    for env in envios:
        params += "%s , " 

    params = params[:-2]
    like1 = 'CDMX'
    like2 = 'CIUDAD DE MEXICO'
    like3 = 'ESTADO DE MÉXICO'
    like4 = 'EDO. DE MEX.'
    likes = [like1, like2, like3, like4]
    parametros = envios  
    print(parametros)
    query = f"""
    select 
    e.id as envio_id,i.direccion_latitud , i.direccion_longitud,
    ifnull(CONCAT(direccion_calle," ",direccion_numero_exterior," ",direccion_colonia ," ",direccion_codigo_postal ," ",direccion_municipio ," ",direccion_estado," ", direccion_pais),"") as direccion,
    destinatario,e.date_created,kilos, i.id as instruccion_id,kilos
    from envio e join instruccion_de_envio i on (e.id = i.envio_id) 
    where   i.direccion_latitud  <> 0 and e.id in ({params})  
    """ 
    print(query)
    dao = RuteoDao()
    envios = dao.get_data(query,parametros)
    print(envios)
    return envios
    


def make_df(data, suc_point):
    df = pd.DataFrame(data) 
    df['coord'] = df.apply(lambda row: (row['direccion_latitud'], row['direccion_longitud']), axis=1)
    df['distancia_km'] = df.apply(lambda row: (distance.distance(suc_point, row['coord']).km), axis=1)
    df['sector'] = df.apply(lambda row: (asignar_sector(suc_point,row['coord'])), axis=1)
    df['tiempo_desde'] = df.apply(lambda row: (calcular_tiempo_desde(row['date_created'])), axis=1)
   
    return df


def drop_outliers(df):
    # Obteniendo valores atipicos por la regla de cuartiles
    Q1 = df['distancia_km'].quantile(0.25)
    Q3 = df['distancia_km'].quantile(0.75)
    IQR = Q3 - Q1
    threshold = 1.5
    outliers = df[(df['distancia_km'] < Q1 - threshold * IQR) | (df['distancia_km'] > Q3 + threshold * IQR)]

    ''' print("*"*50)
    print(outliers['envio_id'])
    print("*"*50) '''

    indices = list(outliers['envio_id'])
    # Quitando valores atipicos para eliminar ruido en el ruteo
    df_sin_outliers = df.drop(list(outliers.index))  
    return df_sin_outliers, indices


def make_df_work(df):
    # Creamos dataframe de trabajo para calcular distancias y costos
    df_coord = df[['envio_id','coord','distancia_km']]
    df_coord = df_coord.set_index('envio_id')

    return df_coord, list(df_coord.index)

def get_matriz_distancias(df_coord):
    # Obteniendo la matriz de distancias
    df_coord.apply(lambda row: calcular_distancias(row, 'coord',df_coord), axis=1)

    return df_coord

def get_matriz_costos(df_coord):
    # Obteniendo la matriz de costos
    df_coord.apply(lambda row: calcular_costo(row,'distancia_km',df_coord), axis=1)

    return df_coord

def set_cero_matriz_costos(df_coord):
    # Pasando a cero los valores duplicados en la diagonal 
    df_coord.apply(lambda row: set_cero(row, df_coord), axis=1)
  
    return df_coord

def order_costos(df_coord):
    df_values_order = df_coord.iloc[:,2:]
    # obteniendo solo los valores de la matriz de costos para ordenar de manera descendente, se covierten a una lista
    listas = list(df_values_order.values)
    # eliminando los ceros de la lista de valores de la matriz de costos
    valores = []
    for lista in listas:
        sin_ceros = list(filter(lambda it :  it>0, lista))
        valores += sin_ceros
    # ordenando los valores  de manera descendente
    valores.sort(reverse=True)
    return valores

def get_intersection(valores,df_coord):
    # Obteniendo la interseccion de la matriz de costos lo que correspondera para comenzar el ruteo
    puntos =[]
    for index,val in enumerate(valores):
        ubicaciones = df_coord.where(df_coord == val).stack().index.tolist()

        for ubicacion in ubicaciones:
            if ubicacion not in puntos:
                puntos.append(ubicacion)

    return puntos

def get_transportes(suc_id):
    print("Sucursal")
    print(suc_id)
    sucursal_id = fix_id_to_sql(str(suc_id))
    query = """
            select e.id as embarque_id,e.documento as embarque_documento,te.* 
            from embarques e join operador o  on (e.operador_id  = o.id) join transporte_embarques te  on (o.transporte_id  = te.id) left join entrega n on (e.id = n.embarque_id)
            where or_fecha_hora_salida is NULL and n.id is null and sucursal_id =%s order by e.date_created"""
    dao = RuteoDao()
    transportes = dao.get_data(query,[sucursal_id])

    return transportes

def make_rutas(transportes):
    rutas = [] 

    for transporte in transportes:
        ruta = {
            "embarque_documento": transporte['embarque_documento'],
            "embarque_id": transporte['embarque_id'],
            "transporte_id": transporte['id'],
            "descripcion": transporte['descripcion'],
            "transporte_capacidad":float(transporte['capacidad_max_kilos']),
            "destinos": [],
            "ocupado": 0
        }
        rutas.append(ruta)

    return rutas

def get_capacidad_total(rutas):
    capacidad_total = 0.0

    # obtener capacidad total de los transportes
    for transporte in rutas:
        capacidad_total += transporte['transporte_capacidad']


    return capacidad_total

def get_demanda(puntos, df_sin_outliers, capacidad_total):
    # identificar los asignables por la capacidad del transporte vs demanda envio 
    # TODO - Evaluar si es factible ocupar esta lista para el ruteo u ocupar otro metodo
    asignables = []
    kilos_total = 0
    for punto in puntos:
        for envio in punto:
            kilos = df_sin_outliers[df_sin_outliers['envio_id'] == envio]['kilos'].values
           
            if envio not in asignables:
                if kilos_total <= capacidad_total:
                    kilos_total += kilos
                    asignables.append(envio)
    return kilos_total

def build_rutas(puntos,asignables, rutas, df_sin_outliers ):
    # Estructurando las rutas 
    asignados = []
    for punto in puntos:
        val1 = punto[0]
        val2 = punto[1]
        kilos_val1 = df_sin_outliers[df_sin_outliers['envio_id'] == val1]['kilos'].values[0]
        kilos_val2 = df_sin_outliers[df_sin_outliers['envio_id'] == val2]['kilos'].values[0]
        val1_asignado = val1 in  asignados
        val2_asignado = val2 in  asignados
    
        if(not val1_asignado and not val2_asignado):
            for ruta in rutas:
                
                if len(ruta['destinos']) == 0:
                    
                    kilos_valid = kilos_val1 + kilos_val2

                    if kilos_valid > ruta['transporte_capacidad']:

                        #print(ruta['transporte_capacidad'])
                        #print(kilos_valid)
                        #print(punto)

                        if kilos_val1 < ruta['transporte_capacidad'] and kilos_val1 > kilos_val2:

                            ruta['destinos'].append(val1)
                            ruta['ocupado'] +=  kilos_val1 
                            asignados.append(val1)

                        else:
             
                            ruta['destinos'].append(val2)
                            ruta['ocupado'] +=  kilos_val2
                            asignados.append(val2)
                            
                    else: 
        
                        ruta['destinos'].append(val1)
                        ruta['ocupado'] +=  kilos_val1 
                        asignados.append(val1)
            
                        ruta['destinos'].append(val2)
                        ruta['ocupado'] +=  kilos_val2
                        asignados.append(val2)
                    
                    break
        
        if( not val1_asignado and val2_asignado):
     
            for ruta in rutas:
                
                if len(ruta['destinos'])< 11:
                
                    if val2 in ruta['destinos']:
                        kilos_valid = ruta['ocupado'] + kilos_val1
                        if kilos_valid < ruta['transporte_capacidad']:
                            ruta['destinos'].append(val1)
                            ruta['ocupado'] +=  kilos_val1
                            asignados.append(val1)
                            break

        if( val1_asignado and not val2_asignado):
    
            for ruta in rutas:
                if len(ruta['destinos'])< 11:
                    if val1 in ruta['destinos']:
                        kilos_valid = ruta['ocupado'] + kilos_val2
                        if kilos_valid < ruta['transporte_capacidad']:
                            ruta['destinos'].append(val2)
                            ruta['ocupado'] +=  kilos_val2
                            asignados.append(val2)
                            break

    no_asignados = obtener_diferencias(asignables,asignados)
    return rutas, no_asignados

def add_coords_rutas(rutas,df):
    for ruta in rutas:
   
        destinos_coords= []
        for destino in ruta['destinos']:
            coords_latitud = df[df['envio_id'] == destino]['direccion_latitud'].values
            coords_longitud = df[df['envio_id'] == destino]['direccion_longitud'].values
            destino_coords = {  
                                "destino": destino,
                                "latitud": float(coords_latitud),
                                "longitud":float(coords_longitud)
                             }
            
            destinos_coords.append(destino_coords)
         
        ruta['destinos_coords'] = destinos_coords
        ruta['ocupado'] = float(ruta['ocupado'])
    return rutas

def make_rutas_json(rutas):
    rutas_json = json.dumps(rutas,indent = 6)

    with open("./rutas.json","w") as file_json :
            file_json.write(rutas_json) 
    return rutas_json



def build_ruteo_by_pendientes(fecha,sucursal_nombre):
    
    sucursal = Sucursal.objects.get(nombre = sucursal_nombre)
    #sucursal =  {"nombre": "CALLE 4", "latitud":19.3598997, "longitud":-99.1068492, "tipo": "EMPRESA"}
    suc_point = (sucursal.direccion_latitud,sucursal.direccion_longitud)

    envios = get_envios_fecha(sucursal.nombre,fecha)
    if len(envios) > 0:
        rutas = build_ruteo(envios, suc_point, sucursal.id)
        return rutas
    else:
        return {}


def build_ruteo_by_envios(ids, sucursal_nombre):
    
    sucursal = Sucursal.objects.get(nombre = sucursal_nombre)
    # sucursal =  {"nombre": "CALLE 4", "latitud":19.3598997, "longitud":-99.1068492, "tipo": "EMPRESA"}
    # suc_point = (sucursal['latitud'],sucursal['longitud'])
    suc_point = (sucursal.direccion_latitud,sucursal.direccion_longitud)
    envios = get_envios(ids)
    # print("*"*50)
    # print(envios)
    if len(envios) > 0:
        rutas = build_ruteo(envios, suc_point, sucursal.id)
        return rutas
    else:
        return {}

def build_ruteo(envios, suc_point, suc_id):
   
    
    df = make_df(envios, suc_point)
    #print(df)
    df_sin_outliers, outliers = drop_outliers(df)
    #print(outliers)
    df_coord, asignables = make_df_work(df_sin_outliers)
    #print(df_coord)
    df_distancias = get_matriz_distancias(df_coord)
    #print(df_distancias)
    df_costos = get_matriz_costos(df_distancias)
    #print(df_costos)
    df_costos_work = set_cero_matriz_costos(df_costos)
    #print(df_costos_work)
    valores = order_costos(df_costos_work)
    print("*"*50)
    #print(valores)
    puntos = get_intersection(valores, df_costos_work )
    print("*"*50)
    #print(puntos)
    transportes = get_transportes(suc_id)
    print("Transportes")
    print(transportes)
    rutas = make_rutas(transportes)
    print("Rutas")
    print(rutas)
    capacidad_total = get_capacidad_total(rutas)
    demanda = get_demanda(puntos, df_sin_outliers, capacidad_total)
    rutas, no_asignados = build_rutas(puntos, asignables, rutas, df_sin_outliers)

    # TODO - Preguntar si hay no asignados y se tienen camiones vacios 
    # validar si el envio es mayor a la mitad de la capacidad del transporte asignarla sola y enviar?. 
    if len(no_asignados) > 0 :
        for no_asignado in no_asignados:
            rutas_vacias = [r for r in rutas if len(r['destinos']) <= 0 ]
            for ruta_vacia in rutas_vacias:
                kilos = df_sin_outliers[df_sin_outliers['envio_id'] == no_asignado]['kilos'].values
                kilos = float(kilos)
                #print(f"Kilos enviar : {kilos}")
                #print(f"Capacidad Transporte: {ruta_vacia['transporte_capacidad']}")
                if kilos  >= ruta_vacia['transporte_capacidad'] /2 and kilos  <= ruta_vacia['transporte_capacidad']:
                    #print("Si se puede asignar")
                    ruta_vacia['destinos'].append(no_asignado)
                    ruta_vacia['ocupado'] = kilos
                    no_asignados.remove(no_asignado) 

    rutas = add_coords_rutas(rutas,df)
    rutas_json = make_rutas_json(rutas)

    ruteo = {
        "no_asignados": no_asignados,
        "outliers": outliers,
        "rutas": rutas
    }

    return ruteo


def ruteo_dj_orm(rutas):

    if not rutas:
        return {}

    rutas_orm = {
        "no_asignados" :[],
        "outliers":[],
        "rutas":[],
    }

    for no_asignado in rutas["no_asignados"]:
        envio = Envio.objects.get(pk= no_asignado)
        rutas_orm['no_asignados'].append(envio)

    for outlier in rutas["outliers"]: 
        envio = Envio.objects.get(pk= outlier)
        rutas_orm['outliers'].append(envio)


    for ruta in rutas['rutas']:
        embarque = Embarque.objects.get(pk = ruta["embarque_id"])
        ruta_orm= {
            "embarque": None,
            "destinos": [],
            "ocupado": 0.00,
            "transporte_capacidad": 0.00
        }
        ruta_orm['embarque'] = embarque
        ruta_orm['ocupado'] = ruta["ocupado"]
        #ruta_orm['transporte_capacidad'] = ruta["transporte_capacidad"]
        for destino in ruta["destinos"]:
            envio = Envio.objects.get(pk= destino)
            ruta_orm['destinos'].append(envio)
        rutas_orm['rutas'].append(ruta_orm)
    return rutas_orm

            


