from flaskvel import Validator

class CustomValidator(Validator):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.rules = {
			'password': 'string|confirmed|min:6'
		}
