JSON Schema
===========

Use this Lib to create a structure schema of a given JSON and also to check if a given JSON matches a given schema.


Why Should I Use This?
----------------------

Features
--------

Usage Exemple:
--------------
.. code-block:: bash
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