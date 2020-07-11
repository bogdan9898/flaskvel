from flask import jsonify

class ValidationException(Exception):
	def __init__(self, message):
		super().__init__(message)
		self._message = message

	def pretty_print(self):
		return jsonify({
			'status': 'Validation failure',
			'errors': self._message
		})