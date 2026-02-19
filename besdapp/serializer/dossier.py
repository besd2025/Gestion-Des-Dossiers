# Si ton fichier s'appelle Dossier.py et la classe dedans s'appelle Dossier :
from besdapp.models.dossier import Dossier 
from rest_framework import serializers


class DossierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dossier
        fields =['reference', 'objet', 'fichier','annexe','date_creation','niveau_priorite','date_fin']
        read_only_fields = ['date_creation'] # Dis à DRF de ne pas l'attendre dans le POST
        

# class EtatSerializer(serializers.ModelSerializer):
#     class Meta:
#         model= EtatAvancement
#         fields=['Id_dossier', 'previous_state','Id_user_actual''commentaire']
