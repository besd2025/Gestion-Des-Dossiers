from rest_framework import serializers
from besdapp.models.cellule import Cellule
from .bureau import BureauSerializer
class CelluleSerializer(serializers.ModelSerializer):
    bureau = BureauSerializer(read_only=True)
    class Meta:
        model = Cellule
        fields = ['id', 'nom_cellule', 'code_cellule', 'bureau']
