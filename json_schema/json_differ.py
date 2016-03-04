# -*- encoding: utf-8 -*-
try:
    import simplejson as json
except:
    import json
from json_schema import JsonSchema


def dumps(j, *args, **kwargs):
    u"""Recebe um json e retorna um schema."""
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
            return retorno
        elif isinstance(valor, str) or isinstance(valor, unicode):
            return "str:%s" % valor
        elif isinstance(valor, bool):
            return "bool:%s" % valor
        elif isinstance(valor, int):
            return "int:%s:%s" % (valor, valor)
        elif isinstance(valor, float):
            return "float:%s:%s" % (valor, valor)
        elif valor is None:
            return "null"
        else:
            raise Exception(u"O json nao parece ser valido")

    data = json.loads(j)
    return json.dumps(montador(data), *args, **kwargs)


def diff_jsons(b, a):
    u"""Mostra a diferença entre 2 jsons."""
    schema_a = JsonSchema(dumps(a))
    if schema_a == b:
        return True
    schema_a.full_check(b)
    return False
