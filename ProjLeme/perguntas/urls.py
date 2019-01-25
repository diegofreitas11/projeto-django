from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('envio/', views.envio,name='envio')
]