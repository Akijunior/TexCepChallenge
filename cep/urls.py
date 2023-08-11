"""Urls para Endereco."""

# Importações externas
from django.urls import path

# Importações internas
from cep import views

urlpatterns = [
    path('', views.endereco_list, name='enderecos'),
    path('<pk>', views.endereco_detail, name='endereco_detail'),
    path('busca_cep/<cep>', views.busca_endereco_por_cep, name='endereco_cep')
]
