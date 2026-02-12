from rest_framework import viewsets
from besdapp.models import Cellule
from besdapp.serializer import CelluleSerializer


class CelluleViewSet(viewsets.ModelViewSet):
    queryset = Cellule.objects.all()
    serializer_class = CelluleSerializer