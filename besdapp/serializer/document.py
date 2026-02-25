from rest_framework import serializers
from besdapp.models.document import Document
from .etatavancement import EtatSerializer

class DocumentSerializer(serializers.ModelSerializer):
    # Affiche la référence du dossier au lieu de son ID simple (lecture seule)
    # state = EtatSerializer(read_only=True)

    class Meta:
        model = Document
        fields = ['id', 'state', 'fichier','created_at','updated_at']
        read_only_fields = ["id",'created_at','updated_at']
