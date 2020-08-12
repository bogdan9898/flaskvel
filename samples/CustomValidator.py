from flaskvel import Validator, Rules, ParsedRule

class CustomValidator(Validator):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.rules = {
		    "username": ["required", "string"],
		    "password": ["required", "string", "min:8", "max:32", "confirmed"], 
		    "email": [Rules.REQUIRED, Rules.EMAIL] # we can also use predefined constants instead of strings
		}

		self.messages = {
			"username.string": "Type of username is invalid",
			"password.min": "Password must be between 8 and 32",
			"password.max": "Password must be between 8 and 32",
			"password.confirmed": "Please confirm your password",
			"email.required": "Email address is required"
		}

		# self.rules = {
		# 	'username': "required|string",
		# 	'title': "nullable|string",
		# 	'description': "required_with:title|string|max:256",
		# 	'genre': "nullable|in:thriller,fantasy,romance"
		# }

		# self.rules = {
		# 	# "order_number": [Rules.NUMERIC, ParsedRule(self.is_divisible, [2])],
		# 	"order_number": [Rules.NUMERIC, 'divisible:2'],
		# }

		# self.messages = {
		# 	"order_number.divisible": "Order number must be divisible by {divisor}"
		# }

	def is_divisible(self, value, params, err_msg_params, **kwargs):
		err_msg_params['divisor'] = params[0]
		return int(value) % params[0] == 0