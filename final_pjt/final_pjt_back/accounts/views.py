from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserUpdateSerializer

@api_view(['GET'])
def duplicate_user(request, username):
    User = get_user_model()
    exists = User.objects.filter(username=username).exists()
    return Response({'result': exists})

@api_view(['PUT'])  # PUT 메서드를 허용
def update(request):
    user = request.user
    serializer = UserUpdateSerializer(user, data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)