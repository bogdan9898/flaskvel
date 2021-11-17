from functools import wraps
import time
from flask import request

from .Flaskvel import Flaskvel
from .Constants.BodyFormat import BodyFormats
from .Parsers.UniversalParser import UniversalParser
from .Processor import Processor
from .ParsedRule import ParsedRule
from .Exceptions.ValidationException import ValidationException

class Validator():
	def __init__(self, request, expected_body_format=BodyFormats.ANY):
		self._request = request
		self._expected_body_format = expected_body_format
		self._parsed_rules = {}
		# override these 2 attributes in your own implemenation of validator #
		self.rules = {}
		self.messages = {}
		# ------------------------------------------------------------------ #
		self._processor = Processor(self)

	def get_parsed_rules(self):
		return self._parsed_rules

	def get_request(self):
		return self._request

	def get_messages(self):
		return self.messages

	def get_validation_errors(self):
		return self._processor.get_errors()

	def get_processor(self):
		return self._processor

	def validate(self):
		if not hasattr(self, '_processor'):
			raise Exception("Base validator not initialized. Most probably you forgot to call super().__init__(*args, **kwargs) inside your validator class.")
		self._validate_body_format()
		self._parsed_rules = UniversalParser.parse(self.rules)
		result = self._processor._run()
		if not result:
			raise Flaskvel._exception_class(self._processor.get_errors())
		return True

	def _validate_body_format(self):
		if self._expected_body_format == BodyFormats.ANY:
			return True
		elif self._expected_body_format == BodyFormats.JSON:
			if not self._request.is_json:
				time.sleep(0.5) # this fixes a bug that triggers "write EPIPE" on client side
				raise Flaskvel._exception_class("Request body is not a valid json")
			return True
		elif self._expected_body_format == BodyFormats.FORM:
			if self._request.is_json:
				time.sleep(0.5) # this fixes a bug that triggers "write EPIPE" on client side
				raise Flaskvel._exception_class("Request body is not a valid form")
			return True
		else:
			raise Flaskvel._exception_class("Invalid body format")

# methods: {"GET", "POST", "PUT", "DELETE"....}
# methods can be PipedString or Array or '*'
def validate(validator_class, expected_body_format=BodyFormats.ANY, run_on_methods="*"):
	def decorator(func):
		@wraps(func)
		def wrapper(*args, **kwargs):
			if run_on_methods == "*" or request.method in run_on_methods:
				validator_class(request, expected_body_format).validate()
			# else: validation ignored for other methods
			return func(*args, **kwargs)
		return wrapper
	return decorator

def validate_no_validator(rules, messages={}, expected_body_format=BodyFormats.ANY, run_on_methods="*"):
	def decorator(func):
		@wraps(func)
		def wrapper(*args, **kwargs):
			if run_on_methods == "*" or request.method in run_on_methods:
				validator = Validator(request, expected_body_format)
				validator.rules = rules
				validator.messages = messages
				validator.validate()
			# else: validation ignored for other methods
			return func(*args, **kwargs)
		return wrapper
	return decorator
