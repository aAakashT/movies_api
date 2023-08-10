from rest_framework.response import Response 
from django.shortcuts import render
from rest_framework.views import APIView
from django.contrib.auth import authenticate 
from .serilaizers import RegisterSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from rest_framework import status
# Create your views here.

class RegisterUserView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        username = data.get('username')
        password = data.get('password')
        serializer =  RegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            user = User.objects.get(username=username)
            token = RefreshToken.for_user(user=user)
            access_token = str(token.access_token)
            data = {'access_token': access_token}    
            return Response(data=data, status=status.HTTP_201_CREATED)
        data = {'error': 'Username and password are required.'}
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)            

class SignInView(APIView):
    def post(self, request, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = User.objects.all()
        user = authenticate(username=username, password=password)
        
        if user is not None:
            Token = RefreshToken.for_user(user=user)
            if Token:
                access_token = str(Token.access_token)
            else:    
                Token = RefreshToken.for_user(user=user)
                access_token = str(Token.access_token)
            data = {"access_token": access_token}
            return Response(data=data, status=status.HTTP_200_OK)
        
        data= {"error": "provide correct username and password"}
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)