from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_details_form, name='user_details_form'),
    # path('user-details/', views.user_details_form, name='user_details_form'),
    path('direct-deposit/', views.direct_deposit_form, name='direct_deposit_form'),
    path('contractor-agreement/', views.contractor_agreement_form, name='contractor_agreement_form'),
    path('commission-agreement/', views.commission_agreement_form, name='commission_agreement_form'),
    path('success/', views.success, name='success'),
]

