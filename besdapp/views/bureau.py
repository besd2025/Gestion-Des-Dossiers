from rest_framework import viewsets, permissions
from besdapp.models import Bureau
from besdapp.serializer import BureauSerializer

class BureauViewSet(viewsets.ModelViewSet):
    queryset = Bureau.objects.all()
    serializer_class = BureauSerializer
    # permission_classes = [permissions.IsAuthenticated]