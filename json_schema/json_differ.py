# -*- encoding: utf-8 -*-
import six
try:
    import simplejson as json
except:
    import json
from .json_schema import JsonSchema


def dumps(j, *args, **kwargs):
    """Recebe um json e retorna um schema."""
    def montador(valor):
        """Função recursiva para montar o schema."""
        if isinstance(valor, dict):
            retorno = {}
            for c, v in list(valor.items()):
                retorno[c] = montador(v)
            return retorno
        elif isinstance(valor, list) or isinstance(valor, tuple):
            retorno = []
            for i in valor:
                retorno.append(montador(i))
            return retorno
        elif isinstance(valor, six.string_types):
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
            raise Exception("O json nao parece ser valido")

    data = json.loads(j)
    return json.dumps(montador(data), *args, **kwargs)


def diff_jsons(b, a):
    """Mostra se há diferença entre 2 jsons."""
    schema_a = JsonSchema(dumps(a))
    if schema_a == b:
        return True
    schema_a.full_check(b)
    return False


def diff(a, b):
    """Mostra a diferença entre JSONs."""
    def type_name(obj):
        """Traduz a nomeclatura python para javascript."""
        return {"str": "string",
                "unicode": "string",
                "int": "integer",
                "dict": "hash",
                "list": "array",
                "NoneType": "null",
                "float": "float",
                "bool": "boolean"}[type(obj).__name__]

    def comparador(ia, ib):
        if ia == ib:
            return ia
        if type(ia) == type(ib):
            if isinstance(ia, dict):
                chaves_a = set(ia.keys())
                chaves_b = set(ib.keys())
                if chaves_a == chaves_b:
                    retorno = {}
                    for chave in chaves_a:
                        retorno[chave] = comparador(ia[chave], ib[chave])
                    return retorno
                else:
                    retorno = {}
                    apenas_a = chaves_a - chaves_b
                    apenas_b = chaves_b - chaves_a
                    for chave in apenas_a:
                        retorno[chave] = False, "Exists on left branch only"
                    for chave in apenas_b:
                        retorno[chave] = False, "Exists on right branch only"
                    for chave in chaves_a & chaves_b:
                        retorno[chave] = comparador(ia[chave], ib[chave])
                    return retorno
            elif isinstance(ia, list):
                retorno = []
                for i in range(min([len(ia), len(ib)])):
                    retorno.append(comparador(ia[i], ib[i]))
                if len(ia) > len(ib):
                    retorno += [(False, "%s '%s' exists on left branch only" %
                                (type_name(i), i)) for i in ia[len(ib):]]
                elif len(ia) < len(ib):
                    retorno += [(False, "%s '%s' exists on right branch only" %
                                (type_name(i), i)) for i in ib[len(ia):]]
                return retorno
            elif type(ia) in [str, int, float, bool, str]:
                var_type = type_name(ia)
                return False, "Left %s '%s' differ from right %s '%s'" % (
                               var_type, ia, var_type, ib)
        else:
            if {type(ia), type(ib)}.issubset({int, str, float, bool, type(None)}):
                return (False, "Left %s '%s' differ from right %s '%s'" % (
                                type_name(ia), ia, type_name(ib), ib))
            else:
                if type(ia) in [dict, list]:
                    left = "Left is a %s structure and differ from " % type_name(ia)
                else:
                    left = "Left %s '%s' differ from " % (type_name(ia), ia)
                if type(ib) in [dict, list]:
                    right = "right which is %s structure" % type_name(ib)
                else:
                    right = "right %s '%s'" % (type_name(ib), ib)
                return (False, "%s%s" % (left, right))

    ja, jb = json.loads(a), json.loads(b)
    return comparador(ja, jb)


def diff_color_string(a, b, indent=4):
    """Retorna uma string com color code mostrando as diferenças."""
    def replacer(d):
        if isinstance(d, dict):
            r = {}
            for k, v in list(d.items()):
                r[k] = replacer(v)
            return r
        elif isinstance(d, list):
            r = []
            for i in d:
                r.append(replacer(i))
            return r
        elif isinstance(d, tuple):
            return "\033[91m%s\033[92m" % d[1]
        else:
            return d
    diferencas = replacer(diff(a, b))
    r = json.dumps(diferencas,
                   indent=indent).replace("\\u001b[91m",
                                          "\033[91m").replace("\\u001b[92m",
                                                              "\033[92m")
    return "\033[92m%s\033[0m" % r
