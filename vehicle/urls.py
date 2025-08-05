from django.urls import path
from .views import VehicleTypeCreateView, VehicleTypeListView, VehicleTypeUpdateView, VehicleTypeDeleteView, \
    VehicleCreateView, VehicleDeleteView, VehicleListView, VehicleUpdateView, VehicleDetailView

urlpatterns = [
    path('vehicle-types/create/', VehicleTypeCreateView.as_view(), name="vehicle-type-create"),
    path('vehicle-types/<int:pk>/', VehicleTypeUpdateView.as_view(), name="vehicle-type-update"),
    path('vehicle-types/', VehicleTypeListView.as_view(), name="vehicle-type-list"),
    path('vehicle-types/<int:pk>/delete/', VehicleTypeDeleteView.as_view(), name="vehicle-type-delete"),
    path('vehicles/create/', VehicleCreateView.as_view(), name="vehicle-create"),
    path('vehicles/<int:pk>/', VehicleDetailView.as_view(), name="vehicle-detail"),
    path('vehicles/<int:pk>/edit/', VehicleUpdateView.as_view(), name="vehicle-update"),
    path('vehicles/', VehicleListView.as_view(), name="vehicle-list"),
    path('vehicles/<int:pk>/delete/', VehicleDeleteView.as_view(), name="vehicle-delete"),
]
