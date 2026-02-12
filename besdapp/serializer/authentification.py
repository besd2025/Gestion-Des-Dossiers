from rest_framework import serializers
# IMPORTATION DEPUIS LES MODELS (et non depuis lui-même)
from besdapp.models.authentification import CustomUser 
from besdapp.models.roles import Roles
from besdapp.models.cellule import Cellule
from besdapp.models.bureau import Bureau

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
    # Champ pour confirmer le mot de passe (ne sera pas stocké en base)
    password_confirm = serializers.CharField(
        write_only=True, 
        required=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = CustomUser
        fields = [
            'email', 'password', 'password_confirm', 
            'nom', 'prenom', 'role', 'cellule', 'bureau'
        ]
        extra_kwargs = {
            'password': {'write_only': True, 'style': {'input_type': 'password'}},
            'nom': {'required': True},
            'prenom': {'required': True}
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
        
        # On utilise create_user qui s'occupe de set_password()
        user = CustomUser.objects.create_user(**validated_data)
        return user