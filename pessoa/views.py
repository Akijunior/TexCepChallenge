"""Pessoa Views."""

# Importacoes externas.
from typing import Union
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.request import Request
from django.http.response import JsonResponse

# Importacoes internas.
from pessoa.models import Pessoa
from pessoa.serializers import PessoaSerializer, PessoaUpdateSerializer


def get_pessoa(pk: str) -> Union[Pessoa, JsonResponse]:
    """Tenta buscar um pessoa pelo pk e lanca uma excecao caso não encontre.

    :param pk: Primary Key do pessoa a ser procurado.

    :return: Objeto de pessoa encontrado ou um json em caso de falha.

    """
    try:
        pessoa = Pessoa.objects.get(pk=pk)
    except Pessoa.DoesNotExist:
        return JsonResponse(
            {'message': 'A pessoa procurada não existe na base atual.'},
            status=status.HTTP_404_NOT_FOUND,
        )
    return pessoa


@api_view(['GET', 'POST', 'DELETE'])
def pessoa_list(request: Request) -> JsonResponse:
    """Lista pessoas presentes na base atualmente.

    :param request: Objeto de request.

    :return: Informacoes sobre o resultado do processo chamado.
    """
    if request.method == 'GET':
        pessoas = Pessoa.objects.all()
        filtros = {key: value[0] for key, value in dict(request.GET).items()}

        if filtros:
            pessoas = pessoas.filter(**filtros)

        pessoas_serializer = PessoaSerializer(pessoas, many=True)
        return JsonResponse(pessoas_serializer.data, safe=False)

    elif request.method == 'POST':
        pessoa_data = JSONParser().parse(request)
        pessoa_serializer = PessoaSerializer(data=pessoa_data)
        if pessoa_serializer.is_valid():
            pessoa_serializer.save()
            return JsonResponse(pessoa_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(pessoa_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        count = Pessoa.objects.all().delete()
        return JsonResponse(
            {'message': f'{count[0]} Pessoa(s) deletada(s) com sucesso!'},
            status=status.HTTP_204_NO_CONTENT,
        )


@api_view(['GET', 'PUT', 'DELETE'])
def pessoa_detail(request: Request, pk: str) -> JsonResponse:
    """Procura pessoa por pk (id).

    :param request: Objeto de request.
    :param pk: Primary Key do pessoa a ser procurado.

    :return: Informacoes sobre o resultado do processo chamado.
    """
    pessoa = get_pessoa(pk)

    if not isinstance(pessoa, Pessoa):
        return pessoa

    if request.method == 'GET':
        pessoa_serializer = PessoaSerializer(pessoa)
        return JsonResponse(pessoa_serializer.data)

    elif request.method == 'PUT':
        pessoa_data = JSONParser().parse(request)
        pessoa_serializer = PessoaUpdateSerializer(pessoa, data=pessoa_data)
        if pessoa_serializer.is_valid():
            pessoa_serializer.save()
            return JsonResponse(pessoa_serializer.data)

        return JsonResponse(pessoa_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        pessoa.delete()
        return JsonResponse(
            {'message': 'Pessoa deletado com sucesso!'},
            status=status.HTTP_204_NO_CONTENT,
        )

def resposta_de_pessoa_unico(pessoa: Pessoa) -> JsonResponse:
    """Retorna o Json Response para casos de Pessoa unico.

    :param pessoa: Pessoa a ser utilizado no serializer.

    :return: Pessoa montado no serializer.
    """
    pessoa_serializer = PessoaSerializer(pessoa)
    resposta = {'sucesso': True, 'pessoa': pessoa_serializer.data}

    return JsonResponse(resposta, status=status.HTTP_200_OK)


def cria_pessoa(dados_de_pessoa: dict) -> Pessoa:
    """Cria um novo pessoa na base.

    :param dados_de_pessoa: Dados a serem utilizados na criacao de pessoa.

    :return: Objeto de pessoa criado.
    """
    pessoa = Pessoa(**dados_de_pessoa)
    pessoa.save()

    return pessoa
