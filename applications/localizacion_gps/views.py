from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .serializers import UbicacionGPSSerializer

from .services import get_ubicacion_gps,get_ubicacion_transportes


@api_view(['GET'])
@permission_classes([AllowAny])
def get_ubicaciones_gps(request):
    sucursal = request.query_params.get('sucursal') 
    ubicaciones = get_ubicacion_transportes(sucursal)
    print(ubicaciones)
    serializer = UbicacionGPSSerializer(ubicaciones, many=True)
    return Response(serializer.data)