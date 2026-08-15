from django.urls import path
from . import views

app_name = 'resources'

urlpatterns = [
    path('', views.resources_view, name='resources_list'),
    path('add/', views.add_resource, name='add_resource'),
    path('<int:resource_id>/delete/', views.delete_resource, name='delete_resource'),
]