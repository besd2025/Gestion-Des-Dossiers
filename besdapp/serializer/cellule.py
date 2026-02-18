from rest_framework import serializers
from besdapp.models.cellule import Cellule

class CelluleSerializer(serializers.ModelSerializer):
    tot_doss_cel= serializers.IntegerField(read_only=True)
    tot_return=serializers.IntegerField(read_only=True)
    tot_assign=serializers.IntegerField(read_only=True)
    tot_send=serializers.IntegerField(read_only=True)
    tot_recu=serializers.IntegerField(read_only=True)
    tot_en_cours=serializers.IntegerField(read_only=True)
    tot_valide=serializers.IntegerField(read_only=True)
    tot_rejete=serializers.IntegerField(read_only=True)
    tot_en_validation=serializers.IntegerField(read_only=True)
    tot_archive=serializers.IntegerField(read_only=True)
    class Meta:
        model = Cellule

        fields = ['id', 'nom_cellule', 'code_cellule', 'bureau',
                  'tot_doss_cel','tot_return','tot_assign','tot_send',
                  'tot_recu','tot_en_cours','tot_valide','tot_rejete',
                  'tot_en_validation','tot_archive'
                  ]
