from rest_framework import serializers
# IMPORTATION DEPUIS LES MODELS (et non depuis lui-même)
from besdapp.models.authentification import CustomUser
from besdapp.models.roles import Roles,RoleBureau,RoleCellure
from besdapp.models.bureau import Bureau
from besdapp.models.cellule import Cellule
from django.db import transaction


# --- 1. SÉRIALISEUR DE CONSULTATION (Affichage) ---
class CustomUserSerializer(serializers.ModelSerializer):
    role = serializers.CharField(read_only = True)
    bureau_cellule = serializers.CharField(read_only = True)

    class Meta:
        model = CustomUser
        fields = [
            'id', 'nom', 'prenom', 'email','role','bureau_cellule'
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

            

        