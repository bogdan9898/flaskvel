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
	def __init__(self, request, body_format=BodyFormats.ANY):
		self._request = request
		self._body_format = body_format
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
		if self._body_format == BodyFormats.ANY:
			return True
		elif self._body_format == BodyFormats.JSON:
			if not self._request.is_json:
				time.sleep(0.5) # this fixes a bug that triggers "write EPIPE" on client side
				raise Flaskvel._exception_class("Request body is not a valid json")
			return True
		elif self._body_format == BodyFormats.FORM:
			if self._request.is_json:
				time.sleep(0.5) # this fixes a bug that triggers "write EPIPE" on client side
				raise Flaskvel._exception_class("Request body is not a valid form")
			return True
		else:
			raise Flaskvel._exception_class("Invalid body format")

# methods: {"GET", "POST", "PUT", "DELETE"....}
# methods=PipedString or Array or '*'
# methods: methods for which the Flaskvel should validate the body; default = "*"(all methods)
def validate(validator_class, body_format=BodyFormats.ANY, methods="*"):
	def decorator(func):
		@wraps(func)
		def wrapper(*args, **kwargs):
			if methods == "*" or request.method in methods:
				validator_class(request, body_format).validate()
			# else: validation ignored for other methods
			return func(*args, **kwargs)
		return wrapper
	return decorator