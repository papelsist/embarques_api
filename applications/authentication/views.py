from django.shortcuts import render
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import (RetrieveAPIView,ListAPIView)
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password
from .models import User
from applications.core.models import Sucursal
from .serializers import UserSerializer



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)

        data['username'] = self.user.username
        data['groups'] = self.user.groups.values_list('name', flat=True)
        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['GET'])
def get_user(request):
    
    authentication = JWTAuthentication()
    header = authentication.get_header(request)
    raw_token = authentication.get_raw_token(header) 
    validated_token = authentication.get_validated_token(raw_token)
    user = authentication.get_user(validated_token)
    user_serialized = UserSerializer(user)
    return Response(user_serialized.data)


class GetUser(APIView):
    serializer_class = UserSerializer

    def get(self, request):
      
        authentication = JWTAuthentication()
        header = authentication.get_header(self.request)
        raw_token = authentication.get_raw_token(header) 
        validated_token = authentication.get_validated_token(raw_token)
        user = authentication.get_user(validated_token)
        user_serialized = UserSerializer(user)
    
        return Response(user_serialized.data)
    
@api_view(['GET'])
@permission_classes([AllowAny])
def find_user_by_nip(request):
    nip = request.query_params.get('nip')
    user = User.objects.get(nip=nip)
    user_serialized = UserSerializer(user)
    return Response(user_serialized.data)


class UsersListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserRetrieveView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@api_view(['GET'])
@permission_classes([AllowAny])
def find_user_by_username(request):
    username = request.query_params.get('username')
    user = User.objects.get(username=username)
    user_serialized = UserSerializer(user)
    return Response(user_serialized.data)


@api_view(['POST'])
def create_user(request):

    print(request.data)
    sucursal = Sucursal.objects.get(pk = request.data['sucursal'])

    print(sucursal)
    print(request.data['sucursal'])

    user = User()
    user.username=request.data['username']
    user.nombre=request.data['nombre']
    user.nombres=request.data['nombres']
    user.sucursal=sucursal
    user.puesto=request.data['puesto']
    user.email=request.data['email']
    user.numero_de_empleado=request.data['numero_de_empleado']
    user.enabled=True
    user.is_active=True
    user.is_staff=False
    user.is_superuser=False
    password_encrypted = make_password(request.data['password'])
    user.password = password_encrypted

    user.save()
    user_serialized = UserSerializer(user)
    return Response(user_serialized.data)
  
@api_view(['PUT']) 
def update_user(request):
    user = User.objects.get(pk=request.data['id'])
    user.username=request.data['username']
    user.nombre=request.data['nombre']
    user.nombres=request.data['nombres']
    user.puesto=request.data['puesto']
    user.email=request.data['email']
    user.numero_de_empleado=request.data['numero_de_empleado']

    user.save()
    user_serialized = UserSerializer(user)
    return Response(user_serialized.data)

@api_view(['PUT'])
def update_password(request):
    user = User.objects.get(pk=request.data['id'])
    password_encrypted = make_password(request.data['password'])
    user.password = password_encrypted
    user.save()
    user_serialized = UserSerializer(user)
    return Response(user_serialized.data)
   


