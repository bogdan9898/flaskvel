from flaskvel import Rules, Validator

class MyValidator(Validator):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.rules = {
			'username_test': [Rules.REQUIRED, Rules.STRING],
			'password_test': [Rules.REQUIRED, self.confirm],
			'email_test': [Rules.EMAIL, Rules.NULLABLE],
			'city_test': [Rules.STRING, Rules.NULLABLE],
			'sector_test': [Rules.STRING, "required_if:city,bucharest"],
			'after_date_test': ['after:2020-07-10'],
			'after_eq_date_test': ['after_or_equal:2020-07-10'],
			'before_date_test': ['before:2020-07-20'],
			'before_eq_date_test': ['before_or_equal:2020-07-10'],
			'array_test': [Rules.NULLABLE, Rules.ARRAY],
			'file_test': [Rules.REQUIRED, Rules.FILE],
			'json_test': Rules.JSON,
			'json_test.nested_param1': Rules.STRING,
			'none_test': Rules.PRESENT,
			'same1': Rules.STRING,
			'same2': Rules.STRING,
			'same3': Rules.STRING,
			'same4': [Rules.STRING, "same:same1,same2"],
			'integer_test': Rules.INTEGER
		}

	def confirm(self, **kwargs):
		return False