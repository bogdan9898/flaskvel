from flaskvel import Validator, Rules, ParsedRule

class CustomValidator(Validator):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		# self.rules = {
		#     "username": ["required", "string"],
		#     "password": ["required", "string", "min:8", "max:32", "confirmed"], 
		#     "email": [Rules.REQUIRED, Rules.EMAIL] # we can also use predefined constants instead of strings
		# }
		

		self.rules = {
			# "order_number": [Rules.NUMERIC, ParsedRule(self.is_divisible, [2])],
			"order_number": [Rules.NUMERIC, 'divisible:2'],
		}

		self.messages = {
			"order_number.divisible": "Order number must be divisible by {divisor}"
		}

	def is_divisible(self, value, params, err_msg_params, **kwargs):
		err_msg_params['divisor'] = params[0]
		return int(value) % params[0] == 0