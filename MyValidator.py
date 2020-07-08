from flaskvel import RulesPredicates, Validator

class MyValidator(Validator):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.rules = {
			'username': RulesPredicates.REQUIRED,
			'password': self.confirm,
			'email': [RulesPredicates.REQUIRED, RulesPredicates.EMAIL, 'eq:3,6', 'nullable']
		}

	def confirm(self, **kwargs):
		return False