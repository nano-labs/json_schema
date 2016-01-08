# -*- encoding: utf-8 -*-
u"""Validators padrão a serem usados pelo json_schema."""

import re
from datetime import datetime


class StringValidator:

    u"""Classe apenas para agrupar os metodos do validador.

    Validação:
        Checa se o item é um string e se o tamanho máximo não
        ultrapassa max lenght

    Formatos possíveis:
        "str"
        "str:max lenght

    Ex:
        "str:10"
    """

    @classmethod
    def schema_lookout(cls, schema):
        """Checa se dado schema deve ser validado por este Validator."""
        return schema.startswith("str")

    @classmethod
    def validator(cls, item, item_schema):
        """Validador de fato da string."""
        if isinstance(item, str) or isinstance(item, unicode):
            if item_schema.startswith("str:"):
                try:
                    tamanho = int(item_schema.replace("str:", ""))
                    if len(item) > tamanho:
                        return False
                    return True
                except ValueError:
                    return item == item_schema.replace("str:", "")
            return True
        return False


class IntValidator:

    u"""
    Classe apenas para agrupar os metodos do validador.

    Validação:
        Checa se o item é um Int e se o valor está entre min e max

    Formatos possíveis:
        "int"
        "int:min:max

    Ex:
        "int:-10:10"
    """

    @classmethod
    def schema_lookout(cls, schema):
        """Checa se dado schema deve ser validado por este Validator."""
        return schema.startswith("int")

    @classmethod
    def validator(cls, item, item_schema):
        """Validador de fato do int."""
        if not isinstance(item, int):
            return False
        if item_schema == "int":
            return True
        m = re.match("int\:(\-?[0-9]+)\:(\-?[0-9]+)", item_schema)
        if m:
            inferior, superior = m.groups()
            if item >= int(inferior) and item <= int(superior):
                return True
        return False


class FloatValidator:

    u"""
    Classe apenas para agrupar os metodos do validador.

    Validação:
        Checa se o item é um Float e se o valor está entre min e max

    Formatos possíveis:
        "float"
        "float:min:max

    Ex:
        "float:-10.5:10.5"
    """

    @classmethod
    def schema_lookout(cls, schema):
        """Checa se dado schema deve ser validado por este Validator."""
        return schema.startswith("float")

    @classmethod
    def validator(cls, item, item_schema):
        """Validador de fato do float."""
        if not isinstance(item, float):
            return False
        if item_schema == "float":
            return True
        m = re.match("float\:(\-?[0-9]+\.[0-9]+)\:(\-?[0-9]+\.[0-9]+)",
                     item_schema)
        if m:
            inferior, superior = m.groups()
            if item >= float(inferior) and item <= float(superior):
                return True
        return False


class UrlValidator:

    u"""
    Classe apenas para agrupar os metodos do validador.

    Validação:
        Checa se o item é um Url

    Formatos possíveis:
        "url"

    Ex:
        "url"
    """

    @classmethod
    def schema_lookout(cls, schema):
        """Checa se dado schema deve ser validado por este Validator."""
        return schema == "url"

    @classmethod
    def validator(cls, item, item_schema):
        """Validador de fato do float."""
        regex = re.compile(r'^(?:http|ftp)s?://'  # HTTP, HTTPS, FTP, FTPS
                           # Dominio
                           r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
                           # Localhost
                           r'localhost|'
                           # IP
                           r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
                           # Porta
                           r'(?::\d+)?'
                           r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        try:
            return True if regex.match(item) else False
        except:
            return False


class BooleanValidator:

    u"""
    Classe apenas para agrupar os metodos do validador.

    Validação:
        Checa se o item é um Boolean

    Formatos possíveis:
        "bool"
        "bool:True"
        "bool:False"

    Ex:
        "bool"
    """

    @classmethod
    def schema_lookout(cls, schema):
        """Checa se dado schema deve ser validado por este Validator."""
        return schema.startswith("bool")

    @classmethod
    def validator(cls, item, item_schema):
        """Validador de fato do bool."""
        if ":" in item_schema:
            value = item_schema.split(":")[1] == "True"
            return item == value
        return isinstance(item, bool)


class RegexValidator:

    u"""
    Classe apenas para agrupar os metodos do validador.

    Validação:
        Checa se o item match em um regex

    Formatos possíveis:
        "regex:regex string"

    Ex:
        "regex:^[0-9]{2}\\\\:[0-9]{2}\\\\:[0-9]{2}$"
    """

    @classmethod
    def schema_lookout(cls, schema):
        """Checa se dado schema deve ser validado por este Validator."""
        if schema.startswith("regex:"):
            re.compile(schema.replace("regex:", ""))
            return True
        return False

    @classmethod
    def validator(cls, item, item_schema):
        """Validador de fato do bool."""
        regex = re.compile(item_schema.replace("regex:", ""))
        return True if regex.match(item) else False


class AnyValidator:

    u"""
    Classe apenas para agrupar os metodos do validador.

    Validação:
        Aceita qualquer coisa

    Formatos possíveis:
        "any"

    Ex:
        "any"
    """

    @classmethod
    def schema_lookout(cls, schema):
        """Checa se dado schema deve ser validado por este Validator."""
        return schema.startswith("any")

    @classmethod
    def validator(cls, item, item_schema):
        """Como pode ser qualquer coisa sempre retorna True."""
        return True


class NullValidator:

    u"""
    Classe apenas para agrupar os metodos do validador.

    Validação:
        Checa se o valor é "null"

    Formatos possíveis:
        "null"

    Ex:
        "null"
    """

    @classmethod
    def schema_lookout(cls, schema):
        """Checa se dado schema deve ser validado por este Validator."""
        return schema == "null"

    @classmethod
    def validator(cls, item, item_schema):
        """Como pode ser qualquer coisa sempre retorna True."""
        return item is None


class PythonValidator:

    u"""
    Classe apenas para agrupar os metodos do validador.

    Validação:
        Checa se o valor passa numa expressão python definida

    Formatos possíveis:
        "python:codigo_python"

    Ex:
        "python:value.upper() == value"
    """

    @classmethod
    def schema_lookout(cls, schema):
        """Checa se dado schema deve ser validado por este Validator."""
        return schema.startswith("python:")

    @classmethod
    def validator(cls, item, item_schema):
        u"""Testa o código python."""
        src = item_schema.replace("python:", "")
        src = """def temporary_function(value):\n    return %s""" % src
        try:
            exec(src)
            return temporary_function(item)
        except:
            return False


class DatetimeValidator:

    u"""
    Classe apenas para agrupar os metodos do validador.

    Validação:
        Checa se o valor confere num datetime.strptime

    Formatos possíveis:
        "datetime:datetime string formater"

    Ex:
        "datetime:%Y-%m-%d"
    """

    @classmethod
    def schema_lookout(cls, schema):
        """Checa se dado schema deve ser validado por este Validator."""
        return schema.startswith("datetime:")

    @classmethod
    def validator(cls, item, item_schema):
        """Testa o datetime.strptime()."""
        string_formater = item_schema.replace("datetime:", "")
        try:
            datetime.strptime(item, string_formater)
            return True
        except:
            return False


class EmptyValidator:

    u"""
    Classe apenas para agrupar os metodos do validador.

    Validação:
        Checa se o valor está vazio

    Formatos possíveis:
        "empty:list"
        "empty:dict"
        "empty:hash"
        "empty:object"

    dict, hash e object são sinonimos.
    """

    @classmethod
    def schema_lookout(cls, schema):
        """Checa se dado schema deve ser validado por este Validator."""
        return schema.startswith("empty:")

    @classmethod
    def validator(cls, item, item_schema):
        u"""Testa se o item é de dado tipo e está vazio."""
        tipo = item_schema.replace("empty:", "")
        tipos = {"dict": dict, "hash": dict, "object": dict, "list": list}
        return isinstance(item, tipos[tipo]) and len(item) == 0
