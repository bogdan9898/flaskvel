from flask import Flask
from flaskvel import Flaskvel, validate, BodyFormats, ValidationException

from MyValidator import MyValidator

app = Flask(__name__)
# todo: add DefaultMessages translation units
Flaskvel(app, exception_class=ValidationException, error_code=400)

@app.route("/", methods=["GET"])
@validate(MyValidator, BodyFormats.ANY)
def hello_world():
	return "Hello world!"

if __name__ == "__main__":
	app.run()

