from rest_framework import serializers
from besdapp.models.roles import Roles

class RoleSerializer(serializers.ModelSerializer):
    # Ce champ permet d'afficher le nom lisible (ex: "Chef Bureau") 
    # au lieu du code (ex: "CHEF_BUREAU") dans les réponses GET
    nom_role_display = serializers.CharField(source='get_nom_role_display', read_only=True)

    class Meta:
        model = Roles
        fields = ['id', 'nom_role', 'nom_role_display']