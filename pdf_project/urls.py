"""
URL configuration for pdf_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
# from django.urls import path

# urlpatterns = [
#     path('admin/', admin.site.urls),
# ]
from django.contrib import admin
from django.urls import path
from pdfapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user_details_form/', views.user_details_form, name='user_details_form'),
    path('direct_deposit_form/', views.direct_deposit_form, name='direct_deposit_form'),
    path('contractor_agreement_form/', views.contractor_agreement_form, name='contractor_agreement_form'),
    path('commission_agreement_form/', views.commission_agreement_form, name='commission_agreement_form'),
    path('success/', views.success, name='success'),
]
