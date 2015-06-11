# -*- encoding: utf-8 -*-
u"""Validators padrão a serem usados pelo json_schema."""

import re


class StringValidator:

    u"""Classe apenas para agrupar os metodos do validador.

    Validação:
        Checa se o item é um string e se o tamanho máximo não
        ultrapassa max lenght

    Formatos possíveis:
        "string"
        "string:max lenght

    Ex:
        "string:10"
    """

    @classmethod
    def schema_lookout(cls, schema):
        """Checa se dado schema deve ser validado por este Validator."""
        return schema.startswith("string")

    @classmethod
    def validator(cls, item, item_schema):
        """Validador de fato da string."""
        if isinstance(item, str) or isinstance(item, unicode):
            if item_schema.startswith("string:"):
                tamanho = int(item_schema.replace("string:", ""))
                if len(item) > tamanho:
                    return False
                return True
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
        return True if regex.match(item) else False


class BooleanValidator:

    u"""
    Classe apenas para agrupar os metodos do validador.

    Validação:
        Checa se o item é um Boolean

    Formatos possíveis:
        "bool"

    Ex:
        "bool"
    """

    @classmethod
    def schema_lookout(cls, schema):
        """Checa se dado schema deve ser validado por este Validator."""
        return schema == "bool"

    @classmethod
    def validator(cls, item, item_schema):
        """Validador de fato do bool."""
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
