# FlaskVel

A small package that provides a convenient method to validate incoming HTTP requests with a variety of powerful validation rules, highly customizable and heavily influenced by Laravel.

#### Jump straight to the [documentation](https://bogdan9898.github.io/flaskvel).

---

## Instalation
To install FlaskVel run:
```
pip install flaskvel
```
FlaskVel is now installed, check out the [Quickstart](#quickstart).

> This package is only compatible with Python 3+.

---

## Quickstart
Lets suppose we want an endpoint that is used to register a user. First of all, we have to instantiate Flask and to also [initialize FlaskVel](https://bogdan9898.github.io/flaskvel/#/?id=initialization) by calling it's constructor with the appropriate parameters.

```python
# main.py

from flask import Flask, jsonify
from flaskvel import Flaskvel, validate, BodyFormats

app = Flask(__name__)
Flaskvel(app)
```

Now we are ready to define our endpoint.

```python
# main.py

@app.route("/register", methods=["POST"])
def register():
    # some code for registering the user
    # ...
    return jsonify({"status": "ok"}), 200
```

To add validations let's create a class that derives from `flaskvel.Validator` and contains the rules.

```python
# MyValidator.py

from flaskvel import Validator, Rules

class MyValidator(Validator):
    def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs) # MUST always be called first
        self.rules = {
            "username": ["required", "string"],
            "password": ["required", "string", "min:8", "max:32", "confimed"], 
            "email": [Rules.REQUIRED, Rules.EMAIL] # we can also use predefined constants instead of strings
        }
```

> For more info about writing rules see [Rules syntax](https://bogdan9898.github.io/flaskvel/#/?id=rules-syntax).

Now we can add our validator to the endpoint using [the decorator](https://bogdan9898.github.io/flaskvel/#/?id=the-decorator) provided by FlaskVel.

```python
@app.route("/register", methods=["POST"])
@validate(MyValidator, BodyFormats.ANY)
def register():
    return jsonify({"status": "ok"}), 200
```

> The decorator `@validate` must always be positioned after `@app.route`.

> You can find a list of all the rules [here](https://bogdan9898.github.io/flaskvel/#/rules).

---

#### Jump straight to the [documentation](https://bogdan9898.github.io/flaskvel).
