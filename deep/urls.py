from django.urls import path
from . import views

urlpatterns = [
    # User CRUD operations
    path('', views.user_list, name='user_list'),
    path('users/create/', views.user_create, name='user_create'),
    path('users/<int:pk>/update/', views.user_update, name='user_update'),
    path('users/<int:pk>/delete/', views.user_delete, name='user_delete'),
    
    # Poster management
    path('posters/', views.poster_list, name='poster_list'),
    path('posters/create/', views.poster_create, name='poster_create'),
    path('vip/posters/', views.vip_posters, name='vip_posters'),
    path('share/poster/<int:poster_id>/', views.share_poster, name='share_poster'),
    
 
]