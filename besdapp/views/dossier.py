from rest_framework import viewsets, permissions
# CORRECTION : On importe la CLASSE Dossier depuis le FICHIER Dossier
from besdapp.models.dossier import Dossier,EtatAvancement  
from besdapp.serializer import DossierSerializer,EtatSerializer

class DossierViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les dossiers avec filtrage automatique.
    """
    serializer_class = DossierSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        
        # Sécurité : Si l'utilisateur n'est pas connecté (anonyme)
        if not user or user.is_anonymous:
            return Dossier.objects.none()

        # 1. Les admins et la Direction voient TOUT
        if user.is_superuser or user.groups.filter(name='Direction').exists():
            return Dossier.objects.all().order_by('-date_creation')
        
        # 2. Les autres ne voient que ce qui leur est assigné
        return Dossier.objects.filter(assigne_a=user).order_by('-date_creation')
    

class EtatViewSet(viewsets.ModelViewSet):
    serializer_class= EtatSerializer
    queryset= EtatAvancement.objects.all()