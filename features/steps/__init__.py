# -*- coding: utf-8 -*-
u"""Steps para testes."""

try:
    import simplejson as json
except:
    import json
import behave
import logging
from json_schema import json_schema

INT_SCHEMA = """{"a": "int"}"""
INT_JSON = """{"a": 10}"""
STR_JSON = """{"a": "biscoito"}"""

URL_SCHEMA = """{"a": "url"}"""
NULL_SCHEMA = """{"a": "null"}"""
URL_OR_NULL_SCHEMA = """{"a": "url|null"}"""
URL_JSON = """{"a": "http://example.com"}"""
NULL_JSON = """{"a": null}"""


DICT_SCHEMA_A = """{"a": {"b": "int",
                          "c": "str"}}"""
DICT_JSON_A = """{"a": {"b": 10,
                        "c": "biscoito"}}"""
DICT_JSON_B = """{"a": {"b": 10,
                        "c": "biscoito",
                        "d": "foo"}}"""
DICT_JSON_C = """{"a": {"b": 10,
                        "d": "biscoito"}}"""

PYTHON_SCHEMA = """{"a": "python:value.upper() == value"}"""
PYTHON_JSON = """{"a": "HELLO WORLD"}"""
PYTHON_FAIL_JSON = """{"a": "Hello World"}"""


@behave.given('from {libfile} import {value} as {key}')
def from_file_import_as(context, libfile, value, key):
    """Importa algo de um arquivo para o contexto com nome."""
    end_path_lib = __import__(libfile)
    for n in libfile.split(".")[1:]:
        end_path_lib = getattr(end_path_lib, n)
    context.__setattr__(key, end_path_lib.__getattribute__(value))


@behave.given('from {libfile} import {value}')
def from_file_import(context, libfile, value):
    """Importa algo de um arquivo para o contexto."""
    return from_file_import_as(context, libfile, value, value)


@behave.given('I have schema {schema}')
def i_have_schema(context, schema):
    """Carrega o schema {schema} no atributo 'test_schema' no context."""
    try:
        s = json_schema.loads(getattr(context, schema))
    except:
        logging.info("### Erro ao carregar o schema ###")
        logging.info(repr(getattr(context, schema)))
        raise
    context.__setattr__("test_schema", s)


@behave.given('I have unsafe schema {schema}')
def i_have_unsafe_schema(context, schema):
    """Carrega o schema {schema} con allow_unsafe."""
    try:
        s = json_schema.loads(getattr(context, schema), allow_unsafe=True)
    except:
        logging.info("### Erro ao carregar o schema ###")
        logging.info(repr(getattr(context, schema)))
        raise
    context.__setattr__("test_schema", s)


@behave.then('I can\'t have schema {schema}')
def i_cant_have_schema(context, schema):
    """Falha ao carregar o schema."""
    try:
        s = json_schema.loads(getattr(context, schema))
    except Exception, e:
        assert str(e) == "O schema nao parece ser valido"


@behave.given('I have JSON {jdata}')
def i_have_schema(context, jdata):
    """Carrega o JSON {jdata} no atributo 'test_json' no context."""
    try:
        j = json.loads(getattr(context, jdata))
    except:
        logging.info("### Erro ao parsear o JSON ###")
        logging.info(repr(jdata))
        raise


@behave.then('schema {s} should match JSON {j}')
def json_should_match_schema(context, s, j):
    """Carrega o JSON {jdata} no atributo 'test_json' no context."""
    schema = json_schema.loads(getattr(context, s), allow_unsafe=True)
    json_string = getattr(context, j)
    try:
        if not schema == json_string:
            schema.full_check(json_string)
    except:
        logging.info(schema)
        logging.info(json_string)
        pass
    assert schema == json_string


@behave.then('schema {s} should not match JSON {j}')
def json_should_not_match_schema(context, s, j):
    """Carrega o JSON {jdata} no atributo 'test_json' no context."""
    schema = json_schema.loads(getattr(context, s), allow_unsafe=True)
    json_string = getattr(context, j)
    logging.info(schema)
    logging.info(json_string)
    assert not schema == json_string
