from django.db import models
from .bureau import Bureau


class Cellule(models.Model):
    nom_cellule = models.CharField(max_length=255)
    code_cellule = models.CharField(max_length=50, unique=True)
    bureau = models.ForeignKey(Bureau, on_delete=models.CASCADE, related_name='cellules')
    
    
