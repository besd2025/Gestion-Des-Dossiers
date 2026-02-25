from rest_framework import viewsets, permissions
from django.db.models import Count,Q
from rest_framework.decorators import action
from rest_framework.response import Response
from besdapp.models.dossier import Dossier,EtatAvancement 
from besdapp.serializer import EtatSerializer
from besdapp.serializer import DossierSerializer
from besdapp.filters import DossierFilter
from django.utils import timezone
from datetime import timedelta
from django.db.models.functions import TruncDay, TruncWeek, TruncMonth
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from django.db.models import Count,F
from django.db.models.functions import TruncDay, TruncWeek, TruncYear,TruncMonth
from django.utils.dateparse import parse_date # Pour valider les dates
from rest_framework.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
from django.db.models import Prefetch
from besdapp.models.authentification import CustomUser
class DossierViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les dossiers avec filtrage automatique.
    """
    serializer_class = DossierSerializer
    #permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = DossierFilter

    def get_queryset(self):

        etat_queryset = EtatAvancement.objects.filter(
            is_active=True
        ).select_related(
            'user_actual',
            'user_actual__user_role',
            'user_actual__user_role__role_bureau__bureau'
        ).annotate(
            role=F('user_actual__user_role__nom_role'),
            bureau_cellule=F('user_actual__user_role__role_cellule__cellule__nom_cellule'),
            bureau_name=F('user_actual__user_role__role_cellule__cellule__bureau__nom_bureau'),
        )

        return Dossier.objects.prefetch_related(
            Prefetch('dossier', queryset=etat_queryset)
        )
        


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



    # def get_queryset(self):
    #     # user = self.request.user
        
    #     # # Sécurité : Si l'utilisateur n'est pas connecté (anonyme)
    #     # if not user or user.is_anonymous:
    #     #     return Dossier.objects.none()

    #     # # 1. Les admins et la Direction voient TOUT
    #     # if user.is_superuser or user.groups.filter(name='Direction').exists():
    #     #     return Dossier.objects.all().order_by('-date_creation')
        
    #     # 2. Les autres ne voient que ce qui leur est assigné
    #     return Dossier.objects.
    
    @action(detail=True, methods=["get"])
    def etapes(self, request, pk=None):
        dossier = self.get_object()
        etats = dossier.etats.all().order_by("created_at")
        serializer = EtatSerializer(etats, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path="statistiques")
    def statistiques(self, request):
        periode = request.query_params.get("periode")
        now = timezone.now()

        # -------------------------
        # CONFIGURATION
        # -------------------------

        if periode == "jour":
            trunc = TruncDay
            periods = [
                (now - timedelta(days=i)).date()
                for i in range(11, -1, -1)
            ]

        elif periode == "semaine":
            trunc = TruncWeek
            periods = []
            for i in range(11, -1, -1):
                date = now - timedelta(weeks=i)
                monday = (date - timedelta(days=date.weekday())).date()
                periods.append(monday)

        elif periode == "mois":
            trunc = TruncMonth
            periods = []
            for i in range(11, -1, -1):
                year = now.year
                month = now.month - i
                while month <= 0:
                    month += 12
                    year -= 1
                periods.append(timezone.datetime(year, month, 1).date())

        elif periode == "annee":
            trunc = TruncYear
            periods = [
                timezone.datetime(now.year - i, 1, 1).date()
                for i in range(11, -1, -1)
            ]

        else:
            return Response({"error": "Période invalide"}, status=400)

        date_from = periods[0]

        # -------------------------
        # QUERY
        # -------------------------

        queryset = (
            Dossier.objects
            .filter(date_creation__date__gte=date_from)
            .annotate(period=trunc("date_creation"))
            .values("period")
            .annotate(count=Count("id"))
        )

        db_data = {
            item["period"].date(): item["count"]
            for item in queryset
        }

        # -------------------------
        # ZERO FILL
        # -------------------------

        result = []

        for period in periods:
            result.append({
                "period": period,
                "count": db_data.get(period, 0)
            })

        return Response(result)
    
    @action(detail=False, methods=['get'], url_path='total-count')
    def total_dossiers(self,request):
        total = Dossier.objects.count()
        tatal_assgin = EtatAvancement.objects.filter(is_active=True).count()
        total_par_etat = EtatAvancement.objects.filter(is_active=True).aggregate(
            total_assign = Count(
                "dossier",
                filter=Q(status="ASSIGN"),
                distinct=True
            ),


            total_in_processing = Count(
                "dossier",
                filter=Q(status="IN_PROCESSING"),
                distinct=True
            ),
            total_processed = Count(
                "dossier",
                filter=Q(status="PROCESSED"),
                distinct=True
            ),
            total_validated = Count(
                "dossier",
                filter=Q(status="VALIDATED"),
                distinct=True
            ),
            total_reject = Count(
                "dossier",
                filter=Q(status="REJECT"),
                distinct=True
            ),
            total_in_validation = Count(
                "dossier",
                filter=Q(status="IN_VALIDATION"),
                distinct=True
            ),
            total_archived = Count(
                "dossier",
                filter=Q(status="ARCHIVED"),
                distinct=True
            ),
            total_return = Count(
                "dossier",
                filter=Q(status="RETURN"),
                distinct=True
            ),
        )
        dossier_non_assigne = total- tatal_assgin
        return Response({'total_dossiers': total,'total_par_etat': total_par_etat,'dossier_non_assigne': dossier_non_assigne })

    @action(detail=False, methods=['get'])
    def classification_niveau_priorite(self,request):
        # count pour chaque niveau de priorite  si il n ya pas des dossiers avec un niveau de priorite specifique on affiche 0 a condition que tous les niveau soit afficher la class pour tous les niveau est 
        # class NiveauPriorite(models.TextChoices):
        #   normale = "NORMALE"
        #    urgente = "URGENTE"
        #    tres_urgente = "TRES_URGENTE"
        qs=self.get_queryset()
        stats=qs.values('niveau_priorite').annotate(total=Count('id'))
        return Response({
            "total_dossiers": qs.count(),
            "resultats": stats
        })
    
    
    @action(detail=False, methods=['get'])
    def recent_dossiers(self, request):
        dossiers = Dossier.objects.filter(is_deleted=False).order_by('-date_creation')[:5]
        serializer = self.get_serializer(dossiers, many=True)
        return Response(serializer.data)


    

    @action(detail=False, methods=["get"], url_path="statistiques_dossier_traite")
    def statistiques_dossier_traite(self, request):
        periode = request.query_params.get("periode")
        now = timezone.now()

        # -------------------------
        # CONFIGURATION
        # -------------------------

        if periode == "jour":
            trunc = TruncDay
            periods = [
                (now - timedelta(days=i)).date()
                for i in range(11, -1, -1)
            ]

        elif periode == "semaine":
            trunc = TruncWeek
            periods = []
            for i in range(11, -1, -1):
                date = now - timedelta(weeks=i)
                monday = (date - timedelta(days=date.weekday())).date()
                periods.append(monday)

        elif periode == "mois":
            trunc = TruncMonth
            periods = []
            for i in range(11, -1, -1):
                year = now.year
                month = now.month - i
                while month <= 0:
                    month += 12
                    year -= 1
                periods.append(timezone.datetime(year, month, 1).date())

        elif periode == "annee":
            trunc = TruncYear
            periods = [
                timezone.datetime(now.year - i, 1, 1).date()
                for i in range(11, -1, -1)
            ]

        else:
            return Response({"error": "Période invalide"}, status=400)

        date_from = periods[0]

        # -------------------------
        # QUERY
        # -------------------------

        queryset = (
            EtatAvancement.objects
            .filter(is_active=True, status=EtatAvancement.Status.processed,created_at__date__gte=date_from)
            .annotate(period=trunc("created_at"))
            .values("period")
            .annotate(count=Count("id"))
        )

        db_data = {
            item["period"].date(): item["count"]
            for item in queryset
        }

        # -------------------------
        # ZERO FILL
        # -------------------------

        result = []

        for period in periods:
            result.append({
                "period": period,
                "count": db_data.get(period, 0)
            })

        return Response(result)


    @action(detail=False, methods=["get"], url_path="stats")
    def count_dossiers(self, request):
        queryset = self.filter_queryset(self.get_queryset())

        total = queryset.count()

        assigne = queryset.filter(
            dossier__is_active=True,
            dossier__user_actual__isnull=False
        ).distinct().count()

        non_assigne = queryset.filter(
            dossier__isnull=True,
        ).distinct().count()

        nouveau = queryset.exclude(
            dossier__is_active=True
        ).distinct().count()

        return Response({
            "total_dossiers": total,
            "dossiers_assignes": assigne,
            "dossiers_non_assignes": non_assigne,
            "dossiers_nouveaux": nouveau,
        })
    
     
  



# class EtatViewSet(viewsets.ModelViewSet):
#     serializer_class= EtatSerializer
#     queryset= EtatAvancement.objects.all() 


   



     
