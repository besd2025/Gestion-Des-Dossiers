import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # On récupère l'ID de l'utilisateur via le scope
        self.user = self.scope["user"]
        
        if self.user.is_authenticated:
            self.group_name = f'user_{self.user.id}'
            
            # Rejoindre le groupe privé de l'utilisateur
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()
        else:
            # Refuser la connexion si l'utilisateur n'est pas connecté
            await self.close()

    async def disconnect(self, close_code):
        if hasattr(self, 'group_name'):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    # Méthode déclenchée par le signal (type: send_notification)
    async def send_notification(self, event):
        # Envoi effectif vers le navigateur (Frontend)
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'notification_id': event.get('notification_id'),
            'reference': event.get('reference_dossier')
        }))