"""Pessoa Tests."""

# Importações externas
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

# Importações internas
from pessoa.models import Pessoa


class PessoaViewsTestCase(TestCase):
    """Testes para View de Pessoa."""

    def setUp(self):
        """Set Up."""
        self.client = APIClient()
        self.pessoa_data = {
            'nome': 'Test Nome',
            'idade': 25,
            'email': 'test@example.com',
        }
        self.pessoa = Pessoa.objects.create(**self.pessoa_data)

    def test_get_pessoa(self):
        """Testa o retrieve de pessoa."""
        response = self.client.get(reverse('pessoa_detail', args=[self.pessoa.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['nome'], self.pessoa_data['nome'])

    def test_list_pessoas(self):
        """Testa listagem de pessoas."""
        response = self.client.get(reverse('pessoas'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.json()) > 0)

    def test_create_pessoa_with_existing_email(self):
        """Testa o tentativa de criacao de pessoa com email ja cadastrado."""
        existing_email = self.pessoa_data['email']
        new_data = {
            'nome': 'New Nome',
            'idade': 30,
            'email': existing_email,
        }
        response = self.client.post(reverse('pessoas'), new_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(),
            {'email': ['pessoa with this email already exists.']}

        )

    def test_create_pessoa(self):
        """Testa o criacao de pessoa."""
        new_data = {
            'nome': 'New Nome',
            'idade': 30,
            'email': 'new@example.com',
        }
        response = self.client.post(reverse('pessoas'), new_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['nome'], new_data['nome'])

    def test_update_pessoa(self):
        """Testa o atualizacao de dados de uma pessoa."""
        updated_data = {
            'nome': 'Updated Nome',
            'idade': 28,
        }
        response = self.client.put(
            reverse('pessoa_detail', args=[self.pessoa.pk]),
            updated_data,
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['nome'], updated_data['nome'])

    def test_delete_pessoa(self):
        """Testa o exclusao de uma pessoa."""
        response = self.client.delete(reverse('pessoa_detail', args=[self.pessoa.pk]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
