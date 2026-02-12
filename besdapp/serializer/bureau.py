from rest_framework import serializers
from besdapp.models.bureau import Bureau

class BureauSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bureau
        fields = '__all__'