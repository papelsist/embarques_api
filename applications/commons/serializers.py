from rest_framework.serializers import ModelSerializer

from  applications.core.models import Producto
from  applications.inventario.serializers import ProductoMarcaFormSerializer


class ProductoMarcasSerializer(ModelSerializer):
    marcas = ProductoMarcaFormSerializer(many=True)
    class Meta:
        model = Producto
        fields = '__all__'