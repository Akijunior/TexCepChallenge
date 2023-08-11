"""Cep Tests."""

# Importações externas
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

# Importações internas
from cep.models import Endereco
from cep.views import limpa_cep


class CepViewsTestCase(TestCase):
    """Testes para View de CEP."""

    def setUp(self):
        """set Up."""
        self.client = APIClient()
        self.endereco_data = {
            'bairro': 'Test Bairro',
            'cidade': 'Test Cidade',
            'uf': 'TE',
            'cep': '12345678',
            'logradouro': 'Test Logradouro',
            'complemento': 'Test Complemento',
        }
        self.endereco = Endereco.objects.create(**self.endereco_data)

    def test_get_endereco(self):
        """Testa o retrieve de endereco."""
        response = self.client.get(reverse('endereco_detail', args=[self.endereco.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['bairro'], self.endereco_data['bairro'])

    def test_atualiza_endereco(self):
        """Testa o update de endereco."""
        novos_dados = {
            'bairro': 'Updated Bairro',
            'cidade': 'Updated Cidade',
            'logradouro': 'Updated Logradouro',
            'complemento': 'Updated Complemento',
        }
        response = self.client.put(
            reverse('endereco_detail', args=[self.endereco.pk]),
            novos_dados,
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['bairro'], novos_dados['bairro'])

    def test_endereco_list(self):
        """Testa listagem de enderecos."""
        response = self.client.get(reverse('enderecos'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_endereco_delete(self):
        """Testa exclusao de todos enderecos."""
        response = self.client.delete(reverse('enderecos'))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Endereco.objects.count(), 0)

    def test_cria_novo_endereco(self):
        """Testa criacao de endereco quando enviado um cep diferente dos existentes na base."""
        response = self.client.get(reverse('endereco_cep', args=['64082-550']))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Endereco.objects.count(), 2)

    def test_nao_cria_novo_endereco(self):
        """Testa criacao de endereco quando enviado um cep igual a outro ja existente na base."""
        response = self.client.get(reverse('endereco_cep', args=['12345678']))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Endereco.objects.count(), 1)

    def test_limpa_cep(self):
        """Testa funcao de limpeza de chars especiais de uma string de CEP."""
        cep_limpo = limpa_cep('123.456-78')
        self.assertEqual(cep_limpo, '12345678')
