from django.urls import path

from items.views import (
    QuotationVisitListCreateView,
    QuotationVisitRetrieveUpdateDestroyView,
)


urlpatterns = [
    path("", QuotationVisitListCreateView.as_view(), name="quotation_visits"),
    path(
        "<int:pk>",
        QuotationVisitRetrieveUpdateDestroyView.as_view(),
        name="quotation_visit",
    ),
]
