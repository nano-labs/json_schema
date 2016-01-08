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
import re
from pprint import pprint
from validators import (StringValidator, IntValidator, FloatValidator,
                        UrlValidator, BooleanValidator, RegexValidator,
                        AnyValidator, NullValidator, PythonValidator,
                        DatetimeValidator, EmptyValidator)


def loads(schema):
    u"""Recebe uma string de schema e retorna um JsonSchema object."""
    return JsonSchema(schema)


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

    validators = (StringValidator, IntValidator, FloatValidator,
                  UrlValidator, BooleanValidator, RegexValidator,
                  AnyValidator, NullValidator, PythonValidator,
                  DatetimeValidator, EmptyValidator)

    def __init__(self, schema):
        u"""Ainda não sei."""
        self.schema = schema
        self.schema_dict = json.loads(schema)
        if not JsonSchema.validar_schema(self.schema_dict):
            raise Exception(u"O schema nao parece ser valido")

    @classmethod
    def __red_then_gren__(self, string):
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
            return e == True

        estrutura = json.loads(j)
        e = JsonSchema.comparar(estrutura, self.schema_dict)
        return check_response(e)

    def __ne__(self, j):
        """Not Equal."""
        return not self.__eq__(j)

    def full_check(self, j):
        u"""Checa e printa com highlight nos erros."""
        estrutura = json.loads(j)
        e = JsonSchema.comparar(estrutura, self.schema_dict)
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
            items_schema = [schema]
            if "|" in schema:
                items_schema = schema.split("|")
            for schema in items_schema:
                if any([v.schema_lookout(schema)
                        for v in cls.validators] + [schema == "..."]):
                    return True
            return False
        else:
            return False

    @classmethod
    def comparar(cls, item, item_schema):
        u"""Faz a comparação recursiva."""
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
            return {chave: cls.comparar(item[chave], valor_schema)
                    for chave, valor_schema in item_schema.items()}
        # Se for uma lista
        elif isinstance(item_schema, list):
            # Se for uma lista vazia admite-se qualquer valor
            if len(item_schema) == 0:
                return True
            # Se for uma lista de tamalho variável
            if len(item_schema) == 2 and item_schema[1] == "...":
                item_schema_repetido = item_schema[0]
                return [cls.comparar(item_lista, item_schema_repetido) for item_lista in item]
            # Se for uma lista de tamanho fixo
            if not len(item_schema) == len(item):
                msg = u"This list have %s items but should have %s" % (
                      len(item), len(item_schema))
                return cls.__red_then_gren__(msg)
            return [cls.comparar(item_lista, item_schema_list)
                    for item_lista, item_schema_list in zip(item, item_schema)]
        # Se for uma string ou unicode
        elif isinstance(item_schema, str) or isinstance(item_schema, unicode):
            all_results = []
            items_schema = [item_schema]
            if "|" in item_schema:
                items_schema = item_schema.split("|")
            for item_schema in items_schema:
                for validator in cls.validators:
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


def _teste(j):
    js = loads(dumps(j))
    js.full_check(j)
    return js == j

j = u"""
[{"id":4159958,"legacy_id":4159958,"_type":"Video","kind":"Video","adult":false,"category":"Entretenimento","channel_id":196,"collaborative_upload_id":null,"collaborative_upload_user":null,"created_at":"2015-05-06T15:10:50-03:00","created_by":"tvg_raphael.almeida","cut_format":"trecho","description":"Elenco convida o público para a estreia","duration":32766,"exhibited_at":"2015-05-06T15:09:00-03:00","hd_available":true,"hits":11062,"hits_data":{"last_day":18,"last_hour":1,"last_updated_at":1434034586,"last_week":204},"likes":35,"likes_data":{"last_day":0,"last_hour":0,"last_updated_at":1434034586,"last_week":0},"notes":"","program_id":2546,"published_at":"2015-05-07T12:39:56-03:00","queryable":true,"ratings":null,"recommendation_publisher":"webmedia-globotv-intermediate","scheduled_publication_in":null,"scheduled_unpublication_in":null,"status":"published","subscriber_only":false,"tags":["Rede Globo","entretenimento","Bastidores","Zorra","humor","Gshow","vídeos exclusivos Gshow","exclusivo"],"title":"Confira bastidores das primeiras cenas do Zorra!","unpublished_at":"2015-05-06T15:11:22-03:00","updated_at":"2015-05-07T12:39:56-03:00","updated_by":"tvg_thiago.lavega","url_for_consumption":"http://globotv.globo.com/rede-globo/zorra-total/v/confira-bastidores-das-primeiras-cenas-do-zorra/4159958/","videos_ids":[],"votes_count":null,"votes_sum":null,"countries":[]},{"id":4152075,"legacy_id":4152075,"_type":"FullEpisode","kind":"FullEpisode","adult":false,"category":"Entretenimento","channel_id":196,"collaborative_upload_id":null,"collaborative_upload_user":null,"created_at":"2015-05-03T00:40:54-03:00","created_by":"tvg_fernanda.costalonga","cut_format":null,"description":"Zorra Total - Programa de 02/05/2015 na íntegra","duration":2247646,"exhibited_at":"2015-05-02T23:16:15-03:00","hd_available":true,"hits":2327,"hits_data":{"last_day":17,"last_hour":4,"last_updated_at":1434032207,"last_week":145},"likes":16,"likes_data":{"last_day":0,"last_hour":0,"last_updated_at":1434032207,"last_week":0},"notes":null,"program_id":2546,"published_at":"2015-05-03T00:41:01-03:00","queryable":true,"ratings":null,"recommendation_publisher":"webmedia-globotv-intermediate","scheduled_publication_in":null,"scheduled_unpublication_in":null,"status":"published","subscriber_only":true,"tags":["Rede Globo","Zorra Total","dramaturgia","episódio","Séries","entretenimento","quadros","personagens"],"title":"Zorra Total - Programa de 02/05/2015 na íntegra","unpublished_at":null,"updated_at":"2015-05-04T00:12:10-03:00","updated_by":"tvg_fernanda.costalonga","url_for_consumption":"http://globotv.globo.com/rede-globo/zorra-total/v/zorra-total-programa-de-02052015-na-integra/4152075/","videos_ids":[4152062,4152042,4152046],"votes_count":null,"votes_sum":null,"countries":[]},{"id":4152051,"legacy_id":4152051,"_type":"Video","kind":"Video","adult":false,"category":"Entretenimento","channel_id":196,"collaborative_upload_id":null,"collaborative_upload_user":null,"created_at":"2015-05-02T23:43:36-03:00","created_by":"tvg_fernanda.costalonga","cut_format":"trecho","description":"Ela não se aguenta quando atende um pobre","duration":250335,"exhibited_at":"2015-05-02T23:01:03-03:00","hd_available":true,"hits":4221,"hits_data":{"last_day":24,"last_hour":2,"last_updated_at":1434029797,"last_week":229},"likes":62,"likes_data":{"last_day":0,"last_hour":0,"last_updated_at":1434029797,"last_week":5},"notes":null,"program_id":2546,"published_at":"2015-05-02T23:44:07-03:00","queryable":true,"ratings":null,"recommendation_publisher":"webmedia-globotv-intermediate","scheduled_publication_in":null,"scheduled_unpublication_in":null,"status":"published","subscriber_only":false,"tags":["Rede Globo","Zorra Total","dramaturgia","episódio","Séries","entretenimento","quadros","personagens"],"title":"Nomealda dá uma de informante e comediante","unpublished_at":null,"updated_at":"2015-05-02T23:46:12-03:00","updated_by":"tvg_fernanda.costalonga","url_for_consumption":"http://globotv.globo.com/rede-globo/zorra-total/v/nomealda-da-uma-de-informante-e-comediante/4152051/","videos_ids":[],"votes_count":null,"votes_sum":null,"countries":[]},{"id":4152047,"legacy_id":4152047,"_type":"Video","kind":"Video","adult":false,"category":"Entretenimento","channel_id":196,"collaborative_upload_id":null,"collaborative_upload_user":null,"created_at":"2015-05-02T23:30:36-03:00","created_by":"tvg_fernanda.costalonga","cut_format":"trecho","description":"Fiscal questiona a origem da madeira com a qual Pinóquio foi construído","duration":122625,"exhibited_at":"2015-05-02T22:50:00-03:00","hd_available":true,"hits":1616,"hits_data":{"last_day":5,"last_hour":1,"last_updated_at":1434032930,"last_week":22},"likes":15,"likes_data":{"last_day":0,"last_hour":0,"last_updated_at":1434032930,"last_week":0},"notes":"","program_id":2546,"published_at":"2015-05-02T23:31:01-03:00","queryable":true,"ratings":null,"recommendation_publisher":"webmedia-globotv-intermediate","scheduled_publication_in":null,"scheduled_unpublication_in":null,"status":"published","subscriber_only":false,"tags":["Rede Globo","Zorra Total","entretenimento"],"title":"Pinóquio e Gepeto tentam uma deleção premiada","unpublished_at":null,"updated_at":"2015-05-03T00:20:02-03:00","updated_by":"tvg_fernanda.costalonga","url_for_consumption":"http://globotv.globo.com/rede-globo/zorra-total/v/pinoquio-e-gepeto-tentam-uma-delecao-premiada/4152047/","videos_ids":[],"votes_count":null,"votes_sum":null,"countries":[]},{"id":4152033,"legacy_id":4152033,"_type":"Video","kind":"Video","adult":false,"category":"Entretenimento","channel_id":196,"collaborative_upload_id":null,"collaborative_upload_user":null,"created_at":"2015-05-02T23:12:30-03:00","created_by":"tvg_fernanda.costalonga","cut_format":"trecho","description":"Hércules dá vexame e briga com todas as mulheres para conseguir o buquê da noiva","duration":321388,"exhibited_at":"2015-05-02T22:45:41-03:00","hd_available":true,"hits":5810,"hits_data":{"last_day":30,"last_hour":3,"last_updated_at":1434033130,"last_week":350},"likes":68,"likes_data":{"last_day":0,"last_hour":0,"last_updated_at":1434033130,"last_week":5},"notes":null,"program_id":2546,"published_at":"2015-05-02T23:13:05-03:00","queryable":true,"ratings":null,"recommendation_publisher":"webmedia-globotv-intermediate","scheduled_publication_in":null,"scheduled_unpublication_in":null,"status":"published","subscriber_only":false,"tags":["Rede Globo","Zorra Total","dramaturgia","episódio","Séries","entretenimento","quadros","personagens"],"title":"Mozinha fisga Hércules para casar, mas ele foge com um bofe","unpublished_at":null,"updated_at":"2015-05-02T23:16:19-03:00","updated_by":"tvg_fernanda.costalonga","url_for_consumption":"http://globotv.globo.com/rede-globo/zorra-total/v/mozinha-fisga-hercules-para-casar-mas-ele-foge-com-um-bofe/4152033/","videos_ids":[],"votes_count":null,"votes_sum":null,"countries":[]},{"id":4152021,"legacy_id":4152021,"_type":"Video","kind":"Video","adult":false,"category":"Entretenimento","channel_id":196,"collaborative_upload_id":null,"collaborative_upload_user":null,"created_at":"2015-05-02T22:56:01-03:00","created_by":"tvg_fernanda.costalonga","cut_format":"trecho","description":"Mulher paga o dobro para Zé Ruela e Beiradinha cantarem por dois dias seguidos em frente à casa de seu admirador","duration":218802,"exhibited_at":"2015-05-02T22:41:48-03:00","hd_available":true,"hits":3533,"hits_data":{"last_day":14,"last_hour":2,"last_updated_at":1434029798,"last_week":129},"likes":37,"likes_data":{"last_day":0,"last_hour":0,"last_updated_at":1434029798,"last_week":3},"notes":null,"program_id":2546,"published_at":"2015-05-02T22:56:30-03:00","queryable":true,"ratings":null,"recommendation_publisher":"webmedia-globotv-intermediate","scheduled_publication_in":null,"scheduled_unpublication_in":null,"status":"published","subscriber_only":false,"tags":["Rede Globo","Zorra Total","dramaturgia","episódio","Séries","entretenimento","quadros","personagens"],"title":"Serenata às avessas","unpublished_at":null,"updated_at":"2015-05-02T22:58:30-03:00","updated_by":"tvg_fernanda.costalonga","url_for_consumption":"http://globotv.globo.com/rede-globo/zorra-total/v/serenata-as-avessas/4152021/","videos_ids":[],"votes_count":null,"votes_sum":null,"countries":[]},{"id":4152016,"legacy_id":4152016,"_type":"Video","kind":"Video","adult":false,"category":"Entretenimento","channel_id":196,"collaborative_upload_id":null,"collaborative_upload_user":null,"created_at":"2015-05-02T22:48:18-03:00","created_by":"tvg_fernanda.costalonga","cut_format":"trecho","description":"O clube tem atrações para todos os gostos!","duration":315583,"exhibited_at":"2015-05-02T22:40:36-03:00","hd_available":true,"hits":3685,"hits_data":{"last_day":18,"last_hour":1,"last_updated_at":1434029272,"last_week":178},"likes":34,"likes_data":{"last_day":0,"last_hour":0,"last_updated_at":1434029272,"last_week":2},"notes":null,"program_id":2546,"published_at":"2015-05-02T22:48:48-03:00","queryable":true,"ratings":null,"recommendation_publisher":"webmedia-globotv-intermediate","scheduled_publication_in":null,"scheduled_unpublication_in":null,"status":"published","subscriber_only":false,"tags":["Rede Globo","Zorra Total","dramaturgia","episódio","Séries","entretenimento","quadros","personagens"],"title":"A mulherada enlouquece no Zorra City Club","unpublished_at":null,"updated_at":"2015-05-02T22:52:08-03:00","updated_by":"tvg_fernanda.costalonga","url_for_consumption":"http://globotv.globo.com/rede-globo/zorra-total/v/a-mulherada-enlouquece-no-zorra-city-club/4152016/","videos_ids":[],"votes_count":null,"votes_sum":null,"countries":[]},{"id":4120444,"legacy_id":4120444,"_type":"FullEpisode","kind":"FullEpisode","adult":false,"category":"Entretenimento","channel_id":196,"collaborative_upload_id":null,"collaborative_upload_user":null,"created_at":"2015-04-19T00:08:56-03:00","created_by":"tvg_rosana.araujo_let","cut_format":null,"description":"Zorra Total - Programa de sábado, 18/04/2015, na íntegra","duration":2216300,"exhibited_at":"2015-04-18T23:40:00-03:00","hd_available":true,"hits":1549,"hits_data":{"last_day":3,"last_hour":0,"last_updated_at":1433958848,"last_week":28},"likes":10,"likes_data":{"last_day":0,"last_hour":0,"last_updated_at":1433958848,"last_week":0},"notes":"","program_id":2546,"published_at":"2015-04-19T14:55:47-03:00","queryable":true,"ratings":null,"recommendation_publisher":"webmedia-globotv-intermediate","scheduled_publication_in":null,"scheduled_unpublication_in":null,"status":"published","subscriber_only":true,"tags":["Rede Globo","Zorra Total","dramaturgia","episódio","Séries","entretenimento","quadros","personagens","íntegra"],"title":"Zorra Total - Programa de sábado, 18/04/2015, na íntegra","unpublished_at":"2015-04-19T09:28:22-03:00","updated_at":"2015-04-19T14:55:46-03:00","updated_by":"tvg_tulio_let","url_for_consumption":"http://globotv.globo.com/rede-globo/zorra-total/v/zorra-total-programa-de-sabado-18042015-na-integra/4120444/","videos_ids":[4120439,4120436,4120438],"votes_count":null,"votes_sum":null,"countries":[]},{"id":4120440,"legacy_id":4120440,"_type":"Video","kind":"Video","adult":false,"category":"Entretenimento","channel_id":196,"collaborative_upload_id":null,"collaborative_upload_user":null,"created_at":"2015-04-18T23:48:09-03:00","created_by":"tvg_rosana.araujo_let","cut_format":"trecho","description":"Essa assistente social vai aprontar outra vez","duration":226395,"exhibited_at":"2015-04-18T23:37:08-03:00","hd_available":true,"hits":4429,"hits_data":{"last_day":21,"last_hour":1,"last_updated_at":1434026439,"last_week":61},"likes":58,"likes_data":{"last_day":0,"last_hour":0,"last_updated_at":1434026439,"last_week":0},"notes":null,"program_id":2546,"published_at":"2015-04-18T23:48:41-03:00","queryable":true,"ratings":null,"recommendation_publisher":"webmedia-globotv-intermediate","scheduled_publication_in":null,"scheduled_unpublication_in":null,"status":"published","subscriber_only":false,"tags":["Rede Globo","Zorra Total","dramaturgia","episódio","Séries","entretenimento","quadros","personagens"],"title":"Umbelinda tenta ajudar uma família carente","unpublished_at":null,"updated_at":"2015-04-18T23:50:51-03:00","updated_by":"tvg_rosana.araujo_let","url_for_consumption":"http://globotv.globo.com/rede-globo/zorra-total/v/umbelinda-tenta-ajudar-uma-familia-carente/4120440/","videos_ids":[],"votes_count":null,"votes_sum":null,"countries":[]},{"id":4120431,"legacy_id":4120431,"_type":"Video","kind":"Video","adult":false,"category":"Entretenimento","channel_id":196,"collaborative_upload_id":null,"collaborative_upload_user":null,"created_at":"2015-04-18T23:16:50-03:00","created_by":"tvg_rosana.araujo_let","cut_format":"trecho","description":"Será que eles estão no sertão nordestino?","duration":50109,"exhibited_at":"2015-04-18T23:16:21-03:00","hd_available":true,"hits":5042,"hits_data":{"last_day":1,"last_hour":0,"last_updated_at":1434034592,"last_week":31},"likes":51,"likes_data":{"last_day":0,"last_hour":0,"last_updated_at":1434034592,"last_week":0},"notes":null,"program_id":2546,"published_at":"2015-04-18T23:17:06-03:00","queryable":true,"ratings":null,"recommendation_publisher":"webmedia-globotv-intermediate","scheduled_publication_in":null,"scheduled_unpublication_in":null,"status":"published","subscriber_only":false,"tags":["Rede Globo","Zorra Total","dramaturgia","episódio","Séries","entretenimento","quadros","personagens"],"title":"Família sofre com a estiagem","unpublished_at":null,"updated_at":"2015-04-18T23:17:47-03:00","updated_by":"tvg_rosana.araujo_let","url_for_consumption":"http://globotv.globo.com/rede-globo/zorra-total/v/familia-sofre-com-a-estiagem/4120431/","videos_ids":[],"votes_count":null,"votes_sum":null,"countries":[]},{"id":4120429,"legacy_id":4120429,"_type":"Video","kind":"Video","adult":false,"category":"Entretenimento","channel_id":196,"collaborative_upload_id":null,"collaborative_upload_user":null,"created_at":"2015-04-18T23:15:21-03:00","created_by":"tvg_rosana.araujo_let","cut_format":"trecho","description":"Ela tenta fazer ele entender o que ela quer dizes, mas está difícil!","duration":54242,"exhibited_at":"2015-04-18T23:13:14-03:00","hd_available":true,"hits":3111,"hits_data":{"last_day":5,"last_hour":0,"last_updated_at":1434034160,"last_week":35},"likes":23,"likes_data":{"last_day":0,"last_hour":0,"last_updated_at":1434034160,"last_week":0},"notes":null,"program_id":2546,"published_at":"2015-04-18T23:15:36-03:00","queryable":true,"ratings":null,"recommendation_publisher":"webmedia-globotv-intermediate","scheduled_publication_in":null,"scheduled_unpublication_in":null,"status":"published","subscriber_only":false,"tags":["Rede Globo","Zorra Total","dramaturgia","episódio","Séries","entretenimento","quadros","personagens"],"title":"Mulher perde a paciência com marido que completa todas as suas frases","unpublished_at":null,"updated_at":"2015-04-18T23:16:19-03:00","updated_by":"tvg_rosana.araujo_let","url_for_consumption":"http://globotv.globo.com/rede-globo/zorra-total/v/mulher-perde-a-paciencia-com-marido-que-completa-todas-as-suas-frases/4120429/","videos_ids":[],"votes_count":null,"votes_sum":null,"countries":[]},{"id":4120428,"legacy_id":4120428,"_type":"Video","kind":"Video","adult":false,"category":"Entretenimento","channel_id":196,"collaborative_upload_id":null,"collaborative_upload_user":null,"created_at":"2015-04-18T23:15:01-03:00","created_by":"tvg_rosana.araujo_let","cut_format":"trecho","description":"Isso só pode terminar em confusão!","duration":129963,"exhibited_at":"2015-04-18T23:08:57-03:00","hd_available":true,"hits":3098,"hits_data":{"last_day":5,"last_hour":0,"last_updated_at":1434034173,"last_week":32},"likes":23,"likes_data":{"last_day":0,"last_hour":0,"last_updated_at":1434034173,"last_week":1},"notes":null,"program_id":2546,"published_at":"2015-04-18T23:15:21-03:00","queryable":true,"ratings":null,"recommendation_publisher":"webmedia-globotv-intermediate","scheduled_publication_in":null,"scheduled_unpublication_in":null,"status":"published","subscriber_only":false,"tags":["Rede Globo","Zorra Total","dramaturgia","episódio","Séries","entretenimento","quadros","personagens"],"title":"Pai de santo taxista?","unpublished_at":null,"updated_at":"2015-04-18T23:16:41-03:00","updated_by":"tvg_rosana.araujo_let","url_for_consumption":"http://globotv.globo.com/rede-globo/zorra-total/v/pai-de-santo-taxista/4120428/","videos_ids":[],"votes_count":null,"votes_sum":null,"countries":[]}]"""
