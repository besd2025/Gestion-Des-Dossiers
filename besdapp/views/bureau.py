from rest_framework import viewsets, permissions
from besdapp.models import Bureau,Cellule,roles,CustomUser
from besdapp.serializer import BureauSerializer,CelluleSerializer,CustomUserSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

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
    
    
    # @action(detail=True, methods=['get'])
    # def tUserBurRole(self, request,pk=None):
    #     Bureau=roles.objects.filter()
        
        
    
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
