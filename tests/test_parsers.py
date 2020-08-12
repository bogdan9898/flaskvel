from flaskvel.Parsers import ArrayParser, PipedStringParser
from flaskvel import Rules

import pytest

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


def test_ArrayParser_parse():
	parsed_rules = {}
	for field_name, field_rules in array_rules.items():
		parsed_rules[field_name] = ArrayParser.parse(field_rules)
	print(parsed_rules)
	assert True


def test_PipedString_parse(rules):
	pass

