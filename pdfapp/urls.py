from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_details, name='user_details'),
    path('records_form/', views.records_form, name='records_form'),
    path('log_in/', views.log_in, name='log_in'),
    path('download_file/', views.download_file, name='download_file'),
    path('contractor-agreement/', views.contractor_agreement_form, name='contractor_agreement_form'),
    path('commission-agreement/', views.commission_agreement_form, name='commission_agreement_form'),
    path('success/', views.success, name='success'),
    path('success2/' views.success, name='success2'),
    path('list_forms/' views.success, name='list_forms'),
]

