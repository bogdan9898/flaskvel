from flask import Flask
from flaskvel import Flaskvel, validate, BodyFormats, ValidationException

from MyValidator import MyValidator
# from MyValidator_json import MyValidator
from SizeValidator import SizeValidator
# from SizeValidator_json import SizeValidator
from CustomValidator import CustomValidator
from MyCustomException import MyCustomException

app = Flask(__name__)
# todo: add DefaultMessages translation units
# Flaskvel(app, exception_class=MyCustomException, error_code=403)
Flaskvel(app)

def custom_handler(value, params, **kwargs):
	return value in params
Flaskvel.register_rule('my_new_custom_rule', custom_handler, False)


@app.route("/", methods=["POST"])
@validate(MyValidator, BodyFormats.FORM)
def hello_world():
	return "Hello world!"

@app.route("/size", methods=["POST"])
@validate(SizeValidator, BodyFormats.FORM)
def size_testing():
	return "Hello world!"

@app.route("/test", methods=["POST"])
@validate(CustomValidator, BodyFormats.ANY)
def confirmation():
	return "Hello from test world!"

if __name__ == "__main__":
	app.run()

