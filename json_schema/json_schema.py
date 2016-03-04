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

try:
    import simplejson as json
except:
    import json
from validators import (StringValidator, IntValidator, FloatValidator,
                        UrlValidator, BooleanValidator, RegexValidator,
                        AnyValidator, NullValidator, PythonValidator,
                        DatetimeValidator, EmptyValidator)


def loads(schema, *args, **kwargs):
    u"""Recebe uma string de schema e retorna um JsonSchema object."""
    return JsonSchema(schema, *args, **kwargs)


def dumps(j, *args, **kwargs):
    u"""Recebe um json e retorna um schema."""
    def merge_schema_tree(a, b):
        if a == b:
            return a
        elif isinstance(a, dict):
            return {c: merge_schema_tree(a[c], b[c]) for c, v in a.items()}
        elif isinstance(a, list) or isinstance(a, tuple):
            if not len(a) == len(b):
                if ("..." in a and b == []):
                    return a
                elif ("..." in b and a == []):
                    return b
                raise Exception('Not Match')
            return [merge_schema_tree(a[i], b[i]) for i in range(len(a))]
        elif isinstance(a, str) or isinstance(a, unicode):
            if a == "any":
                return b
            elif b == "any":
                return a
            elif a == "any|null":
                return "%s|null" % b.replace("|null", "")
            elif b == "any|null":
                return "%s|null" % a.replace("|null", "")
            elif a.endswith("|null") or b.endswith("|null"):
                return a
            raise Exception('Not Match: %s - %s' % (a, b))

    def _match_tree(a, b):
        u"""função recursiva para checar se 'a' e 'b' são iguais."""
        if a == b:
            return True
        elif isinstance(a, dict):
            resultados = [_match_tree(a[c], b[c]) for c, v in a.items()]
            return all(resultados)
        elif isinstance(a, list) or isinstance(a, tuple):
            if not len(a) == len(b):
                if ("..." in a and b == []) or ("..." in b and a == []):
                    return True
                return False
            resultados = [_match_tree(a[i], b[i]) for i in range(len(a))]
            return all(resultados)
        elif isinstance(a, str) or isinstance(a, unicode):
            return a.startswith("any") or b.startswith("any") or a == b

    def montador(valor):
        u"""Função recursiva para montar o schema."""
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
            if retorno:
                # print merge_schema_tree(retorno[1], retorno[0])
                if all([_match_tree(r, retorno[0]) for r in retorno]):
                    final = retorno[0]
                    for r in retorno:
                        final = merge_schema_tree(final, r)
                    retorno = [final, "..."]
            return retorno or ["any|null", "..."]
        elif isinstance(valor, str) or isinstance(valor, unicode):
            return "str"
        elif isinstance(valor, bool):
            return "bool"
        elif isinstance(valor, int):
            return "int"
        elif isinstance(valor, float):
            return "float"
        elif valor is None:
            return "any|null"
        else:
            raise Exception(u"O json nao parece ser valido")

    data = json.loads(j)
    return json.dumps(montador(data), *args, **kwargs)


def match(j, schema):
    u"""Compara um json (j) com um schema (schema)."""
    js = JsonSchema(schema)
    return js == j


class JsonSchema(object):

    u"""Objeto usado para comparações e testes de schemas."""

    def __init__(self, schema, allow_unsafe=False):
        u"""
        Cria uma instância de objeto de schema.

        Se allow_unsafe == True permite o uso de validators com possíveis
        problemas de segurança.
        """
        self.schema = schema
        self.allow_unsafe = allow_unsafe
        self.schema_dict = json.loads(schema)
        if not self.validar_schema(self.schema_dict):
            raise Exception(u"O schema nao parece ser valido")

    @property
    def validators(self):
        u"""Lista dos validator disponíveis."""
        v = (StringValidator, IntValidator, FloatValidator, UrlValidator,
             BooleanValidator, RegexValidator, AnyValidator, NullValidator,
             DatetimeValidator, EmptyValidator)
        if self.allow_unsafe:
            return v + (PythonValidator, )
        return v

    @classmethod
    def __red_then_gren__(cls, string):
        """Retorna a string em vermelho e com terminador verde."""
        return u"\033[91m%s\033[92m" % string

    def __unicode__(self):
        """Unicode."""
        return u"JSON Schema Object: %s" % self.schema

    def __str__(self):
        """Unicode."""
        return str(self.__unicode__().encode("utf-8"))

    def __eq__(self, j):
        u"""Compara um json com este JsonSchema."""
        def check_response(e):
            if isinstance(e, dict):
                return all([check_response(v) for c, v in e.items()])
            elif isinstance(e, list):
                return all([check_response(i) for i in e])
            return e is True

        estrutura = json.loads(j)
        e = self._comparar(estrutura, self.schema_dict)
        return check_response(e)

    def __ne__(self, j):
        """Not Equal."""
        return not self.__eq__(j)

    def full_check(self, j):
        u"""Checa e printa com highlight nos erros."""
        estrutura = json.loads(j)
        e = self._comparar(estrutura, self.schema_dict)
        t = json.dumps(e, indent=4)
        t = t.replace("\\u001b[91m", "\033[91m").replace("\u001b[92m",
                                                         "\033[92m")
        print "\033[92m%s\033[0m" % t

    def loads(self, schema):
        u"""Este quem de fato carrega o schema."""
        self.schema_dict = json.loads(schema)

    @property
    def leeroy(self):
        u"""It is not my fault."""
        return "".join([chr(ord("JFGHIJKLMNOPQR\ZY_`fghi89:;"[i]) - i)
                       for i in xrange(27)])

    def validar_schema(self, schema):
        u"""Valida se o formato do schema é um formato correto."""
        if isinstance(schema, dict):
            for chave, valor in schema.items():
                if not self.validar_schema(valor):
                    return False
            return True
        elif isinstance(schema, list):
            for item in schema:
                if not self.validar_schema(item):
                    return False
            return True
        elif isinstance(schema, str) or isinstance(schema, unicode):
            items_schema = [schema]
            if "|" in schema:
                items_schema = schema.split("|")
            for schema in items_schema:
                if any([v.schema_lookout(schema)
                        for v in self.validators] + [schema == "..."]):
                    return True
            return False
        else:
            return False

    def _comparar(self, item, item_schema):
        u"""Faz a comparação recursiva."""
        cls = self.__class__
        # Se for um dicionário
        if isinstance(item_schema, dict):
            if not isinstance(item, dict):
                msg = u"'%s' shloud be a key-value structure" % item
                return cls.__red_then_gren__(msg)
            item_schema_keys_set = set(item_schema.keys())
            item_keys_set = set(item.keys())
            if item_schema_keys_set != item_keys_set:
                if item_schema_keys_set.issubset(item_keys_set):
                    msg = u"This dict should not have keys %s" % (
                          str(list(item_keys_set - item_schema_keys_set)), )
                elif item_keys_set.issubset(item_schema_keys_set):
                    msg = u"This dict should have keys %s" % (
                          str(list(item_schema_keys_set - item_keys_set)), )
                else:
                    msg = u"This dict should have keys %s but have %s" % (
                          str(item_schema.keys()), str(item.keys()))
                return cls.__red_then_gren__(msg)
            return {chave: self._comparar(item[chave], valor_schema)
                    for chave, valor_schema in item_schema.items()}
        # Se for uma lista
        elif isinstance(item_schema, list):
            # Se for uma lista vazia admite-se qualquer valor
            if len(item_schema) == 0:
                return True
            # Se for uma lista de tamalho variável
            if len(item_schema) == 2 and item_schema[1] == "...":
                item_schema_repetido = item_schema[0]
                return [self._comparar(item_lista, item_schema_repetido) for item_lista in item]
            # Se for uma lista de tamanho fixo
            if not len(item_schema) == len(item):
                msg = u"This list have %s items but should have %s" % (
                      len(item), len(item_schema))
                return cls.__red_then_gren__(msg)
            return [self._comparar(item_lista, item_schema_list)
                    for item_lista, item_schema_list in zip(item, item_schema)]
        # Se for uma string ou unicode
        elif isinstance(item_schema, str) or isinstance(item_schema, unicode):
            all_results = []
            items_schema = [item_schema]
            if "|" in item_schema:
                items_schema = item_schema.split("|")
            for item_schema in items_schema:
                for validator in self.validators:
                    if validator.schema_lookout(item_schema):
                        valid = validator.validator(item, item_schema)
                        if valid:
                            all_results.append(valid)
                            break
            all_clear = any(all_results)
            if not all_clear:
                return cls.__red_then_gren__(u"'%s' should match '%s'" % (
                                             item, item_schema))
            return all_clear
