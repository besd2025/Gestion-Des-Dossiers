from django.db import models
from django.conf import settings # Importe les réglages pour trouver le CustomUser
from .dossier import EtatAvancement,Dossier
from .timestamp import TimeStamps
from .soft_delete import SoftDeleteModel


class Message(TimeStamps,SoftDeleteModel,models.Model):
    Id_message=models.AutoField(primary_key=True)
    message=models.TextField()
####################################################################################
class Notification(TimeStamps,SoftDeleteModel,models.Model):
    # Remplace l'import de 'Utilisateurs' par settings.AUTH_USER_MODEL
    destinataire = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE
    )

    Id_message = models.ForeignKey(Message, on_delete=models.CASCADE ,related_name='id_message',null=True,
        blank=True)
    Id_avancement=models.ForeignKey(EtatAvancement, on_delete=models.CASCADE,related_name='id_avancement',null=True,
        blank=True)
    lu = models.BooleanField(default=False)
    date_creation = models.DateTimeField(auto_now_add=True)
