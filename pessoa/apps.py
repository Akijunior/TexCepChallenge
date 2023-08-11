"""Pessoa apps."""

# Importações externas
from django.apps import AppConfig


class PessoaConfig(AppConfig):
    """Pessoa Config."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pessoa'
