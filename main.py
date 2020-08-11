from flask import Flask, request
from flaskvel import Flaskvel, validate, BodyFormats, ValidationException
import flaskvel

from MyValidator import MyValidator
# from MyValidator_json import MyValidator
from SizeValidator import SizeValidator
# from SizeValidator_json import SizeValidator
from CustomValidator import CustomValidator
from MyCustomException import MyCustomException
from CustomValidator2 import CustomValidator2

app = Flask(__name__)
# todo: add DefaultMessages translation units
# Flaskvel(app, exception_class=MyCustomException, error_code=403)
Flaskvel(app)

def custom_handler(value, params, **kwargs):
	return value in params
Flaskvel.register_rule('my_new_custom_rule', custom_handler, False)

def is_divisible(value, params, err_msg_params, **kwargs):
		err_msg_params['divisor'] = params[0] # we populate err_msg_params to customize the message defined above
		return int(value) % int(params[0]) == 0

Flaskvel.register_rule('divisible', is_divisible)

def my_handler(field_name, err_msg_params, **kwargs):
	# you can use err_msg_params to pass informtion to the final error message
	err_msg_params['random_words_list'] = ["agreement", "force", "fluttering", "treat", "jam"]
	err_msg_params['link'] = "https://youtu.be/dQw4w9WgXcQ"
	err_msg_params['field_name'] = field_name
	result = False
	# ...
	# do your validation here
	# ...
	return result

Flaskvel.register_rule('my_custom_rule', my_handler)


@app.route("/", methods=["POST"])
@validate(MyValidator, BodyFormats.FORM)
def hello_world():
	return "Hello world!"

@app.route("/size", methods=["POST"])
@validate(SizeValidator, BodyFormats.FORM)
def size_testing():
	return "Hello world!"

@app.route("/test", methods=["POST"])
@validate(CustomValidator)
def test():
	return "Hello from test world!"

@app.route("/validation/manual", methods=["POST"])
def manualValidation():
	validator = CustomValidator(request=request, body_format=BodyFormats.FORM)
	try:
		validator.validate()
		return "Hello from \"not an automated\" world!"
	except flaskvel.ValidationException as e:
		errors = validator.get_validation_errors()
		processor = validator.get_processor()
		# ...
		# code to handle the errors
		# ...
	return "Sorry, your sent the wrong body."

if __name__ == "__main__":
	app.run()

