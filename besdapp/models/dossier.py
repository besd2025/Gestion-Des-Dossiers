from django.db import models
from django.conf import settings
from .timestamp import TimeStamps
from .soft_delete import SoftDeleteModel

class Dossier(SoftDeleteModel,TimeStamps,models.Model):
    class NiveauPriorite(models.TextChoices):
        normale = "NORMALE"
        urgente = "URGENTE"
        confidentiel = "CONFIDENTIEL"
    reference = models.CharField(max_length=50, unique=True)
    objet = models.TextField(blank=True,null=True)
    fichier = models.FileField(upload_to='pieces_jointes/', max_length=100,null=True,blank=True)
    annexe = models.FileField(upload_to='pieces_jointes/', max_length=100,null=True,blank=True)
    niveau_priorite = models.CharField(max_length=50, choices=NiveauPriorite, default=NiveauPriorite.normale)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_fin = models.DateField(null=True,blank=True)

######################################################################################

class EtatAvancement(SoftDeleteModel,TimeStamps,models.Model):
    class Status(models.TextChoices):
        return_dossier = "RETURN"
        assign = "ASSIGN"
        in_processing = 'IN PROCESSING'
        processed = 'PROCESSED'
        validated = "VALIDATED"
        REJECT = "REJECT"
        IN_VALIDATION = "IN_VALIDATION"
        ARCHIVED = "ARCHIVED"


    dossier=models.ForeignKey(Dossier,on_delete=models.CASCADE,related_name='dossier')
    
    previous_state=models.OneToOneField('self', on_delete=models.CASCADE,related_name='previous_etat', blank=True, null=True, related_query_name="previous_etat")
    user_actual=models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL, # Si l'utilisateur est supprimé, le dossier reste
        null=True,
        blank=True,
        related_name='dossiers_assignes'
    )
    comment=models.TextField()
    is_active = models.BooleanField(default=False)
    status = models.CharField(max_length=30, choices=Status, default=Status.assign)

