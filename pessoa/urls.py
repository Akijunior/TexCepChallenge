"""Urls para Pessoas."""

# Importações externas
from django.urls import path

# Importações internas
from pessoa import views

urlpatterns = [
    path('', views.pessoa_list, name='pessoas'),
    path('<pk>', views.pessoa_detail, name='pessoa_detail'),
]
