from flaskvel import Rules, Validator, ParsedRule

class MyValidator(Validator):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.rules = {
			'username': [Rules.REQUIRED, Rules.STRING],
			
			'password': [Rules.REQUIRED, self.is_valid_passwd],
			# 'unreg_paramed_rule': [Rules.REQUIRED, ParsedRule(self.validate_unreg_paramed_rule, [1,2,3])],

			'email': [Rules.EMAIL, Rules.NULLABLE],
			
			'oras': [Rules.STRING, Rules.NULLABLE],
			'sector': [Rules.STRING, "required_if:oras,bucharest,bucuresti"],
			'judet': [Rules.STRING, "required_unless:oras,bucharest,bucuresti"],
			
			'date': [Rules.DATE, 'date_format:%d-%m-%Y'],
			'after_date': ['after:2020-07-10'],
			'after_eq_date': ['after_or_equal:2020-07-10'],
			'before_date': ['before:2020-07-20'],
			'before_eq_date': ['before_or_equal:2020-07-10'],
			'date_eq': ['date_equals:2020-07-16'],
			'timezone': ['timezone'],

			'array': [Rules.NULLABLE, Rules.ARRAY],
			
			'file_test': [Rules.REQUIRED, Rules.FILE],
			'mimetypes': ['mimetypes:image/png'],
			'image': [Rules.IMAGE],
			
			'json_test': Rules.JSON,
			'json_test.nested_param1': Rules.STRING,
			
			'present': Rules.PRESENT,
			'filled':Rules.FILLED,
			
			'same1': [ Rules.NULLABLE, Rules.STRING] ,
			'same2': [Rules.NULLABLE, Rules.STRING],
			'same3': [Rules.NULLABLE, Rules.STRING],
			'same4': [Rules.NULLABLE, Rules.STRING, "same:same1,same2,same3"],
			
			'integer': Rules.INTEGER,
			
			'key1': [Rules.STRING, "required_with:key2,key3,key4"],
			'key2': [Rules.STRING, Rules.NULLABLE],
			'key3': [Rules.STRING, Rules.NULLABLE],
			'key4': [Rules.STRING, Rules.NULLABLE],
			
			'nitrogen': [Rules.STRING, Rules.NULLABLE],
			'oxygen': [Rules.STRING, Rules.NULLABLE],
			'other_gases': [Rules.STRING, Rules.NULLABLE],
			'air': [Rules.STRING, "required_with_all:nitrogen,oxygen,other_gases"],

			'total': [Rules.INTEGER, "required_without:part_a,part_b,part_c"],
			'part_a': [Rules.STRING, Rules.NULLABLE],
			'part_b': [Rules.STRING, Rules.NULLABLE],
			'part_c': [Rules.STRING, Rules.NULLABLE],

			'red_light': [Rules.STRING, Rules.NULLABLE],
			'green_light': [Rules.STRING, Rules.NULLABLE],
			'blue_light': [Rules.STRING, Rules.NULLABLE],
			'darkness': [Rules.STRING, "required_without_all:red_light,green_light,blue_light"],

			'digits': [Rules.STRING, "digits:3"],
			'digits_between': [Rules.STRING, "digits_between:2,5"],

			'distinct': [Rules.DISTINCT],

			'in': ['in:9,8,7,6'],
			'in_array': ['in_array:array'],
			'not_in': ['not_in:9,8,7,6'],
			'not_in_array': ['not_in_array:array'],

			'regex': 'regex:^[a-z]+$',
			'not_regex': 'not_regex:^[a-z]+$',

			'starts_with_string': [Rules.STRING, 'starts_with:TeSt,tEsT'],
			'starts_with_numeric': [Rules.NUMERIC, 'starts_with:20,2020'],
			'starts_with_array': [Rules.ARRAY, 'starts_with:elementul0,elementul1'],
			'starts_with_file': [Rules.FILE, 'starts_with:test1234,TEST'],

			'ends_with_string': [Rules.STRING, 'ends_with:TeSt,tEsT'],
			'ends_with_numeric': [Rules.NUMERIC, 'ends_with:20,2020'],
			'ends_with_array': [Rules.ARRAY, 'ends_with:elementul0,elementul1'],
			'ends_with_file': [Rules.FILE, 'ends_with:test1234,line 7,not_this_ending'],

			'url': [Rules.URL],
			'active_url': [Rules.ACTIVE_URL],

			'uuid': [Rules.UUID],

			'ip': [Rules.IP],
			'ipv4': [Rules.IPV4],
			'ipv6': [Rules.IPV6],
		}

		self.messages = {
			"password.required": "I cant seem to find this field: {field_name}",
		}

	def is_valid_passwd(self, **kwargs):
		return True

	def validate_unreg_paramed_rule(self, params, **kwargs):
		return params is not None and len(params) > 0