from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import CodigosPostalesMX
from .serializers import CodigosPostalesSerializer

# Create your views here.
@api_view(['GET'])
@permission_classes([AllowAny])
def get_address_from_zipcode(request):
    """
    Get address from zipcode
    """
    print(request.query_params)
    addresess = CodigosPostalesMX.objects.filter(codigo=request.query_params.get('zip'))
    print(addresess)

    addresess_serialized = CodigosPostalesSerializer(addresess, many=True)

    return Response(addresess_serialized.data)
