from rest_framework import serializers
from besdapp.models.notification import Notification,Message


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model=Message
        fields='__all__'


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'destinataire','dossier','Id_message', 'Id_avancement','lu']
        read_only_fields = ['destinataire', 'date_creation']