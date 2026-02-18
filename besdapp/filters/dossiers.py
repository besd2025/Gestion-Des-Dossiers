import django_filters
from besdapp.models import Dossier

class DossierFilter(django_filters.FilterSet):
    # Filtrer par date exacte (ignore l'heure)
    date_creation = django_filters.DateFilter(
        field_name="date_creation",
        lookup_expr='date'  # permet de comparer uniquement la date
    )

    # Filtrer par date supérieure ou égale
    
    django_filters.DateFilter(
        field_name="date_creation",
        lookup_expr="date__gte" 
    )

    # Filtrer par date inférieure ou égale
    date_creation_before = django_filters.DateFilter(
        field_name="date_creation",
        lookup_expr="date__lte" 
    )

    class Meta:
        model = Dossier
        fields = ['date_creation']
