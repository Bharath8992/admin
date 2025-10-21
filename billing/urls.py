from django.urls import path
from . import views

app_name = 'billing'

urlpatterns = [
    path('', views.billing_view, name='billing'),
    path('bill-success/<int:bill_id>/', views.bill_success, name='bill_success'),
    path('download-pdf/<int:bill_id>/', views.download_pdf, name='download_pdf'),
    path('share-whatsapp/<int:bill_id>/', views.share_whatsapp, name='share_whatsapp'),
    path('bill-history/', views.bill_history, name='bill_history'),
    path('bill-detail/<int:bill_id>/', views.bill_detail, name='bill_detail'),
]