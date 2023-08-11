"""Pessoa Serializer."""

# Importações externas
from rest_framework import serializers

# Importações internas
from cep.models import Endereco
from cep.serializers import EnderecoSerializer
from pessoa.models import Pessoa


class PessoaSerializer(serializers.ModelSerializer):
    """Serializer para criação de Pessoa."""

    endereco = EnderecoSerializer(required=False)

    class Meta:
        """Meta classe para serializer de Pessoa."""

        model = Pessoa
        fields = '__all__'


class PessoaUpdateSerializer(serializers.ModelSerializer):
    """Serializer para atualizacao de Pessoa."""

    nome = serializers.CharField(required=False)
    idade = serializers.IntegerField(required=False)
    email = serializers.EmailField(required=False)
    endereco = serializers.CharField(required=False)

    class Meta:
        """Meta classe para serializer de Pessoa."""

        model = Pessoa
        fields = '__all__'

    def update(self, instance, validated_data):
        """[Overrides ModelSerializer.update]"""
        if 'endereco' in validated_data:
            endereco = Endereco.objects.get(pk=validated_data['endereco'])
            if not endereco:
                raise serializers.ValidationError(
                    f'Endereco com id {validated_data["endereco"]} nao encontrado.'
                )

            validated_data['endereco'] = endereco

        return super().update(instance, validated_data)
