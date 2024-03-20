from django.urls import path

from items.views import (
    QuotationItemListCreateView,
    QuotationItemRetrieveUpdateDestroyView,
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
    path(
        "<int:quotation_item_pk>/items",
        QuotationItemListCreateView.as_view(),
        name="quotation_visit_items",
    ),
    path(
        "<int:quotation_item_pk>/items/<int:pk>",
        QuotationItemRetrieveUpdateDestroyView.as_view(),
        name="quotation_visit_items",
    ),
]
