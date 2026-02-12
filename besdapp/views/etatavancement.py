from rest_framework import viewsets
from besdapp.models.dossier import EtatAvancement
from besdapp.serializer import EtatSerializer
from rest_framework.response import Response
from rest_framework.decorators import action



class EtatViewSet(viewsets.ModelViewSet):
    serializer_class= EtatSerializer
    queryset= EtatAvancement.objects.all()
    
    
    @action(detail=True, methods=['get'])
    def ListEtatavance(self, request,pk=None):
        etatavancement= EtatAvancement.objects.filter(is_active=True)
        etatser=EtatSerializer(etatavancement, many=True)
        return Response(etatser.data)