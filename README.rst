JSON Differ and Schema Matcher
==============================

Use this Lib to create a structure schema of a given JSON and also to check if a given JSON matches a given schema or simply to diff 2 JSONs.


Why Should I Use This?
----------------------

I made this for use when validating a JSON REST API using Behave. I wanted to be sure that the JSON's structure is correct, no matter it's content.

You may use it for whatever you want :)


Differ Features
---------------

- Diff 2 JSONs


Schema Features
---------------

- Export schema for a given JSON
- Validate a given schema
- Check if a given JSON matches a given schema
- Highlight any unmatched data between JSON and schema



Differ Usage
------------

diff_jsons()
""""""""""""
Show differences between 2 JSONs
::

    In [1]: from json_schema.json_differ import diff_jsons

    In [2]: diff_jsons('{"a": "1"}', '{"a": 2}')
    {
        "a": "'2' should match 'str:1'"
    }
    Out[2]: False
    
    In [3]: diff_jsons('{"a": "1"}', '{"a": "1"}')
    Out[3]: True


Schema Usage
------------

json_schema.loads()
"""""""""""""""""""
Load schema function. Receive a schema and return and JsonSchema object instance.
::

    In [1]: from json_schema import json_schema

    In [2]: my_schema = '{"my_key": "int:0:10|str"}'

    In [3]: my_schema_object = json_schema.loads(my_schema)

    In [4]: my_schema_object
    Out[4]: <json_schema.JsonSchema at 0x10aa96f10>

json_schema.dumps()
"""""""""""""""""""
Dump schema function. Receive a JSON and return an automaticaly created schema. Its very userful when working with some large or complex JSON. Be aware that you may have to adapt its returned schema to work with your JSON variations. For example, if your JSON have some optional value that, this time, is null the schema created will expect that that value is AWAYS null.
:: 

    In [1]: from json_schema import json_schema

    In [2]: my_json = '{"parrot": ["is no more", "It has ceased to be"], "ex-parrot": true, "volts": 2000}'

    In [3]: my_automatic_schema = json_schema.dumps(my_json)

    In [4]: my_automatic_schema
    Out[4]: '{"ex-parrot": "bool", "parrot": ["str", "..."], "volts": "int"}'


json_schema.match()
"""""""""""""""""""
Check if a given JSON matches a given schema.
::

    In [1]: from json_schema import json_schema

    In [2]: my_json = '{"parrot": ["is no more", "It has ceased to be"], "ex-parrot": true, "volts": 2000}'

    In [3]: my_schema = '{"ex-parrot": "bool", "parrot": ["str", "..."], "volts": "int"}'

    In [4]: json_schema.match(my_json, my_schema)
    Out[4]: True


JsonSchema Object
"""""""""""""""""
Object that contains all validations e checkups for that given schema.

JsonSchema.full_check()
"""""""""""""""""""""""
Check and highlights any errors found.
::

    In [1]: from json_schema import json_schema

    In [2]: my_schema = '{"ex-parrot": "bool", "parrot": ["str", "..."], "volts": "int"}'

    In [3]: JS = json_schema.loads(my_schema)

    In [4]: my_json = '{"parrot": ["is no more", "It has ceased to be"], "ex-parrot": true, "volts": 2000}'

    In [5]: JS.full_check(my_json)
    {
        "ex-parrot": true, 
        "parrot": [
            true, 
            true
        ], 
        "volts": true
    }

    In [6]: other_json = '{"parrot": ["is no more", "It has ceased to be"], "ex-parrot": true, "volts": "foobar"}'

    In [7]: JS.full_check(other_json)
    {
        "ex-parrot": true, 
        "parrot": [
            true, 
            true
        ], 
        "volts": "'foobar' should match 'int'"
    }


Usage Example
-------------

::

    In [1]: from json_schema import json_schema

    In [2]: um_json = '''{"chave_list": [1, 2],
                          "chave_dict": {"chave": "valor"},
                          "chave_int": 1,
                          "chave_float": 1.2,
                          "chave_string": "1"}'''

    In [3]: esquema = json_schema.dumps(um_json)

    In [4]: print esquema
    {"chave_list": ["int", "..."], "chave_dict": {"chave": "str"}, "chave_int": "int", "chave_float": "float", "chave_string": "str"}

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

    '{"my_key": "str"}'

Will match any of those:
::

    '{"my_key": "my_value"}'
    '{"my_key": "my value"}'
    '{"my_key": ""}'
    '{"my_key": "123"}'
    '{"my_key": "3.567"}'

It my have max length limit using "str:max_len"

::

    '{"my_key": "str:3"}'

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

Or direct string match using "str:string_to_match"

::

    '{"my_key": "str:Foo Bar"}'

Will match only:
::

    '{"my_key": "Foo Bar"}'

And not match those:
::

    '{"my_key": "foo bar"}'
    '{"my_key": "Foo bar"}'
    '{"my_key": "anything else"}'

int
"""

Will match only if that given JSON data is integer.

::

    '{"my_key": "int"}'

Will match any of those:
::

    '{"my_key": 0}'
    '{"my_key": 1}'
    '{"my_key": 12345}'
    '{"my_key": -1}'
    '{"my_key": -123}'

It my have min:max value limit using "int:min:max"

::

    '{"my_key": "int:-3:3"}'

Will match any of those:
::

    '{"my_key": 0}'
    '{"my_key": -1}'
    '{"my_key": -3}'
    '{"my_key": 1}'
    '{"my_key": 3}'

But not match those:
::

    '{"my_key": -4}'
    '{"my_key": 4}'
    '{"my_key": 12345}'


float
"""""

Same as int but for float values
::

    '{"my_key": "float"}'

Will match any of those:
::

    '{"my_key": 0.0}'
    '{"my_key": 1.1}'
    '{"my_key": 123.45}'
    '{"my_key": -1.1}'
    '{"my_key": -12.3}'

It my have min:max value limit using "float:min:max"

::

    '{"my_key": "float:-3.1:3.5"}'

Will match any of those:
::

    '{"my_key": 0.0}'
    '{"my_key": -1.2}'
    '{"my_key": -3.1}'
    '{"my_key": 1.0}'
    '{"my_key": 3.5}'

But not match those:
::

    '{"my_key": -4.0}'
    '{"my_key": 4.0}'
    '{"my_key": 123.45}'
    '{"my_key": 2}'


url
"""

Will match only if that given JSON data is a string that contains a valid URL.

::

    '{"my_key": "url"}'

Will match any of those:
::

    '{"my_key": "http://example.com"}'
    '{"my_key": "https://example.com"}'
    '{"my_key": "ftp://example.com"}'
    '{"my_key": "ftps://example.com"}'

Validation is made using the folowing python regular expression code
::

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


bool
""""

Will match only if that given JSON data is boolean.

::

    '{"my_key": "bool"}'

Will match only:
::

    '{"my_key": true}'
    '{"my_key": false}'

You may also match it's value:
::

    '{"my_key": "bool:True"}'
    '{"my_key": "bool:False"}'


regex
"""""

Will match only if that given JSON data is string and match some regex string.

::

    '{"my_key": "regex:[regex string]"}'

Example:
::

    In [1]: from json_schema import json_schema

    In [2]: json_schema.loads('{"my_key": "regex:^[0-9]{2}:[0-9]{2}:[0-9]{2}"}') == '{"my_key": "00:00:00"}'
    Out[2]: True

    In [3]: json_schema.loads('{"my_key": "regex:^[0-9]{2}:[0-9]{2}:[0-9]{2}"}') == '{"my_key": "00:00:0"}'
    Out[3]: False

    In [4]: json_schema.loads('{"my_key": "regex:^[0-9]{2}:[0-9]{2}:[0-9]{2}"}') == '{"my_key": "00:00:AA"}'
    Out[4]: False


python
""""""

Will match only if that given python code return True.
The value in JSON will be used as 'value' variable.

::

    '{"my_key": "python:[python code]"}'

Example:
::

    In [1]: from json_schema import json_schema

    In [2]: json_schema.loads('{"my_key": "python:value.upper() == value"}') == '{"my_key": "FOOBAR"}'
    Out[2]: True

    In [3]: json_schema.loads('{"my_key": "python:value.upper() == value"}') == '{"my_key": "FooBar"}'
    Out[3]: False

    In [4]: json_schema.loads('{"my_key": "python:value%2 == 2"}') == '{"my_key": 10}'
    Out[4]: True

    In [5]: json_schema.loads('{"my_key": "python:value%2 == 2"}') == '{"my_key": 11}'
    Out[5]: False


datetime
""""""""

Will match only if that given value match with datetime string formatter
https://docs.python.org/2/library/datetime.html#strftime-and-strptime-behavior

::

    '{"my_key": "datetime:format string"}'

Example:
::

    In [1]: from json_schema import json_schema

    In [2]: json_schema.loads('{"my_key": "datetime:%Y-%m-%d"}') == '{"my_key": "2015-07-07"}'
    Out[2]: True

    In [3]: json_schema.loads('{"my_key": "datetime:%Y-%m-%d"}') == '{"my_key": "2015-17-07"}'
    Out[3]: False

    In [4]: json_schema.loads('{"my_key": "datetime:%d/%m/%Y %H:%M:%S"}') == '{"my_key": "13/04/1984 11:22:33"}'
    Out[4]: True

    In [5]: json_schema.loads('{"my_key": "datetime:%d/%m/%Y %H:%M:%S"}') == '{"my_key": "04/13/1984 11:22:33"}'
    Out[5]: False



any
"""

Will match anything but null.

::

    '{"my_key": "any"}'

Will match any of those:
::

    '{"my_key": 10}'
    '{"my_key": "foo"}'
    '{"my_key": 1.5}'
    '{"my_key": true}'
    '{"my_key": ""}'

But not

::

    '{"my_key": null}'

null
""""

Will match only null values.

::

    '{"my_key": "null"}'

Will match:
::

    '{"my_key": null}'

But not
::

    '{"my_key": 10}'
    '{"my_key": "foo"}'
    '{"my_key": 1.5}'
    '{"my_key": true}'
    '{"my_key": ""}'

empty
"""""

Will match empty structures.

Supported:
::

    '{"my_key": "empty:list"}'
    '{"my_key": "empty:dict"}'
    '{"my_key": "empty:hash"}'
    '{"my_key": "empty:object"}'

Types 'hash', 'dict' and 'object' are actually same

::

    '{"my_key": "empty:list"}'


Will match:
::

    '{"my_key": []}'

And
::

    '{"my_key": "empty:object"}'


Will match:
::

    '{"my_key": {}}'


But not

::

    '{"my_key": null}'


Especial validations
--------------------

'|' - OR operator
"""""""""""""""""

Will match if any of validators match.
::

    '{"my_key": "str|int"}'

Will match:
::

    '{"my_key": "foo"}'
    '{"my_key": 123}'

Example
::

    In [1]: from json_schema import json_schema

    In [2]: json_schema.loads('{"my_key": "int|str"}') == '{"my_key": "foo"}'
    Out[2]: True

    In [3]: json_schema.loads('{"my_key": "int|str"}') == '{"my_key": 123}'
    Out[3]: True

    In [4]: json_schema.loads('{"my_key": "int:0:10|str:3"}') == '{"my_key": "foo"}'
    Out[4]: True

    In [5]: json_schema.loads('{"my_key": "int:0:10|str:3"}') == '{"my_key": 3}'
    Out[5]: True

    In [6]: json_schema.loads('{"my_key": "int:0:10|str:2"}') == '{"my_key": "foo"}'
    Out[6]: False

    In [7]: json_schema.loads('{"my_key": "int:10|str"}') == '{"my_key": 123}'
    Out[7]: False


This will match everything:
::

    '{"my_key": "any|null"}'


Arrays
""""""

Arrays are ordered so your schema order matters as also its size.
::

    '{"my_key": ["str", "str", "int"]}'

Will match:
::

    '{"my_key": ["foo", "bar", 123]}'

But not
::

    '{"my_key": ["foo", 123, "bar"]}'
    '{"my_key": ["foo", "bar", 123, 123]}'

If you dont know the size of your array you may user a special 2 item arrays as follows
::

    '{"my_key": ["str", "..."]}'

That will match:
::

    '{"my_key": ["foo"]}'
    '{"my_key": ["foo", "bar"]}'
    '{"my_key": ["foo", "bar", "Hello World"]}'
    '{"my_key": ["foo", "bar", "Hello World", "etc"]}'

Or even:
::

    '{"my_key": ["str|int", "..."]}'

That will match:
::

    '{"my_key": ["foo"]}'
    '{"my_key": [123]}'
    '{"my_key": ["foo", "bar"]}'
    '{"my_key": ["foo", 123, "Hello World"]}'
    '{"my_key": [123, "bar", "Hello World", 0]}'


Hashs (dicts)
"""""""""""""

Hashs are not ordered so your schema order does not matters but its keys does.
::

    '{"my_key": {"internal_key_1": "str", "internal_key_2": "int"}'

Will match:
::

    '{"my_key": {"internal_key_1": "foo", "internal_key_2": 123}'
    '{"my_key": {"internal_key_2": 123, "internal_key_2": "foo"}'

But not
::

    '{"my_key": {"internal_key_1": 123, "internal_key_2": "foo"}'
    '{"my_key": {"internal_key_1": "foo", "internal_key_3": 123}'
    '{"my_key": {"internal_key_1": "foo", "internal_key_2": 123, "fizz": "buzz"}'


Recursivity
"""""""""""

All validations are recursive so they will check into arrays, hashs, array of arrays, etc.
::

    '[{"my_key": ["str|int", "..."]}, {"my_key": "str"}, "int", ["int|str", "str"]'

Will match:
::

    '[{"my_key": [1, "foo", "bar", 100]}, {"my_key": "foo"}, 12345, [123, "foo"]'


