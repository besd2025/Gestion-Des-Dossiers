from rest_framework import viewsets, generics, permissions
from besdapp.models.authentification import CustomUser
from besdapp.serializer import CustomUserSerializer, RegisterSerializer

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()

    def get_serializer_class(self):
        # Si on crée un utilisateur (POST), on utilise le sérialiseur d'inscription
        if self.action == 'create':
            return RegisterSerializer
        # Pour tout le reste (GET, PUT, DELETE), on utilise le sérialiseur standard
        return CustomUserSerializer