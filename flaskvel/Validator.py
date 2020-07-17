from functools import wraps
from flask import request

from .Constants.BodyFormat import BodyFormats
from .Parsers.ArrayParser import ArrayParser
from .Parsers.PipedStringParser import PipedStringParser
from .Processor import Processor
from .ParsedRule import ParsedRule
from .Exceptions.ValidationException import ValidationException

class Validator:
	def __init__(self, body_format, methods):
		self._body_format = body_format
		self._methods = methods
		self._parsed_rules = {}
		# override these 2 attributes in your own implemenation of validator #
		self.rules = {}
		self.messages = {}
		# ------------------------------------------------------------------ #
		# todo: register custom handlers
		self._registered_handlers = []
		self._processor = Processor(self)

	def get_parsed_rules(self):
		return self._parsed_rules

	def get_messages(self):
		return self.messages

	def get_registered_handlers(self):
		return self._registered_handlers

	def validate(self):
		if not hasattr(self, '_processor'):
			raise Exception("Base validator not initialized. Most probably you forgot to call super().__init__(*args, **kwargs) inside your validator class.")
		if not self.validate_method():
			return # validation ignored for other methods
		self.validate_body_format()
		self.parse_rules()
		result = self._processor.run()
		print("Validation result: {0}".format(result))
		print(self._processor.get_failed_validations())
		if not result:
			raise ValidationException(self._processor.get_errors())

	def validate_method(self):
		return self._methods == "*" or request.method in self._methods

	def validate_body_format(self):
		if self._body_format == BodyFormats.ANY:
			return True
		elif self._body_format == BodyFormats.JSON:
			if not request.is_json:
				raise ValidationException("Request body is not a valid json")
			return True
		elif self._body_format == BodyFormats.FORM:
			if request.is_json:
				raise ValidationException("Request body is not a valid form")
			return True
		else:
			raise Exception("Invalid body format")

	def parse_rules(self):
		for field_name, field_rules in self.rules.items():
			if isinstance(field_rules, list):
				self._parsed_rules[field_name] = ArrayParser.parse(field_rules)
			elif isinstance(field_rules, str):
				self._parsed_rules[field_name] = PipedStringParser.parse(field_rules)
			elif callable(field_rules):
				self._parsed_rules[field_name] = [ParsedRule(field_rules)]
			else:
				raise Exception("Invalid rules; Expected: list/str/callable but got {2} for: <{0}: {1}>".format(field_name, field_rules, type(field_rules)))

# methods: {"GET", "POST", "PUT", "DELETE"....}
# methods=PipedString or Array or '*'
# methods: methods for which the Flaskvel should validate the body; default = "*"(all methods)
def validate(validator_class, body_format, methods="*"):
	def decorator(func):
		@wraps(func)
		def wrapper(*args, **kwargs):
			validator_class(body_format, methods).validate()
			return func(*args, **kwargs)
		return wrapper
	return decorator