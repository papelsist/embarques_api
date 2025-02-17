from django.db import connection





def get_data(query, params_query = None):
    """Funcion que ejecuta un query en la base de datos y regresa los resultados en una lista de diccionarios.

    Args:
        query (str, requerido): Query a ejecutar en la base de datos.  
        params_query (list , optional):  Defaults to None.

    Returns:
        list<dict>:  Lista de diccionarios con los resultados de la consulta.
    """
    data= []
    with connection.cursor() as cursor:
        if params_query :
            cursor.execute(query,params_query)
            table_rows= dictfetchall(cursor)
            data = table_rows
        else :
            cursor.execute(query)
            table_rows= dictfetchall(cursor)
            data = table_rows
    return data



def dictfetchall(cursor):
    """Retorna las filas obtenidas por el cursor como diccionario.

    Args:
        cursor cursor:  recibe el cursor de la base de datos para ejecutar el query.

    Returns:
        List: Regresa una lista de diccionarios
    """
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def get_fields(objeto):
    fields = []
    for field in objeto.keys():
        fields.append(field)
    return  fields

def fix_id_to_sql(id):
    """Funcion que elimina los guiones de un id para poder ser utilizado en un query sql.

    Args:
        id (str): id con formato de guiones.

    Returns:
        str: id sin guiones.
    """
    return id.replace("-", "")

def fix_id_to_uuid(id):
    """Funcion que agrega guiones a un id para poder ser utilizado en un query de la orm de django.

    Args:
        id (str): id sin guiones.

    Returns:
        str: id con guiones.
    """
    return id[:8] + '-' + id[8:12] + '-' + id[12:16] + '-' + id[16:20] + '-' + id[20:]