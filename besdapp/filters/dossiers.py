import django_filters
from django.db.models import Q
from besdapp.models import Dossier, EtatAvancement


class DossierFilter(django_filters.FilterSet):

    # =========================
    # 🔎 Filtres simples
    # =========================
    reference = django_filters.CharFilter(
        field_name="reference",
        lookup_expr="icontains"
    )

    objet = django_filters.CharFilter(
        field_name="objet",
        lookup_expr="icontains"
    )

    niveau_priorite = django_filters.NumberFilter(
        field_name="niveau_priorite"
    )

    # =========================
    # 📅 Filtres Date
    # =========================

    # Date exacte (ignore l'heure)
    date_creation = django_filters.DateFilter(
        field_name="date_creation",
        lookup_expr="date"
    )

    # Date >=
    date_creation_after = django_filters.DateFilter(
        field_name="date_creation",
        lookup_expr="date__gte"
    )

    # Date <=
    date_creation_before = django_filters.DateFilter(
        field_name="date_creation",
        lookup_expr="date__lte"
    )

    # =========================
    # 📌 Statut dossier
    # =========================

    assigne = django_filters.BooleanFilter(method="filter_assigne")
    non_assigne = django_filters.BooleanFilter(method="filter_non_assigne")
    nouveau = django_filters.BooleanFilter(method="filter_nouveau")

    class Meta:
        model = Dossier
        fields = [
            "reference",
            "objet",
            "niveau_priorite",
            "date_creation",
            "date_creation_after",
            "date_creation_before",
            "assigne",
            "non_assigne",
            "nouveau",
        ]

    # =========================
    # 🎯 Filtres personnalisés
    # =========================

    def filter_assigne(self, queryset, name, value):
        if value:
            return queryset.filter(
                dossier__is_active=True,
                dossier__user_actual__isnull=False
            ).distinct()
        return queryset

    def filter_non_assigne(self, queryset, name, value):
        if value:
            return queryset.filter(
                dossier__isnull=True,
            ).distinct()
        return queryset

    def filter_nouveau(self, queryset, name, value):
        if value:
            return queryset.exclude(
                dossier__is_active=True
            ).distinct()
        return queryset