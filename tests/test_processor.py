import pytest

from flaskvel.Processor import Processor
from flaskvel import Validator
from flaskvel.Parsers.UniversalParser import UniversalParser

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
	return validator._processor

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
	return {
		'rules': {
			'field': 'active_url'
		},
		'values': {
			'field': 'nothing here'
		}
	}

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

@pytest.mark.skip(reason="not implemented")
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

@pytest.mark.skip(reason="not implemented")
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

@pytest.mark.skip(reason="not implemented")
def test_handler_ends_with(pass_data_ends_with, fail_data_ends_with):
	generic_test(pass_data_ends_with, fail_data_ends_with)

# ==================================================================================================== #

@pytest.mark.skip(reason="not implemented")
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

@pytest.mark.skip(reason="not implemented")
def test_handler_gt(pass_data_gt, fail_data_gt):
	generic_test(pass_data_gt, fail_data_gt)

# ==================================================================================================== #

@pytest.mark.skip(reason="not implemented")
def test_handler_gte(pass_data_gte, fail_data_gte):
	generic_test(pass_data_gte, fail_data_gte)

# ==================================================================================================== #

@pytest.mark.skip(reason="not implemented")
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

@pytest.mark.skip(reason="not implemented")
def test_handler_lt(pass_data_lt, fail_data_lt):
	generic_test(pass_data_lt, fail_data_lt)

# ==================================================================================================== #

@pytest.mark.skip(reason="not implemented")
def test_handler_lte(pass_data_lte, fail_data_lte):
	generic_test(pass_data_lte, fail_data_lte)

# ==================================================================================================== #

@pytest.mark.skip(reason="not implemented")
def test_handler_max(pass_data_max, fail_data_max):
	generic_test(pass_data_max, fail_data_max)

# ==================================================================================================== #

@pytest.mark.skip(reason="not implemented")
def test_handler_mimetypes(pass_data_mimetypes, fail_data_mimetypes):
	generic_test(pass_data_mimetypes, fail_data_mimetypes)

# ==================================================================================================== #

@pytest.mark.skip(reason="not implemented")
def test_handler_min(pass_data_min, fail_data_min):
	generic_test(pass_data_min, fail_data_min)

# ==================================================================================================== #

@pytest.mark.skip(reason="not implemented")
def test_handler_not_in(pass_data_not_in, fail_data_not_in):
	generic_test(pass_data_not_in, fail_data_not_in)

# ==================================================================================================== #

@pytest.mark.skip(reason="not implemented")
def test_handler_not_in_array(pass_data_not_in_array, fail_data_not_in_array):
	generic_test(pass_data_not_in_array, fail_data_not_in_array)

# ==================================================================================================== #

@pytest.mark.skip(reason="not implemented")
def test_handler_not_regex(pass_data_not_regex, fail_data_not_regex):
	generic_test(pass_data_not_regex, fail_data_not_regex)

# ==================================================================================================== #

@pytest.mark.skip(reason="not implemented")
def test_handler_numeric(pass_data_numeric, fail_data_numeric):
	generic_test(pass_data_numeric, fail_data_numeric)

# ==================================================================================================== #

@pytest.mark.skip(reason="not implemented")
def test_handler_present(pass_data_present, fail_data_present):
	generic_test(pass_data_present, fail_data_present)

# ==================================================================================================== #

@pytest.mark.skip(reason="not implemented")
def test_handler_regex(pass_data_regex, fail_data_regex):
	generic_test(pass_data_regex, fail_data_regex)

# ==================================================================================================== #

@pytest.mark.skip(reason="not implemented")
def test_handler_required(pass_data_required, fail_data_required):
	generic_test(pass_data_required, fail_data_required)

# ==================================================================================================== #

@pytest.mark.skip(reason="not implemented")
def test_handler_required_if(pass_data_required_if, fail_data_required_if):
	generic_test(pass_data_required_if, fail_data_required_if)

# ==================================================================================================== #

@pytest.mark.skip(reason="not implemented")
def test_handler_required_unless(pass_data_required_unless, fail_data_required_unless):
	generic_test(pass_data_required_unless, fail_data_required_unless)

# ==================================================================================================== #

@pytest.mark.skip(reason="not implemented")
def test_handler_required_with(pass_data_required_with, fail_data_required_with):
	generic_test(pass_data_required_with, fail_data_required_with)

# ==================================================================================================== #

@pytest.mark.skip(reason="not implemented")
def test_handler_required_with_all(pass_data_required_with_all, fail_data_required_with_all):
	generic_test(pass_data_required_with_all, fail_data_required_with_all)

# ==================================================================================================== #

@pytest.mark.skip(reason="not implemented")
def test_handler_required_without(pass_data_required_without, fail_data_required_without):
	generic_test(pass_data_required_without, fail_data_required_without)

# ==================================================================================================== #

@pytest.mark.skip(reason="not implemented")
def test_handler_required_without_all(pass_data_required_without_all, fail_data_required_without_all):
	generic_test(pass_data_required_without_all, fail_data_required_without_all)

# ==================================================================================================== #

@pytest.mark.skip(reason="not implemented")
def test_handler_same(pass_data_same, fail_data_same):
	generic_test(pass_data_same, fail_data_same)

# ==================================================================================================== #

@pytest.mark.skip(reason="not implemented")
def test_handler_size(pass_data_size, fail_data_size):
	generic_test(pass_data_size, fail_data_size)

# ==================================================================================================== #

@pytest.mark.skip(reason="not implemented")
def test_handler_starts_with(pass_data_starts_with, fail_data_starts_with):
	generic_test(pass_data_starts_with, fail_data_starts_with)

# ==================================================================================================== #

@pytest.mark.skip(reason="not implemented")
def test_handler_string(pass_data_string, fail_data_string):
	generic_test(pass_data_string, fail_data_string)

# ==================================================================================================== #

@pytest.mark.skip(reason="not implemented")
def test_handler_timezone(pass_data_timezone, fail_data_timezone):
	generic_test(pass_data_timezone, fail_data_timezone)

# ==================================================================================================== #

@pytest.mark.skip(reason="not implemented")
def test_handler_url(pass_data_url, fail_data_url):
	generic_test(pass_data_url, fail_data_url)

# ==================================================================================================== #

@pytest.mark.skip(reason="not implemented")
def test_handler_uuid(pass_data_uuid, fail_data_uuid):
	generic_test(pass_data_uuid, fail_data_uuid)

# ==================================================================================================== #
