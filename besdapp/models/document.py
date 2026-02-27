from django.db import models
from .dossier import Dossier
from .timestamp import TimeStamps
from .soft_delete import SoftDeleteModel
from .dossier import EtatAvancement

class Document(SoftDeleteModel,TimeStamps,models.Model):
    state = models.ForeignKey(to = EtatAvancement, on_delete=models.CASCADE, related_name="state", related_query_name="state")
    fichier = models.FileField(upload_to='pieces_jointes/', max_length=100)
