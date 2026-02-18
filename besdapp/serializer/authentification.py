from rest_framework import serializers
# IMPORTATION DEPUIS LES MODELS (et non depuis lui-même)
from besdapp.models.authentification import CustomUser
from besdapp.models.roles import Roles,RoleBureau,RoleCellure
from besdapp.models.bureau import Bureau
from besdapp.models.cellule import Cellule
from django.db import transaction
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.core.exceptions import ObjectDoesNotExist
from besdapp.models import Roles


# --- 1. SÉRIALISEUR DE CONSULTATION (Affichage) ---
class CustomUserSerializer(serializers.ModelSerializer):
    role = serializers.CharField(read_only = True)
    bureau_cellule = serializers.CharField(read_only = True)
    bureau_name= serializers.CharField(read_only=True)

    class Meta:
        model = CustomUser
        fields = [
            'id', 'nom', 'prenom', 'email','role','bureau_cellule','bureau_name','is_actif'
        ]

# --- 2. SÉRIALISEUR D'INSCRIPTION (Création) ---
class RegisterSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(
        write_only=True, 
        required=True,
        style={'input_type': 'password'}
    )

    role=serializers.CharField(write_only=True, 
        required=True)
    type_service=serializers.CharField(write_only=True, 
        required=True)
    bureau_cellule_code=serializers.CharField(write_only=True, 
        required=True)
    

    class Meta:
        model = CustomUser
        fields = [
            'email', 
            'password', 
            'password_confirm',  # <--- IL DOIT ÊTRE ICI AUSSI
            'nom', 
            'prenom',
            'role',
            'type_service',
            'bureau_cellule_code',

        ]
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, data):
        """Vérifie si les deux mots de passe correspondent."""
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError(
                {"password": "Les deux mots de passe ne correspondent pas."}
            )
        return data

    def create(self, validated_data):
        """Crée l'utilisateur en utilisant create_user pour le hachage du mot de passe."""
        # On retire la confirmation avant d'envoyer les données au Manager
        validated_data.pop('password_confirm')
        role_data = validated_data.pop('role')
        type_service = validated_data.pop('type_service')
        bureau_cellule = validated_data.pop('bureau_cellule_code')

        with transaction.atomic():
            # On utilise create_user qui s'occupe de set_password()
            user = CustomUser.objects.create_user(**validated_data)
            #Role
            role = Roles.objects.create(user = user, nom_role=role_data )
            role.save()
            if type_service == "BUREAU":
                bureau = Bureau.objects.filter(code_bureau =bureau_cellule ).first()
                role = RoleBureau.objects.create(role=role, bureau = bureau)
                return user
            else:
                cellule = Cellule.objects.filter(code_cellule =bureau_cellule ).first()
                role = RoleCellure.objects.create(role=role, cellule = cellule)
                return user


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Ajout des informations personnalisées dans le payload du JWT
        token['nom'] = user.nom
        token['prenom'] = user.prenom
        token['email'] =user.email
    
        
        try:
            role_rel = user.user_role   # NO .first()
            token["type_service"] = "Bureau" if role_rel.nom_role in [Roles.CHEF_ADJOINT_BUREAU, Roles.CHEF_BUREAU] else "Secretariat" if  role_rel.nom_role == Roles.SECRETARIAT else "Cellule"
            token['role'] = role_rel.nom_role
            token["bureau"] =role_rel.role_bureau.bureau.nom_bureau if role_rel.nom_role in [Roles.CHEF_ADJOINT_BUREAU, Roles.CHEF_BUREAU,Roles.SECRETARIAT] else role_rel.role_cellule.cellule.bureau.nom_bureau
            if role_rel.nom_role not in [Roles.CHEF_ADJOINT_BUREAU, Roles.CHEF_BUREAU,Roles.SECRETARIAT]:
                token['cellule'] = role_rel.role_cellule.cellule.nom_cellule
        except ObjectDoesNotExist:
            token['role'] = None

        return token
        
        # # On récupère le nom du rôle (via votre relation user_role)
        # # Note : adaptez 'user_role' selon le related_name de votre modèle Roles
        # role_obj = user.user_role.first() 
        # token['role'] = role_obj.nom_role if role_obj else "Aucun rôle"

        # return token

    