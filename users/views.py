from django.shortcuts import render
from rest_framework import viewsets, permissions

from users.models import User
from users.serializer import UserSerializer



class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    # permission_classes = (AllowAny,)
