Feature: Match
    
    @int @ok
    Scenario: Should match schema and json
        Given from steps import INT_SCHEMA
        And from steps import INT_JSON
        And I have schema INT_SCHEMA
        And I have JSON INT_JSON
        Then schema INT_SCHEMA should match JSON INT_JSON

    @int @fail
    Scenario: Should match schema and json
        Given from steps import INT_SCHEMA
        And from steps import STR_JSON
        And I have schema INT_SCHEMA
        And I have JSON STR_JSON
        Then schema INT_SCHEMA should not match JSON STR_JSON

    @dict @ok
    Scenario: Should match schema and json
        Given from steps import DICT_SCHEMA_A
        And from steps import DICT_JSON_A
        And I have schema DICT_SCHEMA_A
        And I have JSON DICT_JSON_A
        Then schema DICT_SCHEMA_A should match JSON DICT_JSON_A

    @dict @fail
    Scenario: Should match schema and json
        Given from steps import DICT_SCHEMA_A
        And from steps import DICT_JSON_B
        And from steps import DICT_JSON_C
        And I have schema DICT_SCHEMA_A
        And I have JSON DICT_JSON_B
        And I have JSON DICT_JSON_C
        Then schema DICT_SCHEMA_A should not match JSON DICT_JSON_B
        Then schema DICT_SCHEMA_A should not match JSON DICT_JSON_C
