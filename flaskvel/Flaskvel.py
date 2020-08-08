import traceback
from werkzeug.exceptions import BadRequest

from .Constants.RulesPredicates import RulesPredicates
from .Exceptions.ValidationException import ValidationException

class Flaskvel():
	_error_code = 400

	_registered_rules = {}
	_null_intolerant_rules = [
		RulesPredicates.REQUIRED,
		RulesPredicates.REQUIRED_IF,
		RulesPredicates.REQUIRED_UNLESS,
		RulesPredicates.REQUIRED_WITH,
		RulesPredicates.REQUIRED_WITH_ALL,
		RulesPredicates.REQUIRED_WITHOUT,
		RulesPredicates.REQUIRED_WITHOUT_ALL,
		RulesPredicates.PRESENT,
		RulesPredicates.FILLED,
	]

	_exception_class = ValidationException

	def __init__(self, app, exception_class=ValidationException, error_code=400):
		Flaskvel._error_code = error_code
		Flaskvel._exception_class = exception_class
		app.register_error_handler(
			exception_class,
			Flaskvel._error_handler
		)
		app.register_error_handler(
			BadRequest,
			Flaskvel._error_handler
		)

	@staticmethod
	def _error_handler(exception):
		if isinstance(exception, ValidationException):
			return exception.pretty_print(), Flaskvel._error_code
		else:
			traceback.print_exc()
			return exception, Flaskvel._error_code

	@staticmethod
	def register_rule(rule, handler, is_null_tolerant=True):
		if not isinstance(rule, str):
			raise Exception("Rule must be a string")
		if not callable(handler):
			raise Exception("Handler must be callable")

		if not is_null_tolerant:
			Flaskvel._null_intolerant_rules.append(rule)

		Flaskvel._registered_rules[rule] = handler