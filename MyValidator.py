from flaskvel import RulesPredicates, Validator

class MyValidator(Validator):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.rules = {
			'username_test': [RulesPredicates.REQUIRED, RulesPredicates.STRING],
			'password_test': [RulesPredicates.REQUIRED, self.confirm],
			'email_test': [RulesPredicates.REQUIRED, RulesPredicates.EMAIL, RulesPredicates.NULLABLE],
			'city_test': RulesPredicates.STRING,
			'sector_test': [RulesPredicates.STRING, "required_if:city,bucharest"],
			'after_date_test': ['after:2020-07-10'],
			'after_eq_date_test': ['after_or_equal:2020-07-10'],
			'before_date_test': ['before:2020-07-10'],
			'before_eq_date_test': ['before_or_equal:2020-07-10'],
		}

	def confirm(self, **kwargs):
		return False