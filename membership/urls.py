from django.urls import path
from . import views

urlpatterns = [
    path('', views.membership_list, name='membership'),
    path('add/', views.membership_create, name='membership_add'),
    path('<int:pk>/edit/', views.membership_edit, name='membership_edit'),
    path('<int:pk>/delete/', views.membership_delete, name='membership_delete'),
]
