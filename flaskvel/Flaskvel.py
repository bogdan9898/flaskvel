import traceback
from werkzeug.exceptions import BadRequest

from .Exceptions.ValidationException import ValidationException

class Flaskvel():
	error_code = 400

	def __init__(self, app, exception_class=ValidationException, error_code=400):
		Flaskvel.error_code = error_code
		app.register_error_handler(
			exception_class,
			Flaskvel.error_handler
		)
		app.register_error_handler(
			BadRequest,
			Flaskvel.error_handler
		)

	@staticmethod
	def error_handler(exception):
		if isinstance(exception, ValidationException):
			return exception.pretty_print(), Flaskvel.error_code
		else:
			traceback.print_exc()
			return exception, Flaskvel.error_code
