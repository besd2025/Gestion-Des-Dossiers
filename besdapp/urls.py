from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.bureau import BureauViewSet
from .views.cellule import CelluleViewSet
from .views.roles import RoleViewSet
from .views.authentification import CustomUserViewSet
from .views.dossier import DossierViewSet
from .views.etatavancement import EtatViewSet
from .views.document import DocumentViewSet
from .views.notification import NotificationViewSet,MessageViewSet

router = DefaultRouter()
router.register(r'bureaux', BureauViewSet)
router.register(r'Cellule', CelluleViewSet)
router.register(r'roles', RoleViewSet, basename='role')
router.register(r'utilisateurs', CustomUserViewSet)
router.register(r'dossiers', DossierViewSet, basename='dossier')
router.register(r'etatavancement', EtatViewSet, basename='etat_avancement')
router.register(r'documents', DocumentViewSet)
router.register(r'notifications', NotificationViewSet, basename='notification')
router.register(r'message', MessageViewSet, basename='msg')

# # =========================
 # URLPATTERNS
# # =========================
urlpatterns = [
#     # Route pour l'inscription
#     # path('register/', RegisterView.as_view(), name='auth_register'),
    
#     # Routes pour le profil et la gestion (CRUD)
     path('', include(router.urls)),
     path('api/login', include('rest_framework.urls'))
]

# Bureaux	/api/bureaux/
# Services	/api/services/
# Rôles	/api/roles/
# Utilisateurs	/api/utilisateurs/