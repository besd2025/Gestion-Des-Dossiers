from rest_framework import viewsets
from besdapp.models.dossier import EtatAvancement
from besdapp.serializer import EtatSerializer
from rest_framework.response import Response
from rest_framework.decorators import action



class EtatViewSet(viewsets.ModelViewSet):
    serializer_class= EtatSerializer
    queryset= EtatAvancement.objects.all()
    
    
    @action(detail=True, methods=['get'])
    def ListEtatavancement(self, request,pk=None):
        etatavancement= EtatAvancement.objects.filter(is_active=True)
        etatser=EtatSerializer(etatavancement, many=True)
        return Response(etatser.data)
  

    # def get_queryset(self):
    #     dossier_id = self.request.query_params.get("dossier")
    #     return EtatAvancement.objects.filter(dossier_id=dossier_id)
    
    @action(detail=False, methods=["get"], url_path="toutes-etapes")
    def toutes_etapes(self, request):
        etats = EtatAvancement.objects.select_related( "dossier","user_actual","previous_state").order_by("dossier", "created_at")
        serializer = EtatSerializer(etats, many=True)
        return Response(serializer.data)
    