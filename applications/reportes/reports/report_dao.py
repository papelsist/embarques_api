from django.db import connection
from itertools import groupby


class ReportDao:

    def get_data(self, query= None, params_query = None):
        """Funcion para obtener los datos en un diccionario a partir del query recibido en el init.
            Returns: list<dict>
        """
        data= []
        with connection.cursor() as cursor:
            if params_query :
                cursor.execute(query,params_query)
                table_rows= self._dictfetchall(cursor)
                data = table_rows
            else :
                cursor.execute(query)
                table_rows= self._dictfetchall(cursor)
                data = table_rows
        return data

    def _dictfetchall(self,cursor):
        """Retorna las filas obtenidas por el cursor como diccionario.

        Args:
            cursor cursor:  recibe el cursor de la base de datos para ejecutar el query.

        Returns:
            List: Regreasa una lista de diccionarios
        """
        columns = [col[0] for col in cursor.description]
        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]
            
       

