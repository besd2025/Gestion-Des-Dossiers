from rest_framework import serializers
from besdapp.models.cellule import Cellule

class CelluleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cellule
        fields = '__all__'