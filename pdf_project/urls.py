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
from django.urls import path
from django.contrib import admin
from pdfapp import views

urlpatterns = [
    path('', views.user_details, name='user_details'),
    path('records_form/', views.records_form, name='records_form'),
    path('log_in/', views.log_in, name='log_in'),
    path('download_file/', views.download_file, name='download_file'),
    path('contractor_agreement_form/', views.contractor_agreement_form, name='contractor_agreement_form'),
    path('commission_agreement_form/', views.commission_agreement_form, name='commission_agreement_form'),
    path('success/', views.success, name='success'),
    path('logout/', views.logout_view, name='logout'),  # Use views.logout_view here
    path('register/', views.register, name='register'),
    path('admin/', admin.site.urls),
    path('home/', views.home, name='home'),
    path('success2/', views.success2, name='success2'),
    path('delete_record/', views.delete_record, name='delete_record'),
]

