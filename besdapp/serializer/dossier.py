# Si ton fichier s'appelle Dossier.py et la classe dedans s'appelle Dossier :
from besdapp.models.dossier import Dossier 
from rest_framework import serializers
from .authentification import CustomUserSerializer
from .etatavancement import EtatSerializer
# serializers/activity.py

from rest_framework import serializers
from besdapp.models import EtatAvancement

class ObservationSerializer(serializers.ModelSerializer):
    role_name = serializers.SerializerMethodField()
    user_full_name = serializers.SerializerMethodField()
    date_action = serializers.SerializerMethodField()
    observation = serializers.CharField(source="comment")

    class Meta:
        model = EtatAvancement
        fields = [
            "role_name",
            "user_full_name",
            "date_action",
            "observation",
        ]

    def get_user_full_name(self, obj):
        if obj.user_actual:
            return f"{obj.user_actual.prenom} {obj.user_actual.nom}"
        return "Utilisateur inconnu"

    def get_role_name(self, obj):
        if obj.user_actual and hasattr(obj.user_actual, "user_role"):
            return obj.user_actual.user_role.get_nom_role_display()
        return None

    def get_date_action(self, obj):
        return obj.created_at.strftime("%d/%m/%Y à %H:%M")


class DossierActivitySerializer(serializers.ModelSerializer):
    action = serializers.SerializerMethodField()
    user_full_name = serializers.SerializerMethodField()
    role_name = serializers.SerializerMethodField()
    date_action = serializers.SerializerMethodField()

    class Meta:
        model = EtatAvancement
        fields = [
            "action",
            "user_full_name",
            "role_name",
            "date_action",
        ]

    def get_action(self, obj):
        mapping = {
            "ASSIGN": "Dossier transféré",
            "IN_PROCESSING": "Dossier reçu",
            "PROCESSED": "Dossier traité",
            "VALIDATED": "Dossier validé",
            "REJECT": "Dossier rejeté",
            "RETURN": "Dossier retourné",
            "IN_VALIDATION": "En validation",
            "ARCHIVED": "Dossier archivé",
        }
        return mapping.get(obj.status, "Action inconnue")

    def get_user_full_name(self, obj):
        if obj.user_actual:
            return f"{obj.user_actual.prenom} {obj.user_actual.nom}"
        return "Utilisateur inconnu"

    def get_role_name(self, obj):
        if obj.user_actual and hasattr(obj.user_actual, "user_role"):
            return obj.user_actual.user_role.get_nom_role_display()
        return None

    def get_date_action(self, obj):
        return obj.created_at.strftime("Le %d/%m/%Y à %H:%M")


class DossierSerializer(serializers.ModelSerializer):
    utilisateur = serializers.SerializerMethodField()
    is_assign = serializers.SerializerMethodField() 
    status = serializers.SerializerMethodField()

    class Meta:
        model = Dossier
        fields = [
            'id',
            'reference',
            'objet',
            'fichier',
            'annexe',
            'date_creation',
            'niveau_priorite',
            'date_fin',
            'description',
            'utilisateur',
            'is_assign',
            'status'
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

    def get_is_assign(self, obj):
        etat_actif = next(
            (etat for etat in obj.dossier.all() if etat.is_active),
            None
        )
        return bool(etat_actif and etat_actif.user_actual)
        
    def get_status(self, obj):
        etat_actif = next(
            (etat for etat in obj.dossier.all() if etat.is_active),
            None
        )

        if not etat_actif:
            return None

        return EtatSerializer(etat_actif).data
# class EtatSerializer(serializers.ModelSerializer):
#     class Meta:
#         model= EtatAvancement
#         fields=['Id_dossier', 'previous_state','Id_user_actual''commentaire']
