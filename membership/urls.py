from django.urls import path
from .views import (
    MembershipListView, MembershipCreateView, MembershipUpdateView,
    MembershipDeleteView, MembershipDetailView
)

urlpatterns = [
    path('', MembershipListView.as_view(), name='membership_list'),
    path('add/', MembershipCreateView.as_view(), name='membership_add'),
    path('<int:pk>/edit/', MembershipUpdateView.as_view(), name='membership_edit'),
    path('<int:pk>/delete/', MembershipDeleteView.as_view(), name='membership_delete'),
    path('<int:pk>/', MembershipDetailView.as_view(), name='membership_detail'),
]
