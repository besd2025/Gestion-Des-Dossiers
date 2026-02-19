from django.db.models import F , Q
from rest_framework import viewsets, permissions
from besdapp.models import Bureau,Cellule,roles,CustomUser,EtatAvancement
from besdapp.serializer import BureauSerializer,CelluleSerializer,CustomUserSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Q

class BureauViewSet(viewsets.ModelViewSet):
    queryset = Bureau.objects.all()
    serializer_class = BureauSerializer
    # permission_classes = [permissions.IsAuthenticated]
    
    
    # @action(detail=True, methods=['get'])
    # def BureauStas(self, request):
    #     Bureaulist = Bureau.object()
        
        
    @action(detail=True, methods=['get'])
    def cellules(self, request, pk=None):
        bureau = self.get_object()
        # On récupère toutes les cellules liées à ce bureau
        cellules = Cellule.objects.filter(bureau=bureau) 
        serializer = CelluleSerializer(cellules, many=True)
        return Response(serializer.data)
    
    
    @action(detail=True, methods=['get'])
    def compter_cellules(self, request, pk=None):
        bureau = self.get_object()
    # On utilise .count() pour que ce soit ultra rapide au niveau de la base de données
        nbre_cellules = Cellule.objects.count() 
    
        return Response({
        'bureau': bureau.nom_bureau,
        'total_cellules': nbre_cellules
    })
    
    
    @action(detail=True, methods=['get'])
    def All_User_BurRole(self, request,pk=None):
        Alluserburole=CustomUser.objects.filter(Q(user_role__role_bureau__bureau__code_bureau="02")|Q(user_role__role_cellule__cellule__bureau__code_bureau="02")).annotate(nom_du_role=F('user_role__nom_role'),bureau_cellule=F('user_role__role_bureau__bureau__nom_bureau'))
        serializer= CustomUserSerializer(Alluserburole, many=True)
        return Response(serializer.data)

    
    @action(detail=True, methods=['get'])
    def statistiques_dossiers(self, request, pk=None):
        bureau = self.get_object()

        stats_queryset = (
            EtatAvancement.objects
            .filter(
                is_active=True,
                status__in=[
                    EtatAvancement.Status.in_processing,
                    EtatAvancement.Status.processed
                ],
                user_actual__isnull=False,
                user_actual__user_role__role_cellule__cellule__bureau_id=bureau.id
            )
            .values(
                'user_actual__user_role__role_cellule__cellule__id',
                'user_actual__user_role__role_cellule__cellule__nom_cellule',
                'status'
            )
            .annotate(total=Count('dossier', distinct=True))
        )

        statistiques = {}

        for item in stats_queryset:
            cellule_id = item['user_actual__user_role__role_cellule__cellule__id']
            nom_cellule = item['user_actual__user_role__role_cellule__cellule__nom_cellule']

            if cellule_id not in statistiques:
                statistiques[cellule_id] = {
                    "cellule_id": cellule_id,
                    "nom_cellule": nom_cellule,
                    "total_dossiers": 0,
                    "par_status": {
                        "IN_PROCESSING": 0,
                        "PROCESSED": 0
                    }
                }

            statistiques[cellule_id]["par_status"][item["status"]] = item["total"]
            statistiques[cellule_id]["total_dossiers"] += item["total"]

        return Response({
            "bureau_id": bureau.id,
            "nom_bureau": bureau.nom_bureau,
            "statistiques": list(statistiques.values())
        })
    
# @action(detail=False, methods=['get'], url_path='user-bureau')
# def user_bureau(self, request):
#          """Retourne la liste simplifiée : id, nom, prenom, bureau, role"""
#          queryset = CustomUser.objects.filter(user_role__isnull=False,user_role__role_bureau__isnull=False ).annotate(role = F('user_role__nom_role'), bureau_cellule = F('user_role__role_bureau__bureau__nom_bureau'))
#          serializer = CustomUserSerializer(queryset, many=True)
#          return Response(serializer.data)
     
# c = CustomUser.objects.filter(Q(user_role__role_bureau__bureau__code_bureau="02")|Q(user_role__role_cellule__cellule__bureau__code
# _bureau="02" ).annotate(role = F('user_role__nom_role'), bureau_cellule = F('user_role__role_bureau__bureau__nom_bureau'))  
            

# c = CustomUser.objects.filter(Q(user_role__role_bureau__bureau__code_bureau="02")|Q(user_role__role_cellule__cellule__bureau__code
# _bureau="02" ).annotate(role = F('user_role__nom_role'), bureau_cellule = F('user_role__role_bureau__bureau__nom_bureau'))                                                                                         
#     def user_bureau(self, request):
#         """Retourne la liste simplifiée : id, nom, prenom, bureau, role"""
#         queryset = CustomUser.objects.filter(user_role__isnull=False,user_role__role_bureau__isnull=False ).annotate(role = F('user_role__nom_role'), bureau_cellule = F('user_role__role_bureau__bureau__nom_bureau'))
#         serializer = CustomUserSerializer(queryset, many=True)
#         return Response(serializer.data)
