from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.views import APIView

from .serializers import (
    UserLoginValidateSerializer, UserCreateSerializer)


class RegistrationAPIView(APIView):
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        User.objects.create_user(**serializer.validated_data)
        return Response(status=status.HTTP_201_CREATED,
                        data={'message': 'User created'})
# @api_view(['POST'])
# def registration(request):
#     # username = request.data.get('username')
#     # password = request.data.get('password')
#     serializer = UserCreateSerializer(data=request.data)
#     serializer.is_valid(raise_exception=True)
#     User.objects.create_user(**serializer.validated_data)
#     return Response(status=status.HTTP_201_CREATED,
#                     data={'message': 'User created'}
#                     )


class LoginAPIView(APIView):
    def post(self, request):
        serializer = UserLoginValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(**serializer.validated_data)
        if user:
            Token.objects.filter(user=user).delete()
            token = Token.objects.create(user=user)
            return Response(data={
                'key': token.key
            })
        return Response(data={'message': 'Invalid login/password'},
                        status=status.HTTP_401_UNAUTHORIZED)

# @api_view(['POST'])
# def login(request):
#     # username = request.data.get('username')
#     # password = request.data.get('password')
#     serializer = UserLoginValidateSerializer(data=request.data)
#     # user = authenticate(username=username, password=password)
#     serializer.is_valid(raise_exception=True)
#     user = authenticate(**serializer.validated_data)
#     if user:
#         Token.objects.filter(user=user).delete()
#         token = Token.objects.create(user=user)
#         return Response(data={
#             'key': token.key
#         })
#
#     return Response(data={'message': 'Invalid login/password'},
#                     status=status.HTTP_401_UNAUTHORIZED)
