# -*- encoding: utf-8 -*-
u"""
Lib para comparação, teste e checagem de jsons.

Exemplo de uso:
>>> import json_schema
>>> esquema = '{"chave_list": ["int", "int"],
                "chave_dict": {"chave": "string"},
                "chave_int": "int",
                "chave_float":"float",
                "chave_string": "string"}'
>>> js = json_schema.loads(esquema)
>>> js
<json_schema.JsonSchema at 0x10492b890>
>>> um_json = '{"chave_list": [1, 2],
                "chave_dict": {"chave": "valor"},
                "chave_int": 1,
                "chave_float": 1.2,
                "chave_string": "1"}'
>>> js == um_json
True
"""

import json
import re

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
            return retorno
        elif isinstance(valor, str) or isinstance(valor, unicode):
            return "str"
        elif isinstance(valor, int):
            return "int"
        elif isinstance(valor, float):
            return "float"
        else:
            raise Exception(u"O json nao parece ser valido")

    data = json.loads(j)
    return json.dumps(montador(data))


class JsonSchema(object):

    u"""Objeto usado para comparações e testes de schemas."""

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
            if any([schema.startswith("string"),
                    schema.startswith("int"),
                    schema.startswith("float")]) :
                return True
            print schema
            return False
        else:
            return False

    @classmethod
    def comparar(cls, item, item_schema):
        u"""Faz a comparação recursiva."""
        if isinstance(item_schema, dict):
            for chave, valor_schema in item_schema.items():
                valor = item.get(chave)
                if valor == None:
                    return False
                if not cls.comparar(valor, valor_schema):
                    return False
            return True
        elif isinstance(item_schema, list):
            if not len(item_schema) == len(item):
                return False
            for item_lista, item_schema_list in zip(item, item_schema):
                if not cls.comparar(item_lista, item_schema_list):
                    return False
            return True
        elif isinstance(item_schema, str) or isinstance(item_schema, unicode):
            if item_schema.startswith("string"):
                if isinstance(item, str) or isinstance(item, unicode):
                    if item_schema.startswith("string:"):
                        tamanho = int(item_schema.replace("string:", ""))
                        if len(item) > tamanho:
                            return False
                        return True
                    return True
                return False
            elif item_schema == "int":
                return isinstance(item, int)
            elif item_schema == "float":
                return isinstance(item, float)


exemplo_json = json.dumps({"chave_string": "ab",
                           "chave_list": [1, 2],
                           "chave_int": 1,
                           "chave_dict": {"chave": "valor"},
                           "chave_float": 1.2})

exemplo_schema = '{"chave_list": ["int", "int"], "chave_dict": {"chave": "string"}, "chave_int": "int", "chave_float": "float", "chave_string": "string:1"}'

def teste(exemplo_schema=exemplo_schema, exemplo_json=exemplo_json):
    js = loads(exemplo_schema)
    print JsonSchema.comparar(json.loads(exemplo_json), json.loads(exemplo_schema))

