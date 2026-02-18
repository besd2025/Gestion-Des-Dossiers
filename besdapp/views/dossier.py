from rest_framework import viewsets, permissions
# CORRECTION : On importe la CLASSE Dossier depuis le FICHIER Dossier
from django.db.models import Count,Q
from rest_framework.decorators import action
from rest_framework.response import Response
from besdapp.models.dossier import Dossier,EtatAvancement 
from besdapp.serializer import EtatSerializer
from besdapp.serializer import DossierSerializer
from besdapp.filters import DossierFilter
from django.utils import timezone
from datetime import timedelta
from django.db.models.functions import TruncDay, TruncWeek, TruncMonth
from django_filters.rest_framework import DjangoFilterBackend

class DossierViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les dossiers avec filtrage automatique.
    """
    queryset = Dossier.objects.all()
    serializer_class = DossierSerializer
    #permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = DossierFilter
    
        

    # def get_queryset(self):
    #     # user = self.request.user
        
    #     # # Sécurité : Si l'utilisateur n'est pas connecté (anonyme)
    #     # if not user or user.is_anonymous:
    #     #     return Dossier.objects.none()

    #     # # 1. Les admins et la Direction voient TOUT
    #     # if user.is_superuser or user.groups.filter(name='Direction').exists():
    #     #     return Dossier.objects.all().order_by('-date_creation')
        
    #     # 2. Les autres ne voient que ce qui leur est assigné
    #     return Dossier.objects.
    
    @action(detail=True, methods=["get"])
    def etapes(self, request, pk=None):
        dossier = self.get_object()
        etats = dossier.etats.all().order_by("created_at")
        serializer = EtatSerializer(etats, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='total-count')
    def total_dossiers(self,request):
        total = Dossier.objects.count()
        return Response({'total_dossiers': total })
    
    
    
    @action(detail=False, methods=["get"])
    def stats(self, request):
        stats = EtatAvancement.objects.filter(is_active=True).aggregate(
            total_traite=Count(
                "dossier",
                filter=Q(status="VALIDATED"),
                distinct=True
            ),
            total_archive=Count(
                "dossier",
                filter=Q(status="ARCHIVED"),
                distinct=True
            ),
            total_rejete=Count(
                "dossier",
                filter=Q(status="REJECT"),
                distinct=True
            ),
        )

        return Response(stats)
    
    
    @action(detail=False, methods=['get'])
    def recent_dossiers(self, request):
        dossiers = Dossier.objects.filter(is_deleted=False).order_by('-date_creation')[:5]
        serializer = self.get_serializer(dossiers, many=True)
        return Response(serializer.data)
    
     
  


# 
# class EtatViewSet(viewsets.ModelViewSet):
#     serializer_class= EtatSerializer
#     queryset= EtatAvancement.objects.all() 


   



     
