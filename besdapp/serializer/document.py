from rest_framework import serializers
from besdapp.models.document import Document,EtatAvancement
from .etatavancement import EtatSerializer

class DocumentSerializer(serializers.ModelSerializer):
    state = serializers.PrimaryKeyRelatedField(
        queryset=EtatAvancement.objects.filter(is_active=True)
    )

    class Meta:
        model = Document
        fields = ['id', 'state', 'fichier', 'created_at', 'updated_at']
        read_only_fields = ["id", "created_at", "updated_at"]
