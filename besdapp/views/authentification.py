from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from besdapp.models.authentification import CustomUser
from besdapp.serializer import CustomUserSerializer, RegisterSerializer, BureauSerializer, CelluleSerializer  # N'oubliez pas d'importer ce nouveau serializer
from django.db.models import F


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.filter(user_role__isnull=False).annotate(role = F('user_role__nom_role'), bureau_cellule = F('user_role__role_bureau__bureau__nom_bureau'))

    def get_serializer_class(self):
        # 1. Sérialiseur pour la création
        if self.action == 'create':
            return RegisterSerializer
        
        # 2. Sérialiseur pour la liste par bureau
        if self.action == 'user_bureau':
            return BureauSerializer
            
        # 3. Sérialiseur pour la liste par cellule (Action 2)
        if self.action == 'user_cellule':
            return CelluleSerializer
            
        return CustomUserSerializer

    # --- ACTION 1 : Liste par Bureau ---
    @action(detail=False, methods=['get'], url_path='user-bureau')
    def user_bureau(self, request):
        """Retourne la liste simplifiée : id, nom, prenom, bureau, role"""
        queryset = CustomUser.objects.filter(user_role__isnull=False,user_role__role_bureau__isnull=False ).annotate(role = F('user_role__nom_role'), bureau_cellule = F('user_role__role_bureau__bureau__nom_bureau'))
        serializer = CustomUserSerializer(queryset, many=True)
        return Response(serializer.data)

    # --- ACTION 2 : Liste par Cellule ---
    @action(detail=False, methods=['get'], url_path='user-cellule')
    def user_cellule(self, request):
        """Retourne la liste simplifiée : id, nom, prenom, bureau, cellule, role"""
        queryset = CustomUser.objects.filter(user_cellule__isnull=False,user_cellule__cellule_bureau__isnull=False).annotate(cellule= F('user_cellule__nom_cellule'), bureau_role=F('user_cellule__cellule_bureau__buraeu__nom_bureau'))
        serializer = CustomUserSerializer(queryset, many=True)
        return Response(serializer.data)
