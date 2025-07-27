from django.urls import path
from . import views

urlpatterns = [
    path('spare_part_type_create/', views.create_spare_part_type, name='spare_part_type_create'),
    path('spare_part_type_read_update/<int:pk>/', views.read_update_spare_part_type, name='spare_part_type_read_update'),
    path('spare_part_type_list_delete/', views.list_delete_spare_part_type, name='spare_part_type_list_delete'),
    path('spare_part_create/', views.create_spare_part, name='spare_part_create'),
    path('spare_part_read/<int:pk>/', views.read_spare_part, name='spare_part_read'),
    path('spare_part_list_delete/', views.list_delete_spare_part, name='spare_part_list_delete'),
    path('spare_part_update/<int:pk>/', views.update_spare_part, name='spare_part_update'),
    path('attribute_create/', views.create_attribute, name='attribute_create'),
    path('attribute_read_update/<int:pk>/', views.read_update_attribute, name='attribute_read_update'),
    path('attribute_list_delete/', views.list_delete_attribute, name='attribute_list_delete'),
]
