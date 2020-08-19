import pytest

from werkzeug.datastructures import FileStorage

from flaskvel.Processor import Processor
from flaskvel import Validator
from flaskvel.Parsers.UniversalParser import UniversalParser

mockup_files = {
	'0kb': FileStorage(
		stream=open('tests/files/file_0kb', 'rb'),
		filename='tests/files/file_0kb',
		content_type='text/plain',
		name='field'
	),
	'1kb': FileStorage(
		stream=open('tests/files/file_1kb', 'rb'),
		filename='tests/files/file_1kb',
		content_type='text/plain',
		name='field'
	),
	'2kb': FileStorage(
		stream=open('tests/files/file_2kb', 'rb'),
		filename='tests/files/file_2kb',
		content_type='text/plain',
		name='field'
	),
	'3kb': FileStorage(
		stream=open('tests/files/file_3kb', 'rb'),
		filename='tests/files/file_3kb',
		content_type='text/plain',
		name='field'
	),
	'4kb': FileStorage(
		stream=open('tests/files/file_4kb', 'rb'),
		filename='tests/files/file_4kb',
		content_type='text/plain',
		name='field'
	),
	'alphabet': FileStorage(
		stream=open('tests/files/file_alphabet', 'rb'),
		filename='tests/files/file_alphabet',
		content_type='text/plain',
		name='field'
	),

	'json': FileStorage(
		stream=open('tests/files/file_json', 'rb'),
		filename='tests/files/file_json',
		content_type='application/json',
		name='field'
	),

	'image': FileStorage(
		stream=open('tests/files/photo1.webp', 'rb'),
		filename='tests/files/photo1.webp',
		content_type='image/webp',
		name='field'
	),
	'1280x720': FileStorage(
		stream=open('tests/files/photo2.jpg', 'rb'),
		filename='tests/files/photo2.jpg',
		content_type='image/jpeg',
		name='field'
	),
	'1920x1080': FileStorage(
		stream=open('tests/files/photo3.jpg', 'rb'),
		filename='tests/files/photo3.jpg',
		content_type='image/jpeg',
		name='field'
	),
	'1000x1000': FileStorage(
		stream=open('tests/files/photo4.jpg', 'rb'),
		filename='tests/files/photo4.jpg',
		content_type='image/jpeg',
		name='field'
	),
}

class RequestMockup:
	def __init__(self, json, form, files):
		self.json = json
		self.is_json = json is not None
		self.form = form
		self.files = files

def generate_processor(rules, values, files=[]):
	request = RequestMockup(form=values, json=None, files=[files])
	validator = Validator(request=request)
	validator.rules = rules
	validator._parsed_rules = UniversalParser.parse(rules)
	processor = validator._processor
	# update critical data
	processor._messages = validator.get_messages()
	processor._parsed_rules = validator.get_parsed_rules()
	return processor

def generic_test(pass_data, fail_data):
	# pass_data
	if isinstance(pass_data, dict):
		pass_data = [pass_data]
	assert isinstance(pass_data, list) == True
	for data in pass_data:
		parsed_rules = UniversalParser.parse(data['rules'])
		for field_name, rules_list in parsed_rules.items():
			value = data['values'].get(field_name)
			processor = generate_processor(**data)
			for rule in rules_list:
				params = rule.get_params()
				handler = processor._get_rule_handler(rule.get_predicate())
				assert handler(field_name=field_name, value=value, params=params) == True
	# fail_data
	if isinstance(fail_data, dict):
		fail_data = [fail_data]
	assert isinstance(fail_data, list) == True
	for data in fail_data:
		parsed_rules = UniversalParser.parse(data['rules'])
		for field_name, rules_list in parsed_rules.items():
			value = data['values'].get(field_name)
			processor = generate_processor(**data)
			for rule in rules_list:
				params = rule.get_params()
				handler = processor._get_rule_handler(rule.get_predicate())
				assert handler(field_name=field_name, value=value, params=params) == False

# ==================================================================================================== #

@pytest.fixture
def pass_data_accepted():
	return {
		'rules': {
			'field': 'accepted'
		},
		'values': {
			'field': 1
		}
	}

@pytest.fixture
def fail_data_accepted():
	return {
		'rules': {
			'field': 'accepted'
		},
		'values': {
			'field': 'nothing here'
		}
	}

def test_handler_accepted(pass_data_accepted, fail_data_accepted):
	generic_test(pass_data_accepted, fail_data_accepted)

# ==================================================================================================== #

@pytest.fixture
def pass_data_active_url():
	return {
		'rules': {
			'field': 'active_url'
		},
		'values': {
			'field': 'https://google.com'
		}
	}

@pytest.fixture
def fail_data_active_url():
	return [
		{
			'rules': {
				'field': 'active_url'
			},
			'values': {
				'field': 'google.com'
			}
		},
		{
			'rules': {
				'field': 'active_url'
			},
			'values': {
				'field': 'www.google.com'
			}
		},
		{
			'rules': {
				'field': 'active_url'
			},
			'values': {
				'field': 1234
			}
		}
	]

def test_handler_active_url(pass_data_active_url, fail_data_active_url):
	generic_test(pass_data_active_url, fail_data_active_url)

# ==================================================================================================== #

@pytest.fixture
def pass_data_after():
	return {
		'rules': {
			'field': 'after:2020-07-10'
		},
		'values': {
			'field': '2020-07-11'
		}
	}

@pytest.fixture
def fail_data_after():
	return [
		{
			'rules': {
				'field': 'after:2020-07-10'
			},
			'values': {
				'field': '2020-07-9'
			}
		},
		{
			'rules': {
				'field': 'after:2020-07-10'
			},
			'values': {
				'field': '2020-07-10'
			}
		}
	]

def test_handler_after(pass_data_after, fail_data_after):
	generic_test(pass_data_after, fail_data_after)

# ==================================================================================================== #

@pytest.fixture
def pass_data_after_or_equal():
	return [
		{
			'rules': {
				'field': 'after_or_equal:2020-07-10'
			},
			'values': {
				'field': '2020-07-10'
			}
		},
		{
			'rules': {
				'field': 'after_or_equal:2020-07-10'
			},
			'values': {
				'field': '2020-07-11'
			}
		}
	]

@pytest.fixture
def fail_data_after_or_equal():
	return {
		'rules': {
			'field': 'after_or_equal:2020-07-10'
		},
		'values': {
			'field': '2020-07-9'
		}
	}

def test_handler_after_or_equal(pass_data_after_or_equal, fail_data_after_or_equal):
	generic_test(pass_data_after_or_equal, fail_data_after_or_equal)

# ==================================================================================================== #

@pytest.fixture
def pass_data_alpha():
	return {
		'rules': {
			'field': 'alpha'
		},
		'values': {
			'field': 'abcd'
		}
	}

@pytest.fixture
def fail_data_alpha():
	return {
		'rules': {
			'field': 'alpha'
		},
		'values': {
			'field': 'abcd1234'
		}
	}

def test_handler_alpha(pass_data_alpha, fail_data_alpha):
	generic_test(pass_data_alpha, fail_data_alpha)

# ==================================================================================================== #

@pytest.fixture
def pass_data_alpha_dash():
	return {
		'rules': {
			'field': 'alpha_dash'
		},
		'values': {
			'field': 'ab-cd_ef'
		}
	}

@pytest.fixture
def fail_data_alpha_dash():
	return {
		'rules': {
			'field': 'alpha_dash'
		},
		'values': {
			'field': 'abcd.ef'
		}
	}

def test_handler_alpha_dash(pass_data_alpha_dash, fail_data_alpha_dash):
	generic_test(pass_data_alpha_dash, fail_data_alpha_dash)

# ==================================================================================================== #

@pytest.fixture
def pass_data_alpha_num():
	return {
		'rules': {
			'field': 'alpha_num'
		},
		'values': {
			'field': 'ab12cd34'
		}
	}

@pytest.fixture
def fail_data_alpha_num():
	return {
		'rules': {
			'field': 'alpha_num'
		},
		'values': {
			'field': 'abcd_1234'
		}
	}

def test_handler_alpha_num(pass_data_alpha_num, fail_data_alpha_num):
	generic_test(pass_data_alpha_num, fail_data_alpha_num)

# ==================================================================================================== #

@pytest.fixture
def pass_data_array():
	return [
		{
			'rules': {
				'field': 'array'
			},
			'values': {
				'field': [1,2,3]
			}
		},
		{
			'rules': {
				'field': 'array'
			},
			'values': {
				'field': '[1,2,3]'
			}
		},
	]

@pytest.fixture
def fail_data_array():
	return [
		{
			'rules': {
				'field': 'array'
			},
			'values': {
				'field': 1
			}
		},
		{
			'rules': {
				'field': 'array'
			},
			'values': {
				'field': '[1,2,3'
			}
		},
	]

def test_handler_array(pass_data_array, fail_data_array):
	generic_test(pass_data_array, fail_data_array)

# ==================================================================================================== #

@pytest.fixture
def pass_data_before():
	return {
		'rules': {
			'field': 'before:2020-07-20'
		},
		'values': {
			'field': '2020-07-12'
		}
	}

@pytest.fixture
def fail_data_before():
	return [
		{
			'rules': {
				'field': 'before:2020-07-20'
			},
			'values': {
				'field': '2020-07-21'
			}
		},
		{
			'rules': {
				'field': 'before:2020-07-20'
			},
			'values': {
				'field': '2020-07-20'
			}
		},
	]

def test_handler_before(pass_data_before, fail_data_before):
	generic_test(pass_data_before, fail_data_before)

# ==================================================================================================== #

@pytest.fixture
def pass_data_before_or_equal():
	return [
		{
			'rules': {
				'field': 'before_or_equal:2020-07-10'
			},
			'values': {
				'field': '2020-07-10'
			}
		},
		{
			'rules': {
				'field': 'before_or_equal:2020-07-10'
			},
			'values': {
				'field': '2020-07-9'
			}
		}
	]

@pytest.fixture
def fail_data_before_or_equal():
	return {
		'rules': {
			'field': 'before_or_equal:2020-07-10'
		},
		'values': {
			'field': '2020-07-11'
		}
	}

def test_handler_before_or_equal(pass_data_before_or_equal, fail_data_before_or_equal):
	generic_test(pass_data_before_or_equal, fail_data_before_or_equal)

# ==================================================================================================== #

@pytest.fixture
def pass_data_between():
	return [
		{
			'rules': {
				'field': 'between:1,3'
			},
			'values': {
				'field': 'a'
			}
		},
		{
			'rules': {
				'field': 'between:1,3'
			},
			'values': {
				'field': 'ab'
			}
		},
		{
			'rules': {
				'field': 'between:1,3'
			},
			'values': {
				'field': 'abc'
			}
		},
		{
			'rules': {
				'field': 'between:1,3'
			},
			'values': {
				'field': 1
			}
		},
		{
			'rules': {
				'field': 'between:1,3'
			},
			'values': {
				'field': 2
			}
		},
		{
			'rules': {
				'field': 'between:1,3'
			},
			'values': {
				'field': 3
			}
		},
		{
			'rules': {
				'field': 'between:1,3'
			},
			'values': {
				'field': [0]
			}
		},
		{
			'rules': {
				'field': 'between:1,3'
			},
			'values': {
				'field': [0, 1]
			}
		},
		{
			'rules': {
				'field': 'between:1,3'
			},
			'values': {
				'field': [0, 1, 2]
			}
		},
		{
			'rules': {
				'field': 'between:1,3'
			},
			'values': {
				'field': {"a":0}
			}
		},
		{
			'rules': {
				'field': 'between:1,3'
			},
			'values': {
				'field': {"a":0, "b":1}
			}
		},
		{
			'rules': {
				'field': 'between:1,3'
			},
			'values': {
				'field': {"a":0, "b":1, "c":2}
			}
		},
		{
			'rules': {
				'field': 'between:1,3'
			},
			'values': {
				'field': mockup_files['1kb']
			}
		},
		{
			'rules': {
				'field': 'between:1,3'
			},
			'values': {
				'field': mockup_files['2kb']
			}
		},
		{
			'rules': {
				'field': 'between:1,3'
			},
			'values': {
				'field': mockup_files['3kb']
			}
		},
	]

@pytest.fixture
def fail_data_between():
	return [
		{
			'rules': {
				'field': 'between:1,3'
			},
			'values': {
				'field': ''
			}
		},
		{
			'rules': {
				'field': 'between:1,3'
			},
			'values': {
				'field': 'abcd'
			}
		},
		{
			'rules': {
				'field': 'between:1,3'
			},
			'values': {
				'field': 0
			}
		},
		{
			'rules': {
				'field': 'between:1,3'
			},
			'values': {
				'field': 4
			}
		},
		{
			'rules': {
				'field': 'between:1,3'
			},
			'values': {
				'field': []
			}
		},
		{
			'rules': {
				'field': 'between:1,3'
			},
			'values': {
				'field': [0, 1, 2, 3]
			}
		},
		{
			'rules': {
				'field': 'between:1,3'
			},
			'values': {
				'field': {}
			}
		},
		{
			'rules': {
				'field': 'between:1,3'
			},
			'values': {
				'field': {"a":0, "b":1, "c":2, "d":3}
			}
		},
		{
			'rules': {
				'field': 'between:1,3'
			},
			'values': {
				'field': mockup_files['0kb']
			}
		},
		{
			'rules': {
				'field': 'between:1,3'
			},
			'values': {
				'field': mockup_files['4kb']
			}
		},
	]

def test_handler_between(pass_data_between, fail_data_between):
	generic_test(pass_data_between, fail_data_between)

# ==================================================================================================== #

@pytest.fixture
def pass_data_boolean():
	return {
		'rules': {
			'field': 'boolean'
		},
		'values': {
			'field': 'true'
		}
	}

@pytest.fixture
def fail_data_boolean():
	return {
		'rules': {
			'field': 'boolean'
		},
		'values': {
			'field': 'test'
		}
	}

def test_handler_boolean(pass_data_boolean, fail_data_boolean):
	generic_test(pass_data_boolean, fail_data_boolean)

# ==================================================================================================== #

@pytest.fixture
def pass_data_confirmed():
	return {
		'rules': {
			'field': 'confirmed'
		},
		'values': {
			'field': 'value1',
			'field_confirmation': 'value1'
		}
	}

@pytest.fixture
def fail_data_confirmed():
	return [
		{
			'rules': {
				'field': 'confirmed'
			},
			'values': {
				'field': 'value1',
				'field_confirmation': 'VALUE'
			}
		},
		{
			'rules': {
				'field': 'confirmed'
			},
			'values': {
				'field': 'value1',
			}
		}
	]

def test_handler_confirmed(pass_data_confirmed, fail_data_confirmed):
	generic_test(pass_data_confirmed, fail_data_confirmed)

# ==================================================================================================== #

@pytest.fixture
def pass_data_date():
	return {
		'rules': {
			'field': 'date'
		},
		'values': {
			'field': '2020-08-16'
		}
	}

@pytest.fixture
def fail_data_date():
	return {
		'rules': {
			'field': 'date'
		},
		'values': {
			'field': 'not a date'
		}
	}

def test_handler_date(pass_data_date, fail_data_date):
	generic_test(pass_data_date, fail_data_date)

# ==================================================================================================== #

@pytest.fixture
def pass_data_date_equals():
	return {
		'rules': {
			'field': 'date_equals:2020-07-16'
		},
		'values': {
			'field': '2020-07-16'
		}
	}

@pytest.fixture
def fail_data_date_equals():
	return [
		{
			'rules': {
				'field': 'date_equals:2020-07-16'
			},
			'values': {
				'field': '2020-07-15'
			}
		},
		{
			'rules': {
				'field': 'date_equals:2020-07-16'
			},
			'values': {
				'field': '2020-07-17'
			}
		}
	]

def test_handler_date_equals(pass_data_date_equals, fail_data_date_equals):
	generic_test(pass_data_date_equals, fail_data_date_equals)

# ==================================================================================================== #

@pytest.fixture
def pass_data_date_format():
	return {
		'rules': {
			'field': 'date_format:%d-%m-%Y'
		},
		'values': {
			'field': '16-08-2020'
		}
	}

@pytest.fixture
def fail_data_date_format():
	return [
		{
			'rules': {
				'field': 'date_format:%d-%m-%Y'
			},
			'values': {
				'field': 'not a date'
			}
		},
		{
			'rules': {
				'field': 'date_format:%d-%m-%Y'
			},
			'values': {
				'field': '2020-08-16'
			}
		}
	]

def test_handler_date_format(pass_data_date_format, fail_data_date_format):
	generic_test(pass_data_date_format, fail_data_date_format)

# ==================================================================================================== #

@pytest.fixture
def pass_data_different():
	return {
		'rules': {
			'field1': 'different:field2,field3'
		},
		'values': {
			'field1': 1,
			'field2': 2,
			'field3': 'three',
		}
	}

@pytest.fixture
def fail_data_different():
	return {
		'rules': {
			'field1': 'different:field2,field3'
		},
		'values': {
			'field1': 1,
			'field2': 1,
			'field3': 'three',
		}
	}

def test_handler_different(pass_data_different, fail_data_different):
	generic_test(pass_data_different, fail_data_different)

# ==================================================================================================== #

@pytest.fixture
def pass_data_digits():
	return [
		{
			'rules': {
				'field': 'digits:3'
			},
			'values': {
				'field': 123
			}
		},
		{
			'rules': {
				'field': 'digits:3'
			},
			'values': {
				'field': '123'
			}
		}
	]

@pytest.fixture
def fail_data_digits():
	return [
		{
			'rules': {
				'field': "digits:3"
			},
			'values': {
				'field': 1
			}
		},
		{
			'rules': {
				'field': "digits:3"
			},
			'values': {
				'field': '1'
			}
		},
		{
			'rules': {
				'field': "digits:3"
			},
			'values': {
				'field': 'abcd'
			}
		}
	]

def test_handler_digits(pass_data_digits, fail_data_digits):
	generic_test(pass_data_digits, fail_data_digits)

# ==================================================================================================== #

@pytest.fixture
def pass_data_digits_between():
	return [
		{
			'rules': {
				'field': "digits_between:2,5"
			},
			'values': {
				'field': 123
			}
		},
		{
			'rules': {
				'field': "digits_between:2,5"
			},
			'values': {
				'field':'123'
			}
		}
	]

@pytest.fixture
def fail_data_digits_between():
	return [
		{
			'rules': {
				'field': "digits_between:2,5"
			},
			'values': {
				'field': 1
			}
		},
		{
			'rules': {
				'field': "digits_between:2,5"
			},
			'values': {
				'field':'1'
			}
		},
		{
			'rules': {
				'field': "digits_between:2,5"
			},
			'values': {
				'field': 'abcd'
			}
		},
	]

def test_handler_digits_between(pass_data_digits_between, fail_data_digits_between):
	generic_test(pass_data_digits_between, fail_data_digits_between)

# ==================================================================================================== #

@pytest.fixture
def pass_data_dimensions():
	return [
		{
			'rules': {
				'field': 'dimensions:ratio=16/9'
			},
			'values': {
				'field': mockup_files['1280x720']
			}
		},
		{
			'rules': {
				'field': 'dimensions:min_width=1280'
			},
			'values': {
				'field': mockup_files['1280x720']
			}
		},
		{
			'rules': {
				'field': 'dimensions:min_height=1000'
			},
			'values': {
				'field': mockup_files['1000x1000']
			}
		},
		{
			'rules': {
				'field': 'dimensions:min_width=1280,min_height=1000'
			},
			'values': {
				'field': mockup_files['1920x1080']
			}
		},
		{
			'rules': {
				'field': 'dimensions:width=1280'
			},
			'values': {
				'field': mockup_files['1280x720']
			}
		},
		{
			'rules': {
				'field': 'dimensions:height=1000'
			},
			'values': {
				'field': mockup_files['1000x1000']
			}
		},
		{
			'rules': {
				'field': 'dimensions:width=1280,height=720'
			},
			'values': {
				'field': mockup_files['1280x720']
			}
		},
		{
			'rules': {
				'field': 'dimensions:max_width=1280'
			},
			'values': {
				'field': mockup_files['1000x1000']
			}
		},
		{
			'rules': {
				'field': 'dimensions:max_height=1000'
			},
			'values': {
				'field': mockup_files['1280x720']
			}
		},
		{
			'rules': {
				'field': 'dimensions:max_width=1920,max_height=1080'
			},
			'values': {
				'field': mockup_files['1920x1080']
			}
		},
	]

@pytest.fixture
def fail_data_dimensions():
	return [
		{
			'rules': {
				'field': 'dimensions:ratio=16/9'
			},
			'values': {
				'field': mockup_files['1000x1000']
			}
		},
		{
			'rules': {
				'field': 'dimensions:min_width=1280'
			},
			'values': {
				'field': mockup_files['1000x1000']
			}
		},
		{
			'rules': {
				'field': 'dimensions:min_height=1000'
			},
			'values': {
				'field': mockup_files['1280x720']
			}
		},
		{
			'rules': {
				'field': 'dimensions:min_width=1280,min_height=1000'
			},
			'values': {
				'field': mockup_files['1000x1000']
			}
		},
		{
			'rules': {
				'field': 'dimensions:width=1280'
			},
			'values': {
				'field': mockup_files['1000x1000']
			}
		},
		{
			'rules': {
				'field': 'dimensions:height=1000'
			},
			'values': {
				'field': mockup_files['1280x720']
			}
		},
		{
			'rules': {
				'field': 'dimensions:width=1280,height=720'
			},
			'values': {
				'field': mockup_files['1920x1080']
			}
		},
		{
			'rules': {
				'field': 'dimensions:max_width=1280'
			},
			'values': {
				'field': mockup_files['1920x1080']
			}
		},
		{
			'rules': {
				'field': 'dimensions:max_height=1000'
			},
			'values': {
				'field': mockup_files['1920x1080']
			}
		},
		{
			'rules': {
				'field': 'dimensions:max_width=1280,max_height=1000'
			},
			'values': {
				'field': mockup_files['1920x1080']
			}
		},
	]

def test_handler_dimensions(pass_data_dimensions, fail_data_dimensions):
	generic_test(pass_data_dimensions, fail_data_dimensions)

# ==================================================================================================== #

@pytest.fixture
def pass_data_distinct():
	return [
		{
			'rules': {
				'field': 'distinct'
			},
			'values': {
				'field': [1,2,3]
			}
		},
		{
			'rules': {
				'field': 'distinct'
			},
			'values': {
				'field': 'not an array'
			}
		}
	]

@pytest.fixture
def fail_data_distinct():
	return {
		'rules': {
			'field': 'distinct'
		},
		'values': {
			'field': [1,1,2,3]
		}
	}

def test_handler_distinct(pass_data_distinct, fail_data_distinct):
	generic_test(pass_data_distinct, fail_data_distinct)

# ==================================================================================================== #

@pytest.fixture
def pass_data_email():
	return {
		'rules': {
			'field': 'email'
		},
		'values': {
			'field': 'email@example.com'
		}
	}

@pytest.fixture
def fail_data_email():
	return {
		'rules': {
			'field': 'email'
		},
		'values': {
			'field': 'not an email'
		}
	}

def test_handler_email(pass_data_email, fail_data_email):
	generic_test(pass_data_email, fail_data_email)

# ==================================================================================================== #

@pytest.fixture
def pass_data_ends_with():
	return [
		{
			'rules': {
				'field': 'ends_with:z'
			},
			'values': {
				'field': 'wxyz'
			}
		},
		{
			'rules': {
				'field': 'ends_with:9'
			},
			'values': {
				'field': 6789
			}
		},
		{
			'rules': {
				'field': 'ends_with:c'
			},
			'values': {
				'field': ['a', 'b', 'c']
			}
		},
		{
			'rules': {
				'field': 'ends_with:xyz'
			},
			'values': {
				'field': mockup_files['alphabet']
			}
		},
	]

@pytest.fixture
def fail_data_ends_with():
	return [
		{
			'rules': {
				'field': 'ends_with:a'
			},
			'values': {
				'field': 'bcd'
			}
		},
		{
			'rules': {
				'field': 'ends_with:1'
			},
			'values': {
				'field': 999
			}
		},
		{
			'rules': {
				'field': 'ends_with:a'
			},
			'values': {
				'field': ['b', 'c']
			}
		},
		{
			'rules': {
				'field': 'ends_with:a'
			},
			'values': {
				'field': mockup_files['alphabet']
			}
		},
	]

def test_handler_ends_with(pass_data_ends_with, fail_data_ends_with):
	generic_test(pass_data_ends_with, fail_data_ends_with)

# ==================================================================================================== #

@pytest.fixture
def pass_data_file():
	return [
		{
			'rules': {
				'field': 'file'
			},
			'values': {
				'field': mockup_files['0kb']
			}
		},
		{
			'rules': {
				'field': 'file'
			},
			'values': {
				'field': mockup_files['2kb']
			}
		}
	]

@pytest.fixture
def fail_data_file():
	return [
		{
			'rules': {
				'field': 'file'
			},
			'values': {
				'field': 'abcd'
			}
		},
		{
			'rules': {
				'field': 'file'
			},
			'values': {
				'field': 1234
			}
		},
		{
			'rules': {
				'field': 'file'
			},
			'values': {
				'field': [0, 1]
			}
		},
		{
			'rules': {
				'field': 'file'
			},
			'values': {
				'field': {"a":0, "b":1}
			}
		},
		{
			'rules': {
				'field': 'file'
			},
			'values': {
			}
		}
	]

def test_handler_file(pass_data_file, fail_data_file):
	generic_test(pass_data_file, fail_data_file)

# ==================================================================================================== #

@pytest.fixture
def pass_data_filled():
	return [
		{
			'rules': {
				'field': 'filled'
			},
			'values': {
				'field': 'abcd'
			}
		},
		{
			'rules': {
				'field': 'filled'
			},
			'values': {
			}
		}
	]

@pytest.fixture
def fail_data_filled():
	return {
		'rules': {
			'field': 'filled'
		},
		'values': {
			'field': None
		}
	}

def test_handler_filled(pass_data_filled, fail_data_filled):
	generic_test(pass_data_filled, fail_data_filled)

# ==================================================================================================== #

@pytest.fixture
def pass_data_gt():
	return [
		{
			'rules': {
				'field1': 'gt:field2'
			},
			'values': {
				'field1': 'abc',
				'field2': 'de'
			}
		},
		{
			'rules': {
				'field1': 'gt:field2'
			},
			'values': {
				'field1': 3,
				'field2': 2
			}
		},
		{
			'rules': {
				'field1': 'gt:field2'
			},
			'values': {
				'field1': [0, 1, 2],
				'field2': [0, 1]
			}
		},
		{
			'rules': {
				'field1': 'gt:field2'
			},
			'values': {
				'field1': {"a":0, "b":1, "c":2},
				'field2': {"a":0, "b":1}
			}
		},
		{
			'rules': {
				'field1': 'gt:field2'
			},
			'values': {
				'field1': mockup_files['3kb'],
				'field2': mockup_files['2kb']
			}
		},
	]

@pytest.fixture
def fail_data_gt():
	return [
		{
			'rules': {
				'field1': 'gt:field2'
			},
			'values': {
				'field1': "abcd",
				'field2': 1234
			}
		},
		{
			'rules': {
				'field1': 'gt:field2'
			},
			'values': {
				'field1': 'a',
				'field2': 'de',
			}
		},
		{
			'rules': {
				'field1': 'gt:field2'
			},
			'values': {
				'field1': 'ab',
				'field2': 'de'
			}
		},
		{
			'rules': {
				'field1': 'gt:field2'
			},
			'values': {
				'field1': 1,
				'field2': 2,
			}
		},
		{
			'rules': {
				'field1': 'gt:field2'
			},
			'values': {
				'field1': 2,
				'field2': 2
			}
		},
		{
			'rules': {
				'field1': 'gt:field2'
			},
			'values': {
				'field1': [0],
				'field2': [0, 1],
			}
		},
		{
			'rules': {
				'field1': 'gt:field2'
			},
			'values': {
				'field1': [0, 1],
				'field2': [0, 1]
			}
		},
		{
			'rules': {
				'field1': 'gt:field2'
			},
			'values': {
				'field1': {"a":0},
				'field2': {"a":0, "b":1},
			}
		},
		{
			'rules': {
				'field1': 'gt:field2'
			},
			'values': {
				'field1': {"a":0, "b":1},
				'field2': {"a":0, "b":1}
			}
		},
		{
			'rules': {
				'field1': 'gt:field2'
			},
			'values': {
				'field1': mockup_files['1kb'],
				'field2': mockup_files['2kb'],
			}
		},
		{
			'rules': {
				'field1': 'gt:field2'
			},
			'values': {
				'field1': mockup_files['2kb'],
				'field2': mockup_files['2kb']
			}
		},
	]

def test_handler_gt(pass_data_gt, fail_data_gt):
	generic_test(pass_data_gt, fail_data_gt)

# ==================================================================================================== #

@pytest.fixture
def pass_data_gte():
	return [
		{
			'rules': {
				'field1': 'gte:field2'
			},
			'values': {
				'field1': 'ab',
				'field2': 'de'
			}
		},
		{
			'rules': {
				'field1': 'gte:field2'
			},
			'values': {
				'field1': 'abc',
				'field2': 'de'
			}
		},
		{
			'rules': {
				'field1': 'gte:field2'
			},
			'values': {
				'field1': 2,
				'field2': 2
			}
		},
		{
			'rules': {
				'field1': 'gte:field2'
			},
			'values': {
				'field1': 3,
				'field2': 2
			}
		},
		{
			'rules': {
				'field1': 'gte:field2'
			},
			'values': {
				'field1': [0, 1],
				'field2': [0, 1]
			}
		},
		{
			'rules': {
				'field1': 'gte:field2'
			},
			'values': {
				'field1': [0, 1, 2],
				'field2': [0, 1]
			}
		},
		{
			'rules': {
				'field1': 'gte:field2'
			},
			'values': {
				'field1': {"a":0, "b":1},
				'field2': {"a":0, "b":1}
			}
		},
		{
			'rules': {
				'field1': 'gte:field2'
			},
			'values': {
				'field1': {"a":0, "b":1, "c":2},
				'field2': {"a":0, "b":1}
			}
		},
		{
			'rules': {
				'field1': 'gte:field2'
			},
			'values': {
				'field1': mockup_files['2kb'],
				'field2': mockup_files['2kb']
			}
		},
		{
			'rules': {
				'field1': 'gte:field2'
			},
			'values': {
				'field1': mockup_files['3kb'],
				'field2': mockup_files['2kb']
			}
		}
	]

@pytest.fixture
def fail_data_gte():
	return [
		{
			'rules': {
				'field1': 'gte:field2'
			},
			'values': {
				'field1': "abcd",
				'field2': 1234
			}
		},
		{
			'rules': {
				'field1': 'gte:field2'
			},
			'values': {
				'field1': 'a',
				'field2': 'de',
			}
		},
		{
			'rules': {
				'field1': 'gte:field2'
			},
			'values': {
				'field1': 1,
				'field2': 2,
			}
		},
		{
			'rules': {
				'field1': 'gte:field2'
			},
			'values': {
				'field1': [0],
				'field2': [0, 1],
			}
		},
		{
			'rules': {
				'field1': 'gte:field2'
			},
			'values': {
				'field1': {"a":0},
				'field2': {"a":0, "b":1},
			}
		},
		{
			'rules': {
				'field1': 'gte:field2'
			},
			'values': {
				'field1': mockup_files['1kb'],
				'field2': mockup_files['2kb'],
			}
		}
	]

def test_handler_gte(pass_data_gte, fail_data_gte):
	generic_test(pass_data_gte, fail_data_gte)

# ==================================================================================================== #

@pytest.fixture
def pass_data_image():
	return [
		{
			'rules': {
				'field': 'image'
			},
			'values': {
				'field': mockup_files['image']
			}
		},
		{
			'rules': {
				'field': 'image'
			},
			'values': {
				'field': mockup_files['1000x1000']
			}
		},
	]

@pytest.fixture
def fail_data_image():
	return [
		{
			'rules': {
				'field': 'image'
			},
			'values': {
				'field': 1234
			}
		},
		{
			'rules': {
				'field': 'image'
			},
			'values': {
				'field': mockup_files['2kb']
			}
		},
		{
			'rules': {
				'field': 'image'
			},
			'values': {
				'field': mockup_files['0kb']
			}
		},
		{
			'rules': {
				'field': 'image'
			},
			'values': {
				'field': None
			}
		},
		{
			'rules': {
				'field': 'image'
			},
			'values': {
			}
		}
	]

def test_handler_image(pass_data_image, fail_data_image):
	generic_test(pass_data_image, fail_data_image)

# ==================================================================================================== #

@pytest.fixture
def pass_data_in():
	return {
		'rules': {
			'field': 'in:x,y,z'
		},
		'values': {
			'field': 'z'
		}
	}

@pytest.fixture
def fail_data_in():
	return {
		'rules': {
			'field': 'in:x,y,z'
		},
		'values': {
			'field': 1
		}
	}

def test_handler_in(pass_data_in, fail_data_in):
	generic_test(pass_data_in, fail_data_in)

# ==================================================================================================== #

@pytest.fixture
def pass_data_in_array():
	return {
		'rules': {
			'field1': 'in_array:field2'
		},
		'values': {
			'field1': 'z',
			'field2': ['x','y','z']
		}
	}

@pytest.fixture
def fail_data_in_array():
	return [
		{
			'rules': {
				'field1': 'in_array:field2'
			},
			'values': {
				'field1': 1,
				'field2': ['x','y','z']
			}
		},
		{
			'rules': {
				'field1': 'in_array:field2'
			},
			'values': {
				'field1': 'z',
				'field2': 999
			}
		},
		{
			'rules': {
				'field1': 'in_array:field2'
			},
			'values': {
				'field1': 1,
			}
		}
	]

def test_handler_in_array(pass_data_in_array, fail_data_in_array):
	generic_test(pass_data_in_array, fail_data_in_array)

# ==================================================================================================== #

@pytest.fixture
def pass_data_integer():
	return [
		{
			'rules': {
				'field': 'integer'
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
		}
	]
@pytest.fixture
def fail_data_integer():
	return {
		'rules': {
			'field': 'integer'
		},
		'values': {
			'field': 'not an integer'
		}
	}

def test_handler_integer(pass_data_integer, fail_data_integer):
	generic_test(pass_data_integer, fail_data_integer)

# ==================================================================================================== #

@pytest.fixture
def pass_data_ip():
	return [
		{
			'rules': {
				'field': 'ip'
			},
			'values': {
				'field': '192.168.1.1'
			}
		},
		{
			'rules': {
				'field': 'ip'
			},
			'values': {
				'field': 'fd42:3c8b:01d5:9476:0000:0000:0000:0000'
			}
		}
	]

@pytest.fixture
def fail_data_ip():
	return {
		'rules': {
			'field': 'ip'
		},
		'values': {
			'field': 'not an ip address'
		}
	}

def test_handler_ip(pass_data_ip, fail_data_ip):
	generic_test(pass_data_ip, fail_data_ip)

# ==================================================================================================== #

@pytest.fixture
def pass_data_ipv4():
	return {
		'rules': {
			'field': 'ipv4'
		},
		'values': {
			'field': '192.168.1.1'
		}
	}

@pytest.fixture
def fail_data_ipv4():
	return [
		{
			'rules': {
				'field': 'ipv4'
			},
			'values': {
				'field': 'fd42:3c8b:01d5:9476:0000:0000:0000:0000'
			}
		},
		{
			'rules': {
				'field': 'ipv4'
			},
			'values': {
				'field': 'not an ip address'
			}
		}
	]

def test_handler_ipv4(pass_data_ipv4, fail_data_ipv4):
	generic_test(pass_data_ipv4, fail_data_ipv4)

# ==================================================================================================== #

@pytest.fixture
def pass_data_ipv6():
	return {
		'rules': {
			'field': 'ipv6'
		},
		'values': {
			'field': 'fd42:3c8b:01d5:9476:0000:0000:0000:0000'
		}
	}

@pytest.fixture
def fail_data_ipv6():
	return [
		{
			'rules': {
				'field': 'ipv6'
			},
			'values': {
				'field': '192.168.1.1'
			}
		},
		{
			'rules': {
				'field': 'ipv6'
			},
			'values': {
				'field': 'not an ip address'
			}
		}
	]

def test_handler_ipv6(pass_data_ipv6, fail_data_ipv6):
	generic_test(pass_data_ipv6, fail_data_ipv6)

# ==================================================================================================== #

@pytest.fixture
def pass_data_json():
	return [
		{
			'rules': {
				'field': 'json'
			},
			'values': {
				'field': {
					"a": 1,
					"b": 2
				}
			}
		},
		{
			'rules': {
				'field': 'json'
			},
			'values': {
				'field': '{"a": 1,"b": 2}'
			}
		}
	]

@pytest.fixture
def fail_data_json():
	return [
		{
			'rules': {
				'field': 'json'
			},
			'values': {
				'field': 1
			}
		},
		{
			'rules': {
				'field': 'json'
			},
			'values': {
				'field': '{"a": 1,"b": 2'
			}
		}
	]

def test_handler_json(pass_data_json, fail_data_json):
	generic_test(pass_data_json, fail_data_json)

# ==================================================================================================== #

@pytest.fixture
def pass_data_lt():
	return [
		{
			'rules': {
				'field1': 'lt:field2'
			},
			'values': {
				'field1': 'a',
				'field2': 'de'
			}
		},
		{
			'rules': {
				'field1': 'lt:field2'
			},
			'values': {
				'field1': 1,
				'field2': 2
			}
		},
		{
			'rules': {
				'field1': 'lt:field2'
			},
			'values': {
				'field1': [0],
				'field2': [0, 1]
			}
		},
		{
			'rules': {
				'field1': 'lt:field2'
			},
			'values': {
				'field1': {"a":0},
				'field2': {"a":0, "b":1}
			}
		},
		{
			'rules': {
				'field1': 'lt:field2'
			},
			'values': {
				'field1': mockup_files['1kb'],
				'field2': mockup_files['2kb']
			}
		},
	]

@pytest.fixture
def fail_data_lt():
	return [
		{
			'rules': {
				'field1': 'lt:field2'
			},
			'values': {
				'field1': "abcd",
				'field2': 1234
			}
		},
		{
			'rules': {
				'field1': 'lt:field2'
			},
			'values': {
				'field1': 'abc',
				'field2': 'de',
			}
		},
		{
			'rules': {
				'field1': 'lt:field2'
			},
			'values': {
				'field1': 'ab',
				'field2': 'de'
			}
		},
		{
			'rules': {
				'field1': 'lt:field2'
			},
			'values': {
				'field1': 3,
				'field2': 2,
			}
		},
		{
			'rules': {
				'field1': 'lt:field2'
			},
			'values': {
				'field1': 2,
				'field2': 2
			}
		},
		{
			'rules': {
				'field1': 'lt:field2'
			},
			'values': {
				'field1': [0, 1, 2],
				'field2': [0, 1],
			}
		},
		{
			'rules': {
				'field1': 'lt:field2'
			},
			'values': {
				'field1': [0, 1],
				'field2': [0, 1]
			}
		},
		{
			'rules': {
				'field1': 'lt:field2'
			},
			'values': {
				'field1': {"a":0, "b":1, "c":2},
				'field2': {"a":0, "b":1},
			}
		},
		{
			'rules': {
				'field1': 'lt:field2'
			},
			'values': {
				'field1': {"a":0, "b":1},
				'field2': {"a":0, "b":1}
			}
		},
		{
			'rules': {
				'field1': 'lt:field2'
			},
			'values': {
				'field1': mockup_files['3kb'],
				'field2': mockup_files['2kb'],
			}
		},
		{
			'rules': {
				'field1': 'lt:field2'
			},
			'values': {
				'field1': mockup_files['2kb'],
				'field2': mockup_files['2kb']
			}
		},
	]

def test_handler_lt(pass_data_lt, fail_data_lt):
	generic_test(pass_data_lt, fail_data_lt)

# ==================================================================================================== #

@pytest.fixture
def pass_data_lte():
	return [
		{
			'rules': {
				'field1': 'lte:field2'
			},
			'values': {
				'field1': 'a',
				'field2': 'de'
			}
		},
		{
			'rules': {
				'field1': 'lte:field2'
			},
			'values': {
				'field1': 'ab',
				'field2': 'de'
			}
		},
		{
			'rules': {
				'field1': 'lte:field2'
			},
			'values': {
				'field1': 1,
				'field2': 2
			}
		},
		{
			'rules': {
				'field1': 'lte:field2'
			},
			'values': {
				'field1': 2,
				'field2': 2
			}
		},
		{
			'rules': {
				'field1': 'lte:field2'
			},
			'values': {
				'field1': [0],
				'field2': [0, 1]
			}
		},
		{
			'rules': {
				'field1': 'lte:field2'
			},
			'values': {
				'field1': [0, 1],
				'field2': [0, 1]
			}
		},
		{
			'rules': {
				'field1': 'lte:field2'
			},
			'values': {
				'field1': {"a":0},
				'field2': {"a":0, "b":1}
			}
		},
		{
			'rules': {
				'field1': 'lte:field2'
			},
			'values': {
				'field1': {"a":0, "b":1},
				'field2': {"a":0, "b":1}
			}
		},
		{
			'rules': {
				'field1': 'lte:field2'
			},
			'values': {
				'field1': mockup_files['1kb'],
				'field2': mockup_files['2kb']
			}
		},
		{
			'rules': {
				'field1': 'lte:field2'
			},
			'values': {
				'field1': mockup_files['2kb'],
				'field2': mockup_files['2kb']
			}
		}
	]

@pytest.fixture
def fail_data_lte():
	return [
		{
			'rules': {
				'field1': 'lte:field2'
			},
			'values': {
				'field1': "abcd",
				'field2': 1234
			}
		},
		{
			'rules': {
				'field1': 'lte:field2'
			},
			'values': {
				'field1': 'abc',
				'field2': 'de',
			}
		},
		{
			'rules': {
				'field1': 'lte:field2'
			},
			'values': {
				'field1': 3,
				'field2': 2,
			}
		},
		{
			'rules': {
				'field1': 'lte:field2'
			},
			'values': {
				'field1': [0, 1, 2],
				'field2': [0, 1],
			}
		},
		{
			'rules': {
				'field1': 'lte:field2'
			},
			'values': {
				'field1': {"a":0, "b":1, "c":2},
				'field2': {"a":0, "b":1},
			}
		},
		{
			'rules': {
				'field1': 'lte:field2'
			},
			'values': {
				'field1': mockup_files['3kb'],
				'field2': mockup_files['2kb'],
			}
		}
	]

def test_handler_lte(pass_data_lte, fail_data_lte):
	generic_test(pass_data_lte, fail_data_lte)

# ==================================================================================================== #

@pytest.fixture
def pass_data_max():
	return [
		{
			'rules': {
				'field': 'max:2'
			},
			'values': {
				'field': 'ab'
			}
		},
		{
			'rules': {
				'field': 'max:2'
			},
			'values': {
				'field': ''
			}
		},
		{
			'rules': {
				'field': 'max:2'
			},
			'values': {
				'field': 2
			}
		},
		{
			'rules': {
				'field': 'max:2'
			},
			'values': {
				'field': 0
			}
		},
		{
			'rules': {
				'field': 'max:2'
			},
			'values': {
				'field': [0, 1]
			}
		},
		{
			'rules': {
				'field': 'max:2'
			},
			'values': {
				'field': []
			}
		},
		{
			'rules': {
				'field': 'max:2'
			},
			'values': {
				'field': {"a":0, "b":1}
			}
		},
		{
			'rules': {
				'field': 'max:2'
			},
			'values': {
				'field': {}
			}
		},
		{
			'rules': {
				'field': 'max:2'
			},
			'values': {
				'field': mockup_files['2kb']
			}
		},
		{
			'rules': {
				'field': 'max:2'
			},
			'values': {
				'field': mockup_files['0kb']
			}
		}
	]

@pytest.fixture
def fail_data_max():
	return [
		{
			'rules': {
				'field': 'max:0'
			},
			'values': {
				'field': 'ab'
			}
		},
		{
			'rules': {
				'field': 'max:0'
			},
			'values': {
				'field': 2
			}
		},
		{
			'rules': {
				'field': 'max:0'
			},
			'values': {
				'field': [0, 1]
			}
		},
		{
			'rules': {
				'field': 'max:0'
			},
			'values': {
				'field': {"a":0, "b":1}
			}
		},
		{
			'rules': {
				'field': 'max:0'
			},
			'values': {
				'field': mockup_files['2kb']
			}
		}
	]

def test_handler_max(pass_data_max, fail_data_max):
	generic_test(pass_data_max, fail_data_max)

# ==================================================================================================== #

@pytest.fixture
def pass_data_mimetypes():
	return [
		{
			'rules': {
				'field': 'mimetypes:text/plain'
			},
			'values': {
				'field': mockup_files['2kb']
			}
		},
		{
			'rules': {
				'field': 'mimetypes:image/jpeg'
			},
			'values': {
				'field': mockup_files['1000x1000']
			}
		},
		{
			'rules': {
				'field': 'mimetypes:text/plain,application/json'
			},
			'values': {
				'field': mockup_files['json']
			}
		},
	]

@pytest.fixture
def fail_data_mimetypes():
	return [
		{
			'rules': {
				'field': 'mimetypes:text/plain'
			},
			'values': {
				'field': mockup_files['image']
			}
		},
		{
			'rules': {
				'field': 'mimetypes:image/jpeg'
			},
			'values': {
				'field': mockup_files['image']
			}
		},
		{
			'rules': {
				'field': 'mimetypes:text/plain,application/json'
			},
			'values': {
				'field': mockup_files['image']
			}
		},
	]

def test_handler_mimetypes(pass_data_mimetypes, fail_data_mimetypes):
	generic_test(pass_data_mimetypes, fail_data_mimetypes)

# ==================================================================================================== #

@pytest.fixture
def pass_data_min():
	return [
		{
			'rules': {
				'field': 'min:2'
			},
			'values': {
				'field': 'ab'
			}
		},
		{
			'rules': {
				'field': 'min:2'
			},
			'values': {
				'field': 'abc'
			}
		},
		{
			'rules': {
				'field': 'min:2'
			},
			'values': {
				'field': 2
			}
		},
		{
			'rules': {
				'field': 'min:2'
			},
			'values': {
				'field': 3
			}
		},
		{
			'rules': {
				'field': 'min:2'
			},
			'values': {
				'field': [0, 1]
			}
		},
		{
			'rules': {
				'field': 'min:2'
			},
			'values': {
				'field': [0, 1, 2]
			}
		},
		{
			'rules': {
				'field': 'min:2'
			},
			'values': {
				'field': {"a":0, "b":1}
			}
		},
		{
			'rules': {
				'field': 'min:2'
			},
			'values': {
				'field': {"a":0, "b":1, "c":2}
			}
		},
		{
			'rules': {
				'field': 'min:2'
			},
			'values': {
				'field': mockup_files['2kb']
			}
		},
		{
			'rules': {
				'field': 'min:2'
			},
			'values': {
				'field': mockup_files['3kb']
			}
		}
	]

@pytest.fixture
def fail_data_min():
	return [
		{
			'rules': {
				'field': 'min:9999'
			},
			'values': {
				'field': 'ab'
			}
		},
		{
			'rules': {
				'field': 'min:9999'
			},
			'values': {
				'field': 2
			}
		},
		{
			'rules': {
				'field': 'min:9999'
			},
			'values': {
				'field': [0, 1]
			}
		},
		{
			'rules': {
				'field': 'min:9999'
			},
			'values': {
				'field': {"a":0, "b":1}
			}
		},
		{
			'rules': {
				'field': 'min:9999'
			},
			'values': {
				'field': mockup_files['2kb']
			}
		}
	]

def test_handler_min(pass_data_min, fail_data_min):
	generic_test(pass_data_min, fail_data_min)

# ==================================================================================================== #

@pytest.fixture
def pass_data_not_in():
	return {
		'rules': {
			'field': 'not_in:x,y,z'
		},
		'values': {
			'field': 1
		}
	}

@pytest.fixture
def fail_data_not_in():
	return {
		'rules': {
			'field': 'not_in:x,y,z'
		},
		'values': {
			'field': 'z'
		}
	}

def test_handler_not_in(pass_data_not_in, fail_data_not_in):
	generic_test(pass_data_not_in, fail_data_not_in)

# ==================================================================================================== #

@pytest.fixture
def pass_data_not_in_array():
	return {
		'rules': {
			'field1': 'not_in_array:field2'
		},
		'values': {
			'field1': 1,
			'field2': ['x','y','z']
		}
	}

@pytest.fixture
def fail_data_not_in_array():
	return [
		{
			'rules': {
				'field1': 'not_in_array:field2'
			},
			'values': {
				'field1': 'z',
				'field2': ['x','y','z']
			}
		},
		{
			'rules': {
				'field1': 'not_in_array:field2'
			},
			'values': {
				'field1': 'z',
				'field2': 999
			}
		},
		{
			'rules': {
				'field1': 'not_in_array:field2'
			},
			'values': {
				'field1': 1,
			}
		}
	]

def test_handler_not_in_array(pass_data_not_in_array, fail_data_not_in_array):
	generic_test(pass_data_not_in_array, fail_data_not_in_array)

# ==================================================================================================== #

@pytest.fixture
def pass_data_not_regex():
	return {
		'rules': {
			'field': r'not_regex:\d+'
		},
		'values': {
			'field': 'abcd'
		}
	}

@pytest.fixture
def fail_data_not_regex():
	return [
		{
			'rules': {
				'field': r'not_regex:\d+'
			},
			'values': {
				'field': '1234'
			}
		},
		{
			'rules': {
				'field': r'not_regex:\d+'
			},
			'values': {
				'field': 9999
			}
		}
	]

def test_handler_not_regex(pass_data_not_regex, fail_data_not_regex):
	generic_test(pass_data_not_regex, fail_data_not_regex)

# ==================================================================================================== #

@pytest.fixture
def pass_data_numeric():
	return [
		{
			'rules': {
				'field': 'numeric'
			},
			'values': {
				'field': '1234'
			}
		},
		{
			'rules': {
				'field': 'numeric'
			},
			'values': {
				'field': '12.34'
			}
		},
		{
			'rules': {
				'field': 'numeric'
			},
			'values': {
				'field': 1234
			}
		}
	]

@pytest.fixture
def fail_data_numeric():
	return {
		'rules': {
			'field': 'numeric'
		},
		'values': {
			'field': 'abcd'
		}
	}

def test_handler_numeric(pass_data_numeric, fail_data_numeric):
	generic_test(pass_data_numeric, fail_data_numeric)

# ==================================================================================================== #

@pytest.fixture
def pass_data_present():
	return [
		{
			'rules': {
				'field': 'present'
			},
			'values': {
				'field': None
			}
		},
		{
			'rules': {
				'field': 'present'
			},
			'values': {
				'field': 'abcd'
			}
		}
	]

@pytest.fixture
def fail_data_present():
	return {
		'rules': {
			'field': 'present'
		},
		'values': {
		}
	}

def test_handler_present(pass_data_present, fail_data_present):
	generic_test(pass_data_present, fail_data_present)

# ==================================================================================================== #

@pytest.fixture
def pass_data_regex():
	return {
		'rules': {
			'field': r'regex:\d+'
		},
		'values': {
			'field': '1234'
		}
	}

@pytest.fixture
def fail_data_regex():
	return [
		{
			'rules': {
				'field': r'regex:\d+'
			},
			'values': {
				'field': 'abcd'
			}
		},
		{
			'rules': {
				'field': r'regex:\d+'
			},
			'values': {
				'field': 9999
			}
		}
	]

def test_handler_regex(pass_data_regex, fail_data_regex):
	generic_test(pass_data_regex, fail_data_regex)

# ==================================================================================================== #

@pytest.fixture
def pass_data_required():
	return {
		'rules': {
			'field': 'required'
		},
		'values': {
			'field': 'abcd'
		}
	}

@pytest.fixture
def fail_data_required():
	return [
		{
			'rules': {
				'field': 'required'
			},
			'values': {
			}
		},
		{
			'rules': {
				'field': 'required'
			},
			'values': {
				'field': ""
			}
		},
		{
			'rules': {
				'field': 'required'
			},
			'values': {
				'field': []
			}
		},
		{
			'rules': {
				'field': 'required'
			},
			'values': {
				'field': {}
			}
		},
		{
			'rules': {
				'field': 'required'
			},
			'values': {
				'field': None
			}
		},
		{
			'rules': {
				'field': 'required'
			},
			'values': {
				'field': mockup_files['0kb']
			}
		}
	]

def test_handler_required(pass_data_required, fail_data_required):
	generic_test(pass_data_required, fail_data_required)

# ==================================================================================================== #

@pytest.fixture
def pass_data_required_if():
	return [
		{
			'rules': {
				'field1': 'required_if:field2,ABCD,abcd'
			},
			'values': {
				'field1': '1234',
				'field2': 'abcd'
			}
		},
		{
			'rules': {
				'field1': 'required_if:field2,ABCD,abcd'
			},
			'values': {
				'field2': 'random string'
			}
		},
		{
			'rules': {
				'field1': 'required_if:field2,ABCD,abcd'
			},
			'values': {
				'field2': 0
			}
		},
		{
			'rules': {
				'field1': 'required_if:field2,ABCD,abcd'
			},
			'values': {
			}
		}
	]

@pytest.fixture
def fail_data_required_if():
	return {
		'rules': {
			'field1': 'required_if:field2,ABCD,abcd'
		},
		'values': {
			'field2': 'ABCD'
		}
	}

def test_handler_required_if(pass_data_required_if, fail_data_required_if):
	generic_test(pass_data_required_if, fail_data_required_if)

# ==================================================================================================== #

@pytest.fixture
def pass_data_required_unless():
	return [
		{
			'rules': {
				'field1': 'required_unless:field2,WXYZ,wxyz'
			},
			'values': {
				'field1': '1234',
				'field2': 'random text',
			}
		},
		{
			'rules': {
				'field1': 'required_unless:field2,WXYZ,wxyz'
			},
			'values': {
				'field1': '1234',
				'field2': 0,
			}
		},
		{
			'rules': {
				'field1': 'required_unless:field2,WXYZ,wxyz'
			},
			'values': {
				'field2': 'wxyz',
			}
		},
		{
			'rules': {
				'field1': 'required_unless:field2,WXYZ,wxyz'
			},
			'values': {
				'field1': '1234',
			}
		},
	]

@pytest.fixture
def fail_data_required_unless():
	return {
		'rules': {
			'field1': 'required_unless:field2,WXYZ,wxyz'
		},
		'values': {
			'field2': 'some text'
		}
	}

def test_handler_required_unless(pass_data_required_unless, fail_data_required_unless):
	generic_test(pass_data_required_unless, fail_data_required_unless)

# ==================================================================================================== #

@pytest.fixture
def pass_data_required_with():
	return [
		{
			'rules': {
				'field1': 'required_with:field2,field3'
			},
			'values': {
				'field1': 1,
				'field2': 2
			}
		},
		{
			'rules': {
				'field1': 'required_with:field2,field3'
			},
			'values': {
				'field1': 1,
				'field2': 2,
				'field3': 3,
			}
		},
		{
			'rules': {
				'field1': 'required_with:field2,field3'
			},
			'values': {
			}
		}
	]

@pytest.fixture
def fail_data_required_with():
	return {
		'rules': {
			'field1': 'required_with:field2,field3'
		},
		'values': {
			'field2': 2
		}
	}

def test_handler_required_with(pass_data_required_with, fail_data_required_with):
	generic_test(pass_data_required_with, fail_data_required_with)

# ==================================================================================================== #

@pytest.fixture
def pass_data_required_with_all():
	return [
		{
			'rules': {
				'field1': 'required_with_all:field2,field3'
			},
			'values': {
				'field1': 1,
				'field2': 2,
				'field3': 3,
			}
		},
		{
			'rules': {
				'field1': 'required_with_all:field2,field3'
			},
			'values': {
				'field2': 2,
			}
		},
		
	]

@pytest.fixture
def fail_data_required_with_all():
	return {
			'rules': {
				'field1': 'required_with_all:field2,field3'
			},
			'values': {
				'field2': 2,
				'field3': 3,
			}
		}

def test_handler_required_with_all(pass_data_required_with_all, fail_data_required_with_all):
	generic_test(pass_data_required_with_all, fail_data_required_with_all)

# ==================================================================================================== #

@pytest.fixture
def pass_data_required_without():
	return [
		{
			'rules': {
				'field1': 'required_without:field2,field3'
			},
			'values': {
				'field1': 1,
				'field2': 2,
			}
		},
		{
			'rules': {
				'field1': 'required_without:field2,field3'
			},
			'values': {
				'field2': 2,
				'field3': 3,
			}
		},
		{
			'rules': {
				'field1': 'required_without:field2,field3'
			},
			'values': {
				'field1': 1,
			}
		}
	]

@pytest.fixture
def fail_data_required_without():
	return [
		{
			'rules': {
				'field1': 'required_without:field2,field3'
			},
			'values': {
				'field2': 2,
			}
		},
		{
			'rules': {
				'field1': 'required_without:field2,field3'
			},
			'values': {
			}
		}
	]

def test_handler_required_without(pass_data_required_without, fail_data_required_without):
	generic_test(pass_data_required_without, fail_data_required_without)

# ==================================================================================================== #

@pytest.fixture
def pass_data_required_without_all():
	return [
		{
			'rules': {
				'field1': 'required_without_all:field2,field3'
			},
			'values': {
				'field1': 1
			}
		},
		{
			'rules': {
				'field1': 'required_without_all:field2,field3'
			},
			'values': {
				'field2': 2
			}
		},
		{
			'rules': {
				'field1': 'required_without_all:field2,field3'
			},
			'values': {
				'field2': 2,
				'field3': 3
			}
		},
	]

@pytest.fixture
def fail_data_required_without_all():
	return {
			'rules': {
				'field1': 'required_without_all:field2,field3'
			},
			'values': {
			}
		}

def test_handler_required_without_all(pass_data_required_without_all, fail_data_required_without_all):
	generic_test(pass_data_required_without_all, fail_data_required_without_all)

# ==================================================================================================== #

@pytest.fixture
def pass_data_same():
	return [
		{
			'rules': {
				'field1': 'same:field2'
			},
			'values': {
				'field1': [1,2,3],
				'field2': [1,2,3]
			}
		},
		{
			'rules': {
				'field1': 'same:field2'
			},
			'values': {
				'field1': "abcd",
				'field2': "abcd"
			}
		}
	]

@pytest.fixture
def fail_data_same():
	return [
		{
			'rules': {
				'field1': 'same:field2'
			},
			'values': {
				'field1': 1234,
				'field2': "abcd"
			}
		},
		{
			'rules': {
				'field1': 'same:field2'
			},
			'values': {
				'field1': 1234,
			}
		}
	]

def test_handler_same(pass_data_same, fail_data_same):
	generic_test(pass_data_same, fail_data_same)

# ==================================================================================================== #

@pytest.fixture
def pass_data_size():
	return [
		{
			'rules': {
				'field': 'size:2'
			},
			'values': {
				'field': 'ab'
			}
		},
		{
			'rules': {
				'field': 'size:2'
			},
			'values': {
				'field': 2
			}
		},
		{
			'rules': {
				'field': 'size:2'
			},
			'values': {
				'field': [0, 1]
			}
		},
		{
			'rules': {
				'field': 'size:2'
			},
			'values': {
				'field': {"a":0, "b":1}
			}
		},
		{
			'rules': {
				'field': 'size:2'
			},
			'values': {
				'field': mockup_files['2kb']
			}
		}
	]

@pytest.fixture
def fail_data_size():
	return [
		{
			'rules': {
				'field': 'size:9999'
			},
			'values': {
				'field': 'ab'
			}
		},
		{
			'rules': {
				'field': 'size:9999'
			},
			'values': {
				'field': 2
			}
		},
		{
			'rules': {
				'field': 'size:9999'
			},
			'values': {
				'field': [0, 1]
			}
		},
		{
			'rules': {
				'field': 'size:9999'
			},
			'values': {
				'field': {"a":0, "b":1}
			}
		},
		{
			'rules': {
				'field': 'size:9999'
			},
			'values': {
				'field': mockup_files['2kb']
			}
		}
	]

def test_handler_size(pass_data_size, fail_data_size):
	generic_test(pass_data_size, fail_data_size)

# ==================================================================================================== #

@pytest.fixture
def pass_data_starts_with():
	return [
		{
			'rules': {
				'field': 'starts_with:a'
			},
			'values': {
				'field': 'abcd'
			}
		},
		{
			'rules': {
				'field': 'starts_with:1'
			},
			'values': {
				'field': 1234
			}
		},
		{
			'rules': {
				'field': 'starts_with:a'
			},
			'values': {
				'field': ['a', 'b', 'c']
			}
		},
		{
			'rules': {
				'field': 'starts_with:abc'
			},
			'values': {
				'field': mockup_files['alphabet']
			}
		},
	]

@pytest.fixture
def fail_data_starts_with():
	return [
		{
			'rules': {
				'field': 'starts_with:a'
			},
			'values': {
				'field': 'bcd'
			}
		},
		{
			'rules': {
				'field': 'starts_with:1'
			},
			'values': {
				'field': 999
			}
		},
		{
			'rules': {
				'field': 'starts_with:a'
			},
			'values': {
				'field': ['b', 'c']
			}
		},
		{
			'rules': {
				'field': 'starts_with:z'
			},
			'values': {
				'field': mockup_files['alphabet']
			}
		},
	]

def test_handler_starts_with(pass_data_starts_with, fail_data_starts_with):
	generic_test(pass_data_starts_with, fail_data_starts_with)

# ==================================================================================================== #

@pytest.fixture
def pass_data_string():
	return {
		'rules': {
			'field': 'string'
		},
		'values': {
			'field': 'abcd'
		}
	}

@pytest.fixture
def fail_data_string():
	return {
		'rules': {
			'field': 'string'
		},
		'values': {
			'field': 1234
		}
	}

def test_handler_string(pass_data_string, fail_data_string):
	generic_test(pass_data_string, fail_data_string)

# ==================================================================================================== #

@pytest.fixture
def pass_data_timezone():
	return {
		'rules': {
			'field': 'timezone'
		},
		'values': {
			'field': 'Europe/Moscow'
		}
	}

@pytest.fixture
def fail_data_timezone():
	return {
		'rules': {
			'field': 'timezone'
		},
		'values': {
			'field': 'not a timezone'
		}
	}

def test_handler_timezone(pass_data_timezone, fail_data_timezone):
	generic_test(pass_data_timezone, fail_data_timezone)

# ==================================================================================================== #

@pytest.fixture
def pass_data_url():
	return {
		'rules': {
			'field': 'url'
		},
		'values': {
			'field': 'https://example.com'
		}
	}

@pytest.fixture
def fail_data_url():
	return [
		{
			'rules': {
				'field': 'url'
			},
			'values': {
				'field': 'example.com'
			}
		},
		{
			'rules': {
				'field': 'url'
			},
			'values': {
				'field': 'www.example.com'
			}
		},
		{
			'rules': {
				'field': 'url'
			},
			'values': {
				'field': 1234
			}
		}
	]

def test_handler_url(pass_data_url, fail_data_url):
	generic_test(pass_data_url, fail_data_url)

# ==================================================================================================== #

@pytest.fixture
def pass_data_uuid():
	return {
		'rules': {
			'field': 'uuid'
		},
		'values': {
			'field': 'c906e94e-dffe-11ea-87d0-0242ac130003'
		}
	}

@pytest.fixture
def fail_data_uuid():
	return {
		'rules': {
			'field': 'uuid'
		},
		'values': {
			'field': 'not and uuid'
		}
	}

def test_handler_uuid(pass_data_uuid, fail_data_uuid):
	generic_test(pass_data_uuid, fail_data_uuid)

# ==================================================================================================== #
