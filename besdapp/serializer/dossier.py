# Si ton fichier s'appelle Dossier.py et la classe dedans s'appelle Dossier :
from besdapp.models.dossier import Dossier 
from rest_framework import serializers


class DossierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dossier
        fields =['reference','objet','fichier','statut_actuel']
        read_only_fields = ['date_creation'] # Dis à DRF de ne pas l'attendre dans le POST


