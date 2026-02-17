from django.db.models import F , Q, Count
from rest_framework import viewsets
from besdapp.models import Cellule,CustomUser,Dossier
from besdapp.serializer import CelluleSerializer,CustomUserSerializer,DossierSerializer
from rest_framework.decorators import action
from rest_framework.response import Response


class CelluleViewSet(viewsets.ModelViewSet):
    queryset = Cellule.objects.all()
    serializer_class = CelluleSerializer
    
    
    @action(detail=True, methods=['get'])
    def user_cellul_role(self, request , pk=None):
        usercellulrol=CustomUser.objects.filter(user_role__role_cellule__cellule__nom_cellule__isnull=False).annotate(nom_role=F('user_role__nom_role'),nom_cellule=F('user_role__role_cellule__cellule__nom_cellule'))
        serializer=CustomUserSerializer(usercellulrol, many=True)
        return Response(serializer.data)
    
    
    @action(detail=True, methods=['get'])
    def All_doss_cellule(self,request ,pk=None):
        doss_cellule=Dossier.objects.filter(dossier__user_actual__user_role__role_cellule__cellule__nom_cellule__isnull=False).annotate(dossiers=F('dossier__user_actual'),nom_cellule=F('dossier__user_actual__user_role__role_cellule__cellule__nom_cellule'))
        serializer=DossierSerializer(doss_cellule, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def stat_cel(self,request,pk=None):
        tot_cellule=Cellule.objects.annotate(tot_doss_cel=Count('cellule_role__role__user__dossiers_assignes__dossier',distinct=True),
                                 tot_return=Count('cellule_role__role__user__dossiers_assignes__dossier',filter=Q(cellule_role__role__user__dossiers_assignes__status='RETURN'),distinct=True),
                                 tot_assign=Count('cellule_role__role__user__dossiers_assignes__dossier',filter=Q(cellule_role__role__user__dossiers_assignes__status='ASSIGN'),distinct=True),
                                 tot_send=Count('cellule_role__role__user__dossiers_assignes__dossier',filter=Q(cellule_role__role__user__dossiers_assignes__status='SEND'),distinct=True),
                                 tot_recu=Count('cellule_role__role__user__dossiers_assignes__dossier',filter=Q(cellule_role__role__user__dossiers_assignes__status='RECU'),distinct=True),
                                 tot_en_cours=Count('cellule_role__role__user__dossiers_assignes__dossier',filter=Q(cellule_role__role__user__dossiers_assignes__status='IN PROCESSING'),distinct=True),
                                 tot_valide=Count('cellule_role__role__user__dossiers_assignes__dossier',filter=Q(cellule_role__role__user__dossiers_assignes__status='VALIDATED'),distinct=True),
                                 tot_rejete=Count('cellule_role__role__user__dossiers_assignes__dossier',filter=Q(cellule_role__role__user__dossiers_assignes__status='REJECT'),distinct=True),
                                 tot_en_validation=Count('cellule_role__role__user__dossiers_assignes__dossier',filter=Q(cellule_role__role__user__dossiers_assignes__status='IN_VALIDATION'),distinct=True),
                                 tot_archive=Count('cellule_role__role__user__dossiers_assignes__dossier',filter=Q(cellule_role__role__user__dossiers_assignes__status='ARCHIVED'),distinct=True),
                                )
        
        serializer=CelluleSerializer(tot_cellule, many=True)
        return Response(serializer.data)
        # for a in tot_cellule:
        #     print(f"Cellule:{a.nom_cellule}|nbre des dossiers:{a.tot_doss_cel}")