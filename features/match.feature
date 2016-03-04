Feature: Match
    
    @int @ok
    Scenario: Should match schema and json with int value
        Given from steps import INT_SCHEMA
        And from steps import INT_JSON
        And I have schema INT_SCHEMA
        And I have JSON INT_JSON
        Then schema INT_SCHEMA should match JSON INT_JSON

    @url @ok
    Scenario: Should match schema and json with url value
        Given from steps import URL_SCHEMA
        And from steps import URL_JSON
        And I have schema URL_SCHEMA
        And I have JSON URL_JSON
        Then schema URL_SCHEMA should match JSON URL_JSON

    @null @ok
    Scenario: Should match schema and json with null value
        Given from steps import NULL_SCHEMA
        And from steps import NULL_JSON
        And I have schema NULL_SCHEMA
        And I have JSON NULL_JSON
        Then schema NULL_SCHEMA should match JSON NULL_JSON

    @url @or @null @ok
    Scenario: Should match schema and json with url or null value
        Given from steps import URL_OR_NULL_SCHEMA
        And from steps import URL_JSON
        And from steps import NULL_JSON
        And I have schema URL_OR_NULL_SCHEMA
        And I have JSON URL_JSON
        Then schema URL_OR_NULL_SCHEMA should match JSON URL_JSON
        Given I have JSON NULL_JSON
        Then schema URL_OR_NULL_SCHEMA should match JSON NULL_JSON

    @int @fail
    Scenario: Should not match schema and json with int value
        Given from steps import INT_SCHEMA
        And from steps import STR_JSON
        And I have schema INT_SCHEMA
        And I have JSON STR_JSON
        Then schema INT_SCHEMA should not match JSON STR_JSON

    @dict @ok
    Scenario: Should match schema and json with hash structure
        Given from steps import DICT_SCHEMA_A
        And from steps import DICT_JSON_A
        And I have schema DICT_SCHEMA_A
        And I have JSON DICT_JSON_A
        Then schema DICT_SCHEMA_A should match JSON DICT_JSON_A

    @dict @fail
    Scenario: Should not match schema and json with hash structure
        Given from steps import DICT_SCHEMA_A
        And from steps import DICT_JSON_B
        And from steps import DICT_JSON_C
        And I have schema DICT_SCHEMA_A
        And I have JSON DICT_JSON_B
        And I have JSON DICT_JSON_C
        Then schema DICT_SCHEMA_A should not match JSON DICT_JSON_B
        Then schema DICT_SCHEMA_A should not match JSON DICT_JSON_C


    @python @safe
    Scenario: Should not match schema and json with python code due security check
        Given from steps import PYTHON_SCHEMA
        Then I can't have schema PYTHON_SCHEMA

    @python @unsafe @ok
    Scenario: Should match schema and json with python code
        Given from steps import PYTHON_SCHEMA
        And from steps import PYTHON_JSON
        And I have unsafe schema PYTHON_SCHEMA
        And I have JSON PYTHON_JSON
        Then schema PYTHON_SCHEMA should match JSON PYTHON_JSON

    @python @unsafe @fail
    Scenario: Should not match schema and json with python code
        Given from steps import PYTHON_SCHEMA
        And from steps import PYTHON_FAIL_JSON
        And I have unsafe schema PYTHON_SCHEMA
        And I have JSON PYTHON_FAIL_JSON
        Then schema PYTHON_SCHEMA should not match JSON PYTHON_FAIL_JSON
