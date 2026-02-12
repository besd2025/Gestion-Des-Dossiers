from django.db import models
from .timestamp import TimeStamps
from .soft_delete import SoftDeleteModel
from .bureau import Bureau
from .cellule import Cellule

class Roles(TimeStamps,SoftDeleteModel,models.Model):
    SECRETARIAT = 'SECRETARIAT'
    CHEF_BUREAU = 'CHEF_BUREAU'
    CHEF_ADJOINT_BUREAU = 'CHEF_ADJOINT_BUREAU'
    CHEF_CELLULE = 'CHEF_CELLULE'
    CHEF_CELLULE_ADJOINT = 'CHEF_CELLULE_ADJOINT'
    CONSEILLER = 'CONSEILLER'

    ROLE_CHOICES = [
        (SECRETARIAT, 'Secrétariat'),
        (CHEF_BUREAU, 'Chef Bureau'),
        (CHEF_ADJOINT_BUREAU, 'Chef Adjoint Bureau'),
        (CHEF_CELLULE, 'Chef Cellule'),
        (CHEF_CELLULE_ADJOINT, 'Chef Cellule Adjoint'),
        (CONSEILLER, 'Conseiller'),
    ]
    user = models.OneToOneField('besdapp.CustomUser', on_delete=models.CASCADE, related_name="user_role", related_query_name="user_role")
    nom_role = models.CharField(
        max_length=50,
        choices=ROLE_CHOICES, 
        default=CONSEILLER,
        unique=True
    )

class RoleBureau(TimeStamps,SoftDeleteModel,models.Model):
    role = models.OneToOneField(to = Roles, on_delete=models.CASCADE, related_name="role_bureau",  related_query_name="role_bureau")
    bureau = models.ForeignKey(to=Bureau, on_delete=models.CASCADE, related_name="bureau_role", related_query_name="bureau_role")


class RoleCellure(TimeStamps,SoftDeleteModel,models.Model):
    role = models.OneToOneField(to = Roles, on_delete=models.CASCADE, related_name="role_cellule",  related_query_name="role_cellule")
    cellule = models.ForeignKey(to=Cellule, on_delete=models.CASCADE, related_name="cellule_role", related_query_name="cellule_role")

