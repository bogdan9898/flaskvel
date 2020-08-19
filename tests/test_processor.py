import pytest

from flaskvel.Processor import Processor
from flaskvel import Validator
from flaskvel import FieldTypes
from flaskvel.ParsedRule import ParsedRule

from tests.test_processor_handlers import generate_processor, mockup_files

def generic_test(data, func):
	count = len(data['input'])
	input_data = data['input']
	expected_types = data['expected']

	for i in range(count):
		processor = generate_processor(**input_data[i])
		output_data = getattr(processor, func)('field')
		assert output_data == expected_types[i]

# ==================================================================================================== #

@pytest.fixture
def get_field_type_data():
	return {
		"input": [
			{
				'rules': {
				},
				'values': {
					'field': 1
				}
			},
			{
				'rules': {
					'field': 'integer'
				},
				'values': {
					'field': '1'
				}
			},
			{
				'rules': {
				},
				'values': {
					'field': '1'
				}
			},
			{
				'rules': {
					'field': 'string'
				},
				'values': {
					'field': '1'
				}
			},
			{
				'rules': {
				},
				'values': {
					'field': [0,1,2]
				}
			},
			{
				'rules': {
				},
				'values': {
					'field': '[0,1,2]'
				}
			},
			{
				'rules': {
					'field': 'array'
				},
				'values': {
					'field': '[0,1,2]'
				}
			},
			{
				'rules': {
					'field': 'json'
				},
				'values': {
					'field': {"a":0,"b":1,"c":[0,1,2]}
				}
			},
			{
				'rules': {
					'field': 'json'
				},
				'values': {
					'field': '{"a":0,"b":1,"c":[0,1,2]}'
				}
			},
			{
				'rules': {
				},
				'values': {
					'field': '{"a":0,"b":1,"c":[0,1,2]}'
				}
			},
			{
				'rules': {
					'field': 'string'
				},
				'values': {
					'field': 1234
				}
			},
		],

		"expected": [
			FieldTypes.NUMERIC,
			FieldTypes.NUMERIC,
			FieldTypes.NUMERIC,
			FieldTypes.STRING,
			FieldTypes.ARRAY,
			FieldTypes.ARRAY,
			FieldTypes.ARRAY,
			FieldTypes.JSON,
			FieldTypes.JSON,
			FieldTypes.JSON,
			FieldTypes.UNKOWN
		],
	}

def test_get_field_type(get_field_type_data):
	generic_test(get_field_type_data, 'get_field_type')

# ==================================================================================================== #

@pytest.fixture
def get_field_value_data():
	return {
		"input": [
			{
				'rules': {
				},
				'values': {
					'field': 1
				}
			},
			{
				'rules': {
				},
				'values': {
					'field': [0,1,2]
				}
			},
			{
				'rules': {
					'field': 'json'
				},
				'values': {
					'field': {"a":0,"b":1,"c":[0,1,2]}
				}
			},
			{
				'rules': {
					'field': 'string'
				},
				'values': {
					'field': 1234
				}
			},
		],

		"expected": [
			1,
			[0,1,2],
			{"a":0,"b":1,"c":[0,1,2]},
			1234
		],
	}

def test_get_field_value(get_field_value_data):
	generic_test(get_field_value_data, 'get_field_value')

# ==================================================================================================== #

@pytest.fixture
def get_field_rules_data():
	return {
		"input": [
			{
				'rules': {
				},
				'values': {
					'field': 1
				}
			},
			{
				'rules': {
					'field': 'required|array|size:3'
				},
				'values': {
					'field': [0,1,2]
				}
			},
			{
				'rules': {
					'field': ['json', 'nullable']
				},
				'values': {
					'field': {"a":0,"b":1,"c":[0,1,2]}
				}
			},
			{
				'rules': {
					'field': ['bail', 'string', 'min:2']
				},
				'values': {
					'field': 1234
				}
			},
		],

		"expected": [
			[],
			[ParsedRule('required'), ParsedRule('array'), ParsedRule('size', ['3'])],
			[ParsedRule('json'), ParsedRule('nullable')],
			[ParsedRule('bail'), ParsedRule('string'), ParsedRule('min', ['2'])],
		],
	}

def test_get_field_rules(get_field_rules_data):
	generic_test(get_field_rules_data, 'get_field_rules')

# ==================================================================================================== #

@pytest.fixture
def is_field_present_data():
	return {
		"input": [
			{
				'rules': {
				},
				'values': {
					'field': 1
				}
			},
			{
				'rules': {
				},
				'values': {
					'field': None
				}
			},
			{
				'rules': {
				},
				'values': {
				}
			},
		],

		"expected": [
			True,
			True,
			False
		],
	}

def test_is_field_present(is_field_present_data):
	generic_test(is_field_present_data, 'is_field_present')

# ==================================================================================================== #

@pytest.fixture
def is_field_nullable_data():
	return {
		"input": [
			{
				'rules': {
					'field': 'nullable'
				},
				'values': {
					'field': 1
				}
			},
			{
				'rules': {
					'field': ['required', 'nullable']
				},
				'values': {
					'field': 1
				}
			},
			{
				'rules': {
				},
				'values': {
					'field': 1
				}
			},
		],

		"expected": [
			True,
			True,
			False
		],
	}

def test_is_field_nullable(is_field_nullable_data):
	generic_test(is_field_nullable_data, 'is_field_nullable')

# ==================================================================================================== #

@pytest.fixture
def is_field_empty_data():
	return {
		"input": [
			{
				'rules': {
				},
				'values': {
					'field': 1
				}
			},
			{
				'rules': {
				},
				'values': {
					'field': ''
				}
			},
			{
				'rules': {
				},
				'values': {
					'field': []
				}
			},
			{
				'rules': {
				},
				'values': {
					'field': {}
				}
			},
			{
				'rules': {
				},
				'values': {
					'field': mockup_files['0kb']
				}
			},
		],

		"expected": [
			False,
			True,
			True,
			True,
			True,
		],
	}

def test_is_field_empty(is_field_empty_data):
	generic_test(is_field_empty_data, 'is_field_empty')

# ==================================================================================================== #

@pytest.fixture
def should_bail_data():
	return {
		"input": [
			{
				'rules': {
					'field': ['integer', 'bail']
				},
				'values': {
					'field': 1
				}
			},
			{
				'rules': {
					'field': ['integer']
				},
				'values': {
					'field': 1
				}
			},
		],

		"expected": [
			True,
			False,
		],
	}

def test_should_bail(should_bail_data):
	generic_test(should_bail_data, 'should_bail')

# ==================================================================================================== #
