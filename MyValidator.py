from flaskvel import Rules, Validator

class MyValidator(Validator):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.rules = {
			'username': [Rules.REQUIRED, Rules.STRING],
			
			'password': [Rules.REQUIRED, self.is_valid_passwd],
			
			'email': [Rules.EMAIL, Rules.NULLABLE],
			
			'oras': [Rules.STRING, Rules.NULLABLE],
			'sector': [Rules.STRING, "required_if:oras,bucharest,bucuresti"],
			'judet': [Rules.STRING, "required_unless:oras,bucharest,bucuresti"],
			
			'after_date': ['after:2020-07-10'],
			'after_eq_date': ['after_or_equal:2020-07-10'],
			'before_date': ['before:2020-07-20'],
			'before_eq_date': ['before_or_equal:2020-07-10'],
			
			'array': [Rules.NULLABLE, Rules.ARRAY],
			
			'file_test': [Rules.REQUIRED, Rules.FILE],
			
			'json_test': Rules.JSON,
			'json_test.nested_param1': Rules.STRING,
			
			'none_test': Rules.PRESENT,
			
			'same1': [Rules.NULLABLE, Rules.STRING],
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

		}

		self.messages = {
			"password.required": "I cant seem to find this field: {field_name}",
			
		}

	def is_valid_passwd(self, **kwargs):
		return False