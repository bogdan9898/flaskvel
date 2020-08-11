from flaskvel import Validator, Rules, ParsedRule

class CustomValidator2(Validator):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.rules = {
			"test_field": [Rules.REQUIRED, 'my_custom_rule:param1,param2,param3'], # we pass a list containig our params for my_custom_rule
		}

		self.messages = {
			"test_field.my_custom_rule": "My name is {field_name}, these are my parameters: {0}, {1}, {2}, here is a link: {link} and a list of random words: {random_words_list}."
		}