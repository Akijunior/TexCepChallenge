"""Pessoa models."""

# Importações externas
from django.db import models


class Pessoa(models.Model):
    """Modelo para pessoa."""

    nome = models.CharField(max_length=70)
    idade = models.IntegerField()
    email = models.EmailField(max_length=90, unique=True)
    endereco = models.ForeignKey(
        'cep.Endereco',
        on_delete=models.CASCADE,
        null=True,
        related_name='residentes_atuais',
    )

    def __str__(self):
        return self.nome
