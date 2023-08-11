"""CEP apps."""

# Importações externas
from django.db import models


class Endereco(models.Model):
    """Modelo de endereco para registrar as informacoes obtidas por meio da rota de CEP."""

    cep = models.CharField(max_length=8)
    uf = models.CharField(max_length=30)
    bairro = models.CharField(max_length=50)
    cidade = models.CharField(max_length=40)
    logradouro = models.CharField(max_length=70)
    complemento = models.CharField(max_length=70)
