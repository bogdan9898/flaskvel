from flask import Flask
from flaskvel import Flaskvel, validate, BodyFormats, ValidationException

from MyValidator import MyValidator
# from MyValidator_json import MyValidator
from SizeValidator import SizeValidator
# from SizeValidator_json import SizeValidator

app = Flask(__name__)
# todo: add DefaultMessages translation units
Flaskvel(app, exception_class=ValidationException, error_code=400)

def custom_handler(value, params, **kwargs):
	print("~~~custom_handler")
	print(kwargs)
	print("~~~")
	return value in params
Flaskvel.register_rule('my_new_custom_rule', custom_handler, False)


@app.route("/", methods=["GET"])
@validate(MyValidator, BodyFormats.ANY)
def hello_world():
	return "Hello world!"

@app.route("/size", methods=["GET"])
@validate(SizeValidator, BodyFormats.ANY)
def hello_world2():
	return "Hello world!"

if __name__ == "__main__":
	app.run()

