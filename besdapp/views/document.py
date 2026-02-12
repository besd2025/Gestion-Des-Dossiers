from rest_framework import viewsets
from ..models.document import Document
from besdapp.serializer import DocumentSerializer

class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer