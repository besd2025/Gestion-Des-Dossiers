from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from besdapp.models import Roles
from besdapp.serializer import RoleSerializer


class RoleViewSet(ModelViewSet):
    serializer_class=RoleSerializer
    queryset= Roles.objects.all()
    
