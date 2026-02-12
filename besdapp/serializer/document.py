from rest_framework import serializers
from besdapp.models.document import Document

class DocumentSerializer(serializers.ModelSerializer):
    # Affiche la référence du dossier au lieu de son ID simple (lecture seule)
    dossier_ref = serializers.ReadOnlyField(source='dossier.reference')

    class Meta:
        model = Document
        fields = ['id', 'dossier', 'dossier_ref', 'fichier']