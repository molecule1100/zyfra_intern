from django.urls import path
from spare_part.views import SparePartTypeCreateView, SparePartTypeUpdateView, SparePartTypeListView, \
    SparePartTypeDeleteView, SparePartCreateView, SparePartDetailView, SparePartUpdateView, SparePartListView, \
    SparePartDeleteView, AttributeCreateView, AttributeUpdateView, AttributeListView, AttributeDetailView, \
    AttributeDeleteView

urlpatterns = [
    path('spare-part-types/create/', SparePartTypeCreateView.as_view(), name="spare-part-type-create"),
    path('spare-part-types/<int:pk>/', SparePartTypeUpdateView.as_view(), name="spare-part-type-update"),
    path('spare-part-types/', SparePartTypeListView.as_view(), name="spare-part-type-list"),
    path('spare-part-types/<int:pk>/delete/', SparePartTypeDeleteView.as_view(), name="spare-part-type-delete"),
    path('spare-parts/create/', SparePartCreateView.as_view(), name="spare-part-create"),
    path('spare-parts/<int:pk>/', SparePartDetailView.as_view(), name="spare-part-detail"),
    path('spare-parts/<int:pk>/edit/', SparePartUpdateView.as_view(), name="spare-part-update"),
    path('spare-parts/', SparePartListView.as_view(), name="spare-part-list"),
    path('spare-parts/<int:pk>/delete/', SparePartDeleteView.as_view(), name="spare-part-delete"),
    path('attribute/create/', AttributeCreateView.as_view(), name="attribute-create"),
    path('attribute/<int:pk>/edit/', AttributeUpdateView.as_view(), name="attribute-update"),
    path('attribute/', AttributeListView.as_view(), name="attribute-list"),
    path('attribute/<int:pk>/', AttributeDetailView.as_view(), name="attribute-detail"),
    path('attribute/<int:pk>/delete/', AttributeDeleteView.as_view(), name="attribute-delete"),
]
