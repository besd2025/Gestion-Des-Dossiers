from django.db.models import F , Q
from rest_framework import viewsets
from besdapp.models import Cellule,CustomUser,Dossier
from besdapp.serializer import CelluleSerializer,CustomUserSerializer,DossierSerializer
from rest_framework.decorators import action
from rest_framework.response import Response


class CelluleViewSet(viewsets.ModelViewSet):
    queryset = Cellule.objects.all()
    serializer_class = CelluleSerializer
    
    
    @action(detail=True, methods=['get'])
    def user_cellul_role(self, request , pk=None):
        usercellulrol=CustomUser.objects.filter(user_role__role_cellule__cellule__nom_cellule__isnull=False).annotate(nom_role=F('user_role__nom_role'),nom_cellule=F('user_role__role_cellule__cellule__nom_cellule'))
        serializer=CustomUserSerializer(usercellulrol, many=True)
        return Response(serializer.data)
    
    
    @action(detail=True, methods=['get'])
    def All_doss_cellule(self,request ,pk=None):
        doss_cellule=Dossier.objects.filter(dossier__user_actual__user_role__role_cellule__cellule__nom_cellule__isnull=False).annotate(dossiers=F('dossier__user_actual'),nom_cellule=F('dossier__user_actual__user_role__role_cellule__cellule__nom_cellule'))
        serializer=DossierSerializer(doss_cellule, many=True)
        return Response(serializer.data)