from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from besdapp.models.authentification import CustomUser
from besdapp.serializer import CustomUserSerializer, RegisterSerializer, BureauSerializer, CelluleSerializer,MyTokenObtainPairSerializer  # N'oubliez pas d'importer ce nouveau serializer
from django.db.models import F
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny,IsAuthenticated

class LoginView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = MyTokenObtainPairSerializer

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.filter(user_role__isnull=False).annotate(role = F('user_role__nom_role'), bureau_cellule = F('user_role__role_bureau__bureau__nom_bureau'))

    # def get_permissions(self):
    #     """
    #     Définit qui peut faire quoi :
    #     - Inscription (create) : Tout le monde
    #     - Consultations (list, user_bureau, etc.) : Utilisateurs avec Token JWT
    #     """
    #     # if self.action == 'create':
    #     #     return [AllowAny()]
    #     # return [IsAuthenticated()]

    def get_serializer_class(self):
        # 1. Sérialiseur pour la création
        if self.action == 'create':
            return RegisterSerializer
        return CustomUserSerializer

    # --- ACTION 1 : Liste par Bureau ---
    @action(detail=False, methods=['get'], url_path='user-bureau')
    def user_bureau(self, request):
        """Retourne la liste simplifiée : id, nom, prenom, bureau, role"""
        queryset = CustomUser.objects.filter(user_role__isnull=False,user_role__role_bureau__isnull=False ).annotate(role = F('user_role__nom_role'), bureau_cellule = F('user_role__role_bureau__bureau__nom_bureau'))
        serializer = CustomUserSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def update_user(self, request, pk=None):
        user=self.get_object()
        user.is_actif = not user.is_actif 
        user.save()
        stat ="active" if user.is_actif else "desactive"
        return Response({
            'status':f'Utilisateur {stat} avec succès',
            'est_active': user.is_actif  
        })
        
    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
       user = self.get_object()
       user.is_actif = False
       user.save()
       return Response({'status': 'Utilisateur désactivé'}, status=status.HTTP_200_OK)

    # --- ACTION 2 : Liste par Cellule ---
    @action(detail=False, methods=['get'], url_path='user-cellule')
    def user_cellule(self, request):
        """Retourne la liste simplifiée : id, nom, prenom, bureau, cellule, role"""
        queryset = CustomUser.objects.filter(user_role__isnull=False,user_role__role_cellule__isnull=False).annotate(role= F('user_role__nom_role'), bureau_cellule=F('user_role__role_cellule__cellule__nom_cellule'),bureau_name=F('user_role__role_cellule__cellule__bureau__nom_bureau'))
        page=self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = CustomUserSerializer(queryset, many=True)
        return Response(serializer.data)
    
    
    
