from besdapp.models.dossier import EtatAvancement
from rest_framework import serializers



class EtatSerializer(serializers.ModelSerializer):
    class Meta:
        model= EtatAvancement
        fields=['dossier','previous_state','user_actual','comment','is_active','status']
        