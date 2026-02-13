import django_filters
from besdapp.models import Dossier

class DossierFilter(django_filters.FilterSet):
    # Filtrer par date exacte (ignore l'heure)
    date_creation = django_filters.DateFilter(
        field_name="date_creation",
        lookup_expr='date'  # permet de comparer uniquement la date
    )

    # Filtrer par date supérieure ou égale
    date_creation_after = django_filters.DateFilter(
        field_name="date_creation",
        lookup_expr="date__gte"  # comparer uniquement la date
    )

    # Filtrer par date inférieure ou égale
    date_creation_before = django_filters.DateFilter(
        field_name="date_creation",
        lookup_expr="date__lte"  # comparer uniquement la date
    )

    class Meta:
        model = Dossier
        fields = ['date_creation', 'date_creation_after', 'date_creation_before']
