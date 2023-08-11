"""CEP Views."""

# Importacoes externas.
import re
from typing import Union
from xml.etree import ElementTree
import requests
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.request import Request
from django.http.response import JsonResponse

# Importacoes internas.
from cep.models import Endereco
from cep.serializers import EnderecoSerializer, EnderecoUpdateSerializer


def get_endereco(pk: str) -> Union[Endereco, JsonResponse]:
    """Tenta buscar um endereco pelo pk e lanca uma excecao caso não encontre.

    :param pk: Primary Key do endereco a ser procurado.

    :return: Objeto de endereco encontrado ou um json em caso de falha.

    """
    try:
        endereco = Endereco.objects.get(pk=pk)
    except Endereco.DoesNotExist:
        return JsonResponse(
            {'message': 'O endereço procurado não existe na base atual.'},
            status=status.HTTP_404_NOT_FOUND,
        )
    return endereco


@api_view(['GET', 'POST', 'DELETE'])
def endereco_list(request: Request) -> JsonResponse:
    """Lista enderecos presentes na base atualmente.

    :param request: Objeto de request.

    :return: Informacoes sobre o resultado do processo chamado.
    """
    if request.method == 'GET':
        enderecos = Endereco.objects.all()
        filtros = {key: value[0] for key, value in dict(request.GET).items()}

        if filtros:
            enderecos = enderecos.filter(**filtros)

        enderecos_serializer = EnderecoSerializer(enderecos, many=True)
        return JsonResponse(enderecos_serializer.data, safe=False)

    elif request.method == 'POST':
        endereco_data = JSONParser().parse(request)
        endereco_serializer = EnderecoSerializer(data=endereco_data)
        if endereco_serializer.is_valid():
            endereco_serializer.save()
            return JsonResponse(endereco_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(endereco_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        count = Endereco.objects.all().delete()
        return JsonResponse(
            {'message': f'{count[0]} Endereco(s) deletado(s) com sucesso!'},
            status=status.HTTP_204_NO_CONTENT,
        )


@api_view(['GET', 'PUT', 'DELETE'])
def endereco_detail(request: Request, pk: str) -> JsonResponse:
    """Procura endereco por pk (id).

    :param request: Objeto de request.
    :param pk: Primary Key do endereco a ser procurado.

    :return: Informacoes sobre o resultado do processo chamado.
    """
    endereco = get_endereco(pk)

    if not isinstance(endereco, Endereco):
        return endereco

    if request.method == 'GET':
        endereco_serializer = EnderecoSerializer(endereco)
        return JsonResponse(endereco_serializer.data)

    elif request.method == 'PUT':
        endereco_data = JSONParser().parse(request)
        endereco_serializer = EnderecoUpdateSerializer(endereco, data=endereco_data)
        if endereco_serializer.is_valid():
            endereco_serializer.save()
            return JsonResponse(endereco_serializer.data)
        return JsonResponse(endereco_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        endereco.delete()
        return JsonResponse(
            {'message': 'Endereco deletado com sucesso!'},
            status=status.HTTP_204_NO_CONTENT,
        )


@api_view(['GET'])
def busca_endereco_por_cep(request: Request, cep: str) -> JsonResponse:
    """Busca endereco por CEP.

    Caso não seja encontrado nenhum endereco de CEP igual ao em questão, uma busca será realizada
    em <https://viacep.com.br/ws/< CEP>/xml/> para buscar por dados para a criacao de um novo
    endereco com essas informacoes, e caso o CEP em si seja invalido sera retornado um JsonResponse
    relatando a falha.

    :param request: Objeto de request.
    :param cep: CEP que se deseja procurar informacoes.

    :return: Resposta da operacao acerca do CEP enviado.
    """
    cep = limpa_cep(cep)
    endereco = Endereco.objects.filter(cep=cep).first()

    if endereco:
        return resposta_de_endereco_unico(endereco)

    url = f'https://viacep.com.br/ws/{cep}/xml/'
    response = requests.get(url)

    if response.status_code != 200:
        return JsonResponse(
            {'message': f'Falha na busca pelo cep {cep}!'},
            status=response.status_code,
        )
    xml_content = response.content.decode('utf-8')
    dados_endereco = monta_objeto_endereco(xml_content)
    endereco = cria_endereco(dados_endereco)

    return resposta_de_endereco_unico(endereco)


def resposta_de_endereco_unico(endereco: Endereco) -> JsonResponse:
    """Retorna o Json Response para casos de Endereco unico.

    :param endereco: Endereco a ser utilizado no serializer.

    :return: Endereco montado no serializer.
    """
    endereco_serializer = EnderecoSerializer(endereco)
    resposta = {'sucesso': True, 'endereco': endereco_serializer.data}

    return JsonResponse(resposta, status=status.HTTP_200_OK)


def cria_endereco(dados_de_endereco: dict) -> Endereco:
    """Cria um novo endereco na base.

    :param dados_de_endereco: Dados a serem utilizados na criacao de endereco.

    :return: Objeto de endereco criado.
    """
    endereco = Endereco(**dados_de_endereco)
    endereco.save()

    return endereco


def monta_objeto_endereco(xml_content: str) -> dict:
    """Prepara um dicionario com as informacoes para criacao de uma instancia de endereco.

    :param xml_content: Conteudo xml de onde extrair as informacoes de endereco.

    :return: Objeto de endereco montado para criacao.
    """
    root = ElementTree.fromstring(xml_content)

    return {
        'bairro': root.find('bairro').text,
        'cidade': root.find('localidade').text,
        'uf': root.find('uf').text,
        'cep': limpa_cep(root.find('cep').text),
        'logradouro': root.find('logradouro').text,
        'complemento': root.find('complemento').text,
    }


def limpa_cep(cep: str) -> str:
    """Remover espacos, pontos e tracos e manter apenas os numeros.

    :param cep: CEP a ser limpo.

    :return: CEP Limpo.
    """
    return re.sub(r'[\s.-]', '', cep)
