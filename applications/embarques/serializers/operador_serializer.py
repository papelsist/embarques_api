from rest_framework import serializers
from datetime import datetime
from ..models import Operador


class OperadorSerializer(serializers.ModelSerializer):

    class Meta: 
        model = Operador
        fields = '__all__'

 