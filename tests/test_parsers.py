import pytest

from flaskvel.Parsers.ArrayParser import ArrayParser
from flaskvel.Parsers.PipedStringParser import PipedStringParser
from flaskvel.Parsers.UniversalParser import UniversalParser
from flaskvel.ParsedRule import ParsedRule
from flaskvel import Rules

@pytest.fixture
def array_rules():
	return {
		"username": ["required", "string"],
		"password": ["required", "string", "min:8", "max:32", "confirmed"], 
		"email": [Rules.REQUIRED, Rules.EMAIL]
	}

@pytest.fixture
def piped_string_rules():
	return {
		"username": "required|string",
		"password": "required|string|min:8|max:32|confirmed", 
		"email": "required|email"
	}

@pytest.fixture
def expected_parsed_rules():
	return {
		'username': [ParsedRule('required'), ParsedRule('string')], 
		'password': [ParsedRule('required'), ParsedRule('string'), ParsedRule('min', ['8']), ParsedRule('max', ['32']), ParsedRule('confirmed')],
		'email': [ParsedRule('required'), ParsedRule('email')]
	}

def test_ArrayParser_parse(array_rules, expected_parsed_rules):
	parsed_rules = {}
	for field_name, field_rules in array_rules.items():
		parsed_rules[field_name] = ArrayParser.parse(field_rules)
	assert parsed_rules == expected_parsed_rules

def test_PipedString_parse(piped_string_rules, expected_parsed_rules):
	parsed_rules = {}
	for field_name, field_rules in piped_string_rules.items():
		parsed_rules[field_name] = PipedStringParser.parse(field_rules)
	assert parsed_rules == expected_parsed_rules

def test_UniversalParser_parse(array_rules, piped_string_rules, expected_parsed_rules):
	assert UniversalParser.parse(array_rules) == expected_parsed_rules
	assert UniversalParser.parse(piped_string_rules) == expected_parsed_rules
