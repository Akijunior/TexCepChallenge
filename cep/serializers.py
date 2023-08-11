"""CEP Serializer."""

# Importações externas
from rest_framework import serializers

# Importações internas
from cep.models import Endereco


class EnderecoSerializer(serializers.ModelSerializer):
    """Serializer para Endereco."""

    class Meta:
        """Meta classe para serializer de Endereco."""

        model = Endereco
        fields = '__all__'


class EnderecoUpdateSerializer(serializers.ModelSerializer):
    """Serializer para atualizacao de Endereco."""

    cep = serializers.CharField(required=False)
    uf = serializers.CharField(required=False)
    bairro = serializers.CharField(required=False)
    cidade = serializers.CharField(required=False)
    logradouro = serializers.CharField(required=False)
    complemento = serializers.CharField(required=False)

    class Meta:
        """Meta classe para serializer de Endereco."""

        model = Endereco
        fields = '__all__'
