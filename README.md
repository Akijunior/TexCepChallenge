# Tex CEP Challenge

Este é um projeto que implementa rotas para manipulação de informações de Pessoas e CEPs. 
Ele fornece uma API para consultar, criar, atualizar e deletar dados relacionados a Pessoas e Endereços.

## Tabela de Conteúdo

- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Instalação](#instalação)
- [Uso](#uso)
- [Rotas](#rotas)
- [Exemplos de Requisições](#exemplos-de-requisições)
- [Contribuição](#contribuição)
- [Licença](#licença)

## Tecnologias Utilizadas

- [Python];
- [Django];
- [Mongo].

## Instalação

1. Clone este repositório: `git clone https://github.com/seu-usuario/seu-repositorio.git`
2. Crie um ambiente virtual: `python -m venv venv`
2. Instale as dependências: `pip install -r requirements.txt`

## Uso

Execute o projeto utilizando o comando: `python manage.py runserver`

## Rotas

### Pessoas

- `GET /api/pessoas`: Retorna a lista de todas as pessoas.
- `GET /api/pessoas/:id`: Retorna os detalhes da pessoa com o ID especificado.
- `POST /api/pessoas`: Cria uma nova pessoa.
- `PUT /api/pessoas/:id`: Atualiza os dados da pessoa com o ID especificado.
- `DELETE /api/pessoas/:id`: Deleta a pessoa com o ID especificado.

### CEPs

- `GET /api/enderecos`: Retorna a lista de todos os endereços.
- `GET /api/enderecos/:id`: Retorna os detalhes do endereço com o ID especificado.
- `POST /api/enderecos/busca_cep/:cep`: Busca por endereços na base com o CEP especificado e caso não encontre realiza 
- uma busca no `https://viacep.com.br/ws/< CEP>/xml/` para obter os dados de endereço associados ao CEP em questão e 
- criar um novo objeto de Endereço na base.
- `PUT /api/enderecos/:id`: Atualiza os dados do endereço com o ID especificado.
- `DELETE /api/enderecos/:id`: Deleta o endereço com o ID especificado.

## Exemplos de Requisições

Aqui estão alguns exemplos de como fazer requisições para as rotas:

**Obter lista de Pessoas:**
```http
GET /api/pessoas
```

**Atualizar Endereço:**
```http
GET /api/enderecos/:id
