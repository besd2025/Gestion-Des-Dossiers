from django.db import models
from .timestamp import TimeStamps
from .soft_delete import SoftDeleteModel

class Bureau(TimeStamps,SoftDeleteModel,models.Model):
    nom_bureau = models.CharField(max_length=100) 
    code_bureau = models.CharField(max_length=50, unique=True)
