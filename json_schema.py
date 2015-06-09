# -*- encoding: utf-8 -*-
u"""
Lib para comparação, teste e checagem de jsons.

Exemplo de uso:
In [1]: import json_schema

In [2]: um_json = '''{"chave_list": [1, 2],
                      "chave_dict": {"chave": "valor"},
                      "chave_int": 1,
                      "chave_float": 1.2,
                      "chave_string": "1"}'''

In [3]: esquema = json_schema.dumps(um_json)

In [4]: print esquema
{"chave_list": ["int", "..."], "chave_dict": {"chave": "string"}, "chave_int": "int", "chave_float": "float", "chave_string": "string"}

In [5]: js = json_schema.loads(esquema)

In [6]: js
Out[6]: <json_schema.JsonSchema at 0x1064f0f50>

In [7]: js == um_json
Out[7]: True
"""

import json
import re
from validators import (StringValidator, IntValidator, FloatValidator,
                        UrlValidator, BooleanValidator, RegexValidator)


def loads(schema):
    u"""Recebe uma string de schema e retorna um JsonSchema object."""
    return JsonSchema(schema)


def dumps(j):
    u"""Recebe um json e retorna um schema."""
    def montador(valor):
        if isinstance(valor, dict):
            retorno = {}
            for c, v in valor.items():
                retorno[c] = montador(v)
            return retorno
        elif isinstance(valor, list) or isinstance(valor, tuple):
            retorno = []
            for i in valor:
                retorno.append(montador(i))
            # Checa se é uma lista de tamanho flexivel
            if all([r == retorno[0] for r in retorno]):
                retorno = [retorno[0], "..."]
            return retorno
        elif isinstance(valor, str) or isinstance(valor, unicode):
            return "string"
        elif isinstance(valor, bool):
            return "bool"
        elif isinstance(valor, int):
            return "int"
        elif isinstance(valor, float):
            return "float"
        else:
            raise Exception(u"O json nao parece ser valido")

    data = json.loads(j)
    return json.dumps(montador(data))


def match(j, schema):
    u"""Compara um json (j) com um schema (schema)."""
    js = JsonSchema(schema)
    return js == j


class JsonSchema(object):

    u"""Objeto usado para comparações e testes de schemas."""

    validators = (StringValidator, IntValidator, FloatValidator,
                  UrlValidator, BooleanValidator, RegexValidator)

    def __init__(self, schema):
        u"""Ainda não sei."""
        self.schema = schema
        self.schema_dict = json.loads(schema)
        if not JsonSchema.validar_schema(self.schema_dict):
            raise Exception(u"O schema nao parece ser valido")

    def __eq__(self, j):
        u"""Compara um json com este JsonSchema."""
        estrutura = json.loads(j)
        return JsonSchema.comparar(estrutura, self.schema_dict)

    def loads(self, schema):
        u"""Este quem de fato carrega o schema."""
        self.schema_dict = json.loads(schema)

    @classmethod
    def validar_schema(cls, schema):
        u"""Valida se o formato do schema é um formato correto."""
        if isinstance(schema, dict):
            for chave, valor in schema.items():
                if not cls.validar_schema(valor):
                    return False
            return True
        elif isinstance(schema, list):
            for item in schema:
                if not cls.validar_schema(item):
                    return False
            return True
        elif isinstance(schema, str) or isinstance(schema, unicode):
            if any([v.schema_lookout(schema)
                    for v in cls.validators] + [schema == "..."]):
                return True
            return False
        else:
            return False

    @classmethod
    def comparar(cls, item, item_schema):
        u"""Faz a comparação recursiva."""
        # Se for um dicionário
        if isinstance(item_schema, dict):
            for chave, valor_schema in item_schema.items():
                valor = item.get(chave)
                if valor is None:
                    return False
                if not cls.comparar(valor, valor_schema):
                    return False
            return True
        # Se for uma lista
        elif isinstance(item_schema, list):
            # Se for uma lista de tamalho variável
            if len(item_schema) == 2 and item_schema[1] == "...":
                item_schema_repetido = item_schema[0]
                for item_lista in item:
                    if not cls.comparar(item_lista, item_schema_repetido):
                        return False
                return True
            # Se for uma lista de tamanho fixo
            if not len(item_schema) == len(item):
                return False
            for item_lista, item_schema_list in zip(item, item_schema):
                if not cls.comparar(item_lista, item_schema_list):
                    return False
            return True
        # Se for uma string ou unicode
        elif isinstance(item_schema, str) or isinstance(item_schema, unicode):
            for validator in cls.validators:
                if validator.schema_lookout(item_schema):
                    return validator.validator(item, item_schema)
