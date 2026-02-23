# Si ton fichier s'appelle Dossier.py et la classe dedans s'appelle Dossier :
from besdapp.models.dossier import Dossier 
from rest_framework import serializers
from .authentification import CustomUserSerializer


class DossierSerializer(serializers.ModelSerializer):
    utilisateur = serializers.SerializerMethodField()

    class Meta:
        model = Dossier
        fields = [
            'reference',
            'objet',
            'fichier',
            'annexe',
            'date_creation',
            'niveau_priorite',
            'date_fin',
            'description',
            'utilisateur'
        ]
        read_only_fields = ['date_creation']

    def get_utilisateur(self, obj):
        # récupérer l'état actif
        etat_actif = obj.dossier.filter(is_active=True).first()

        if etat_actif and etat_actif.user_actual:
            return CustomUserSerializer(etat_actif.user_actual).data

        return "Non assigné"
# class EtatSerializer(serializers.ModelSerializer):
#     class Meta:
#         model= EtatAvancement
#         fields=['Id_dossier', 'previous_state','Id_user_actual''commentaire']
