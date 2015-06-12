JSON Schema
===========

Use this Lib to create a structure schema of a given JSON and also to check if a given JSON matches a given schema.


Why Should I Use This?
----------------------

I made this for use when validating a JSON REST API using Behave. I wanted to be sure that the JSON's structure is correct, no matter it's content.

You may use it for whatever you want :)


Features
--------

- Export schema form a given JSON
- Validate a given schema
- Check if a given JSON matches a given schema
- Highlight any unmatched data between JSON and schema

Usage Exemple
-------------

::

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


Validators
----------

string
""""""

Will match only if that given JSON data is string.

::

    '{"my_key": "string"}'

Will match any of those:
::

    '{"my_key": "my_value"}'
    '{"my_key": "my value"}'
    '{"my_key": ""}'
    '{"my_key": "123"}'
    '{"my_key": "3.567"}'

It my have max length limit using "string:max_len"

::

    '{"my_key": "string:3"}'

Will match any of those:
::

    '{"my_key": ""}'
    '{"my_key": "a"}'
    '{"my_key": "ab"}'
    '{"my_key": "abc"}'
    '{"my_key": "123"}'

But not match those:
::

    '{"my_key": "abcd"}'
    '{"my_key": "abcde"}'
    '{"my_key": "1234"}'
