from rest_framework import viewsets, permissions
# CORRECTION : On importe la CLASSE Dossier depuis le FICHIER Dossier

from rest_framework.decorators import action
from rest_framework.response import Response
from besdapp.models.dossier import Dossier,EtatAvancement 
from besdapp.serializer import DossierSerializer,EtatSerializer
from besdapp.filters import DossierFilter
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
    #     return Dossier.objects.all()
    
    @action(detail=False, methods=['get'], url_path='total-count')
    def total_dossiers(self,request):
        total = Dossier.objects.count()
        return Response({'total_dossiers': total })
    
    

class EtatViewSet(viewsets.ModelViewSet):
    serializer_class= EtatSerializer
    queryset= EtatAvancement.objects.all() 
     
