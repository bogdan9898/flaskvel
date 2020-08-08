from flask import jsonify
from flaskvel import ValidationException

class MyCustomException(ValidationException):
	def pretty_print(self):
		return jsonify({
			"validation": "failed",
			"reasons": self._message
		})