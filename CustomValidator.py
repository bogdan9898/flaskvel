from flaskvel import Validator, Rules

class CustomValidator(Validator):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.rules = {
            "username": ["required", "string"],
            "password": ["required", "string", "min:8", "max:32", "confirmed"], 
            "email": [Rules.REQUIRED, Rules.EMAIL] # we can also use predefined constants instead of strings
        }