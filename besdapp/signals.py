from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models.dossier import Dossier
from .models.notification import Notification

# @receiver(post_save, sender=Dossier)
# def creer_et_envoyer_notification(sender, instance, created, **kwargs):
#     # 1. Vérifier si un utilisateur est assigné
#     #if instance.assigne_a:
#         #message_notif = f"Le dossier {instance.reference} vous a été assigné."
        
#         # 2. Création de la notification en base de données (ton code actuel)
#         # notif, created_now = Notification.objects.get_or_create(
#         #     destinataire=instance.assigne_a,
#         #     message=message_notif,
#         #     defaults={'lu': False}
#         # )

#         # 3. Envoi en temps réel via WebSocket (Ajout)
#         channel_layer = get_channel_layer()
#         # On cible le groupe spécifique de l'utilisateur
#         group_name = f'user_{instance.assigne_a.id}'
        
#         async_to_sync(channel_layer.group_send)(
#             group_name,
#             {
#                 'type': 'send_notification', # Appelle la méthode dans le Consumer
#                 'message': message_notif,
#                 'notification_id': notif.id,
#                 'reference_dossier': instance.reference
#             }
#         )