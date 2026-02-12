from rest_framework import viewsets, permissions
from besdapp.models.notification import Notification,Message
from besdapp.serializer import NotificationSerializer,MessageSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # L'utilisateur ne voit que ses notifications à lui
        return Notification.objects.filter(destinataire=self.request.user).order_by('-date_creation')

    def perform_create(self, serializer):
        # Si vous créez une notification manuellement via l'API
        serializer.save(destinataire=self.request.user)

        @action(detail=False, methods=['post'])
        def marquer_tout_lu(self, request):
         self.get_queryset().update(lu=True)
        return Response({'status': 'Toutes les notifications sont marquées comme lues'})
    

class MessageViewSet(viewsets.ModelViewSet):
   serializer_class= MessageSerializer
   queryset= Message.objects.all()