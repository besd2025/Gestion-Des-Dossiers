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
        
class DocumentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ["id", "fichier", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]

    def create(self, validated_data):
        """
        Création du document en utilisant le 'state' fourni depuis la vue.
        """
        state = self.context.get("state")
        if not state:
            raise serializers.ValidationError(
                "Impossible de trouver l'état actif pour l'utilisateur."
            )

        document = Document.objects.create(state=state, **validated_data)
        return document
