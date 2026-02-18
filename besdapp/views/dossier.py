from rest_framework import viewsets, permissions
# CORRECTION : On importe la CLASSE Dossier depuis le FICHIER Dossier
from rest_framework.decorators import action
from rest_framework.response import Response
from besdapp.models.dossier import Dossier,EtatAvancement 
from besdapp.serializer import DossierSerializer
from besdapp.filters import DossierFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from django.db.models import Count
from django.db.models.functions import TruncDay, TruncWeek, TruncYear,TruncMonth
from django.utils.dateparse import parse_date # Pour valider les dates
from rest_framework.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta

class DossierViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les dossiers avec filtrage automatique.
    """
    queryset = Dossier.objects.all()
    serializer_class = DossierSerializer
    #permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = DossierFilter


    # def get_queryset(self):
    #     user=self.request.user
    #     role_rel=user.user_role.first()
    #     role=role_rel.nom_role if role_rel else None

    #     if role =='CHEF_BUREAU':
    #         return Dossier.objects.all()
    #     elif role=='Chef Adjoint Bureau':
    #         return Dossier.objects.all()
    #     elif role=='Chef Cellule':
    #         return Dossier.objects.filter(cellule=user.cellule)
    #     elif role =='CHEF_CELLULE_ADJOINT':
    #         return Dossier.objects.filter(cellule=user.cellule)
    #     elif role=='CONSEILLER':
    #         return Dossier.objects.filter(assigne_a=user)
    #     return Dossier.objects.none()
    
    @action(detail=False,methods=['get'])
    def statistiques(self, request):
        qs=self.get_queryset()

        period = request.query_params.get('period')
        now = timezone.now()

        if period == 'jour':
            qs = qs.filter(date_creation__date=now.date())
        elif period == 'semaine':
            # 7 derniers jours
            start_date = now - timedelta(days=7)
            qs = qs.filter(date_creation__gte=start_date)
        elif period == 'mois':
            # Dossiers du mois en cours
            qs = qs.filter(date_creation__year=now.year, date_creation__month=now.month)
        elif period == 'annee':
            # Dossiers de l'année en cours
            qs = qs.filter(date_creation__year=now.year)

        # stats_jour=qs.annotate(date=TruncDay('date_creation'))\
        #              .values('date').order_by('-date').annotate(total=Count('id'))
        # stats_semaine=qs.annotate(date=TruncWeek('date_creation'))\
        #              .values('date').order_by('-date').annotate(total=Count('id'))
        # stats_mois=qs.annotate(date=TruncMonth('date_creation'))\
        #              .values('date').order_by('-date').annotate(total=Count('id'))
        # stats_annee=qs.annotate(date=TruncYear('date_creation'))\
        #              .values('date').order_by('-date').annotate(total=Count('id'))
        stats = qs.annotate(date=TruncDay('date_creation'))\
                  .values('date').order_by('-date').annotate(total=Count('id'))
        return Response({
            "periode_choisie": period if period else "Toutes",
            "total_dossiers": qs.count(),
            "resultats": stats
        })


    # def get_queryset(self):
    #     # user = self.request.user
        
    #     # # Sécurité : Si l'utilisateur n'est pas connecté (anonyme)
    #     # if not user or user.is_anonymous:
    #     #     return Dossier.objects.none()

    #     # # 1. Les admins et la Direction voient TOUT
    #     # if user.is_superuser or user.groups.filter(name='Direction').exists():
    #     #     return Dossier.objects.all().order_by('-date_creation')
        
    #     # 2. Les autres ne voient que ce qui leur est assigné
    #     return Dossier.objects.all()
    
    @action(detail=False, methods=['get'], url_path='total-count')
    def total_dossiers(self,request):
        total = Dossier.objects.count()
        return Response({'total_dossiers': total })
    
    

# class EtatViewSet(viewsets.ModelViewSet):
#     serializer_class= EtatSerializer
#     queryset= EtatAvancement.objects.all() 
     
