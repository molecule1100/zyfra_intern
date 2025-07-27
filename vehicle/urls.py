from django.urls import path
from . import views

urlpatterns = [
    path('vehicle_type_create/', views.create_vehicle_type, name='vehicle_type_create'),
    path('vehicle_type_read_update/<int:pk>/', views.read_update_vehicle_type, name='vehicle_type_read_update'),
    path('vehicle_type_list_delete/', views.list_delete_vehicle_type, name='vehicle_type_list_delete'),
    path('vehicle_create/', views.create_vehicle, name='vehicle_create'),
    path('vehicle_read/<int:pk>/', views.read_vehicle, name='vehicle_read'),
    path('vehicle_list_delete/', views.list_delete_vehicle, name='vehicle_list_delete'),
    path('vehicle_update/<int:pk>/', views.update_vehicle, name='vehicle_update'),
]
