from itertools import groupby


def get_grouped_data(lista,grupo ):
    """Funcion que recibe una lista de diccionarios y agrupa los datos por una propiedad en comun.
    Args: 
        lista :List lista de diccionarios.
        grupo: str Propiedad por la que se van a agrupar los datos.
    Returns:
        dict Diccionario que tiene como Key la propiedad por la que se agrupo y como Value una lista con los elementos que corresponden al key
    
    """
    data = sorted(lista, key=lambda x: x[grupo])  
    result = {}
    for key, group in groupby(data, key=lambda x: x[grupo]):
        result[key] = list(group)
    return result 