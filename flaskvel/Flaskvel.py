from .ValidationException import ValidationException


class Flaskvel():
	error_code = 400

	def __init__(self, app, exception_class=ValidationException, error_code=400):
		Flaskvel.error_code = error_code
		app.register_error_handler(
			exception_class,
			Flaskvel.error_handler
		)

	@staticmethod
	def error_handler(exception):
		return exception.pretty_print(), Flaskvel.error_code