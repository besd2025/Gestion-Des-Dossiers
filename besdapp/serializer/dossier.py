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
        # on suppose qu'il y a au max un seul état actif (bonne pratique)
        etat_actif = next(
            (etat for etat in obj.dossier.all() if etat.is_active),
            None
        )

        if not etat_actif or not etat_actif.user_actual:
            return "Non assigné"

        user = etat_actif.user_actual

        return {
            "id": user.id,
            "nom": user.nom,
            "prenom": user.prenom,
            "email": user.email,
            "is_actif": user.is_actif,
            "role": getattr(etat_actif, "role", None),
            "bureau_cellule": getattr(etat_actif, "bureau_cellule", None),
            "bureau_name": getattr(etat_actif, "bureau_name", None),
        }
# class EtatSerializer(serializers.ModelSerializer):
#     class Meta:
#         model= EtatAvancement
#         fields=['Id_dossier', 'previous_state','Id_user_actual''commentaire']
