# Introduction
A small package that provides a convenient method to validate incoming HTTP requests with a variety of powerful validation rules, highly customizable and heavily influenced by Laravel.

---

# Instalation
To install FlaskVel run:
```
pip install flaskvel
```
FlaskVel is now installed. Check out the [Quickstart](#quickstart) or use the search bar on the left to quickly find what you need.

!> This package is only compatible with Python 3+.

---

# Quickstart
Lets suppose we want an endpoint that is used to register a user. First of all, we have to instantiate Flask and to also [initialize FlaskVel](#initialization) by calling it's constructor with the appropriate parameters.

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

> For more info about writing rules see [Rules syntax](#rules-syntax).

Now we can add our validator to the endpoint using [the decorator](#the-decorator) provided by FlaskVel.

```python
@app.route("/register", methods=["POST"])
@validate(MyValidator, BodyFormats.ANY)
def register():
    return jsonify({"status": "ok"}), 200
```

!> The decorator `@validate` must always be positioned after `@app.route`.

> You can find a list of all the rules [here](rules).

---

# Initialization

```python
faskvel.Flaskvel(app, exception_class=flaskvel.ValidationException, error_code=400)
```
- *app* - object returned by Flask()
- *exception_class* - this parameter can be used to customize the format of the response sent when validation fails; see [Custom error response](#custom-error-response)
- *error_code* - HTTP status code returned when validation fails

---

# Exploring further

## The decorator

```python
def validate(validator_class, body_format=BodyFormats.ANY, methods="*")
```

- ***validator_class*** - a class derived from `flaskvel.Validator` that contains the desired rules and messages:

```python
# MyValidator.py

class MyValidator(Validator):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs) # MUST always be called first
    self.rules = {
            ...
    }

    self.messages = {
      ...
    }
```
- ***body_format*** - the type of body that the validator should consider valid: `flaskvel.BodyFormat.JSON`, `flaskvel.BodyFormat.FORM` or `flaskvel.BodyFormat.ANY` to validate every type.

!> If the body received has a different type, the validation will **fail** with an error similar to this:

```json
{
  "errors": "Request body is not a valid json",
  "status": "Validation failure"
}
```

- ***methods*** - an array of: `"GET"`, `"POST"`, `"PUT"` etc. Used to specify the methods for which the validator should do it's job.

!> If the HTTP request is sent with another method than the one specified, the validation will just be ignored, **NOT** fail.

```python
# a few examples how to use it

@validate(MyValidator, body_format=BodyFormats.JSON, methods=["POST", "PUT"])

-----------------------------------------------------------------------------

@validate(MyValidator, methods=["GET"])

-----------------------------------------------------------------------------

@validate(MyValidator, body_format=BodyFormats.FORM)
```

!> The decorator `@validate(...)` must be positioned after `@app.route(...)`.

## Rules syntax

!> The rules are case sensitive.

There are 2 ways in which validation rules can be asigned to fields:

1. Single rule:

  ```python
  self.rules = {
  'username': "required",
  'title': Rules.NULLABLE, # we can also use predefined constants instead of strings, don't forget to import flaskvel.Rules
  'description': "required_with:title",
  'genre': "nullable"
  }
  ```

2. Arrays of multiple rules:

  ```python
  self.rules = {
  'username': ["required", "string"],
  'title': [Rules.NULLABLE, Rules.STRING],
  'description': ["required_with:title', 'string', 'max:256"],
  'genre': ["nullable", "in:thriller,fantasy,romance"]
  }
  ```

3. Piped strings:
  
  !> Piped strings are **NOT** allowed inside arrays.

  !> We recommend to not use piped strings when working with [regex](rules#regexpattern) and [not_regex](rules#not_regexpattern).

  ```python
  self.rules = {
  'username': "required|string",
  'title': "nullable|string",
  'description': "required_with:title|string|max:256",
  'genre': "nullable|in:thriller,fantasy,romance"
  }
  ```

## Custom validation messages

By default, FlaskVel offers a set of default validation failure messages that you can find [here](https://github.com/bogdan9898/flaskvel/blob/master/flaskvel/Constants/DefaultMessages.py), but the validator prioritizes your own messages if you provide them. To do so, override the `messages` attribute inside your own validator class. This attribute should be a `dict` of *field_name.rule* pairs and their corresponding error messages.

### 1. Static messages 

- Simple to use, hardcoded strings

```python
from flaskvel import Validator, Rules

class CustomValidator(Validator):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.rules = {
      "username": ["required", "string"],
      "password": ["required", "string", "min:8", "max:32", "confirmed"], 
      "email": [Rules.REQUIRED, Rules.EMAIL] # we can also use predefined constants instead of strings
    }
    
    self.messages = {
      "username.string": "Type of username is invalid",
      "password.min": "Password must be between 8 and 32",
      "password.max": "Password must be between 8 and 32",
      "password.confirmed": "Please confirm your password",
      "email.required": "Email address is required"
    }
```

### 2. Dynamic messages

- These messages are parameterized string that are formated after all rules are validated by the [processor](#processor) as following:

```python
message.format(*params, **err_msg_params)
```

- *params* - a list of all the params of that rule
- *err_msg_params* - `dict` object containig all your custom arguments populated inside the `handler` function

In the next example we'll [register a new rule](#_2-registered-rules) named `my_custom_rule` just for demonstration purposes:
```python
# main.py

def my_handler(err_msg_params, **kwargs): # go to [1. Unregstered rules] to read about all the arguments that a handler functions can have
  # you can use err_msg_params to pass information to the final error message
  err_msg_params['random_words_list'] = ["agreement", "force", "fluttering", "treat", "jam"]
  err_msg_params['quickstart_demo'] = "https://youtu.be/dQw4w9WgXcQ"
  err_msg_params['field_name'] = field_name
  result = False
  # ...
  # complex validation code
  # ...
  return result

Flaskvel.register_rule('my_custom_rule', my_handler)
```

Now create the validator class which uses a dynamic message.

```python
# MyValidator.py

from flaskvel import Validator, Rules, ParsedRule

class MyValidator(Validator):
    def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      self.rules = {
        "test_field": [Rules.REQUIRED, 'my_custom_rule:param1,param2,param3'],
      }

      self.messages = {
        "test_field.my_custom_rule": "My name is {field_name}, these are my parameters: {0}, {1}, {2}, here is a demo: {quickstart_demo} and a list of random words: {random_words_list}."
      }
```

If our validation fails, we should get a response like this:

```json
{
  "errors": {
    "test_field": [
      "My name is test_field, these are my parameters: param1, param2, param3, here is a demo: https://youtu.be/dQw4w9WgXcQ and a list of random words: ['agreement', 'force', 'fluttering', 'treat', 'jam']."
    ]
  },
  "status": "Validation failure"
}
```

## Custom error response
By default, if the validation fails, the response will have HTTP error status code 400 and will be similar to this:

```json
{
  "errors": {
    "password": [
      "The password field does not match it's confirmation.",
      "The password field must have more than 6 characters."
    ],
    "username": [
      "The username field is required.",
      "The username field must be a string."
    ]
  },
  "status": "Validation failure"
}
```

But we can customize it however we want. Let's create a class that inherits `flaskvel.ValidationException`.

```python
# MyCustomException.py

from flask import jsonify
from flaskvel import ValidationException

class MyCustomException(ValidationException):
  def pretty_print(self):
    return jsonify({
      "validation": "failed",
            "reasons": self._message, # self._message contains all the validation errors
    })
```

Don't forget to tell FlaskVel to use the class just created and change the HTTP error status code to another value if you want to.

```python
# main.py

from flask import Flask, jsonify
from flaskvel import Flaskvel, validate, BodyFormats

from MyCustomException import MyCustomException

app = Flask(__name__)
Flaskvel(app, exception_class=MyCustomException, error_code=403)
```

Now the failed validation responses should have HTTP status code 403 and look like this:

```json
{
  "reasons": {
    "password": [
      "The password field does not match it's confirmation.",
      "The password field must have more than 6 characters."
    ],
    "username": [
      "The username field is required.",
      "The username field must be a string."
    ]
  },
  "validation": "failed"
}
```

## Stopping on first validation failure
Sometimes you may wish to stop running the validation after the first failure. To do so, assign [bail](rules#bail) to the field:

```python
self.rules = {
  "post": "bail|required|string",
  "comments": "nullable|array"
}
```

## Nested Attributes
If your HTTP request contains “nested” parameters, you may specify them in your validation rules using “dot” syntax:

```python
self.rules = {
    "user.id": "required",
    "user.email": "required",
}
```

## Custom rules
Besides the rules offered by default, you can extend the validator with your own custom rules. FlaskVel offers 2 ways to add your own custom rules.

### 1. Unregistered rules
The easiest way to expand FlaskVel's functionality is to write your own `handlers` and pass them directly as rules to the validator. Every `handler` is a function that must satisfy the following conditions:
- it must return either `True` or `False`
- it will receive the folowing keyword parameters:
  - `value` - the value of the field being validated
  - `field_name` - the name of the field being validated
  - `params` - a list of all the parameters of the rule
  - `nullable` - is `True` if the field has been specified as [nullable](rules#nullable), `False` otherwise
  - `err_msg_params` - a `dict` object where you can insert data for [custom validation messages](#custom-validation-messages)
  - `processor` - an instance of the [Processor](#processor) class that called the `handler`, used to get information about other fields
  - `rules` - a list of all the rules of the field being validated

Let's suppose we want `order_number` field to be an even number. We proceed by declaring a handler named `is_even` and assigning it to the field.

```python
# MyValidator.py

from flaskvel import Validator, Rules

class MyValidator(Validator):
    def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      self.rules = {
        "order_number": [Rules.NUMERIC, self.is_even]
      }

      self.messages = {
        "order_number.is_even": "Order number must be even"
      }

    def is_even(self, value, **kwargs):
      return int(value) % 2 == 0
```

If we want to pass parameters to an unregistered rule, we have to create an intance of `flaskvel.ParsedRule` and pass the parameters in a list as following:

```python
# MyValidator.py

from flaskvel import Validator, Rules, ParsedRule

class MyValidator(Validator):
    def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      self.rules = {
        "order_number": [Rules.NUMERIC, ParsedRule(self.is_divisible, [2])], # pass a list containig the params for is_divisible
      }

      self.messages = {
        "order_number.is_divisible": "Order number must be divisible by {divisor}"
      }

  def is_divisible(self, value, params, err_msg_params, **kwargs):
    err_msg_params['divisor'] = params[0] # populate err_msg_params to customize the message defined above
    return int(value) % params[0] == 0
```

For more details on how to get another field's values, check if nullable etc. see [Processor](#processor).

### 2. Registered rules
Registered rules are rules that can be used with the [default rules syntax](#rules-syntax), just like the ones provided by FlaskVel. The `handlers` for this type of rules must satisfy exactly the same condition as the ones for [Unregistered rules](#1-unregistered-rules)
Although this proccess requires a bit of setup, it is recomended when you want to pass params to an unregistered rule more than one time.

Let's take the example above and register a new rule named `divisible`.

!> Be carefull when choosing a name because you risk overriding the default handler for a rule already defined by FlaskVel with the same name. You can find a full list of all rules [here](rules).

```python
# main.py

def is_divisible(value, params, err_msg_params, **kwargs):
    err_msg_params['divisor'] = params[0]
    return int(value) % int(params[0]) == 0

Flaskvel.register_rule('divisible', is_divisible)
```

And just like that our new rule is registered.

```python
# MyValidator.py

from flaskvel import Validator, Rules, ParsedRule

class MyValidator(Validator):
    def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      self.rules = {
        "order_number": [Rules.NUMERIC, 'divisible:2']
      }

      self.messages = {
        "order_number.divisible": "Order number must be divisible by {divisor}"
      }
```

> You can override the `handler` of a rule provided by FlaskVel by registering one with the same name and your own `handler` instead, except for [bail](rules#bail) and [nullable](rules#nullable), their behaviour **CANNOT** be overridden.

The function `flaskvel.Flaskvel.register_rule` has the following signature:

```python
def register_rule(rule, handler, is_null_tolerant=True)
```
- ***rule*** - the name of the rule to be registered
- ***handler*** - the function implementing the rule
- ***is_null_tolerant*** - whether or not the rule is null tolerant. If the rule is null tolerant and the field is specified as being [nullable](rules#nullable) and it's value is `None` then the `handler` for this rule is ignored. If you want your rule to be verified no matter what than this parameter should be `False`

## Manual validation
If you want to validate the data at a specific point during the HTTP request, you can execute the validation manually. To do so, remove [the decorator](#the-decorator), initialize your own validator class and call `validator.validate()`. Don't forget to wrap this call in a `Try Except` block.

!> The `Validator` provided by FlaskVel should be treated as an abstract class and **NOT** be instantiated.

```python
# main.py
from flask import Flask, jsonify, request
from flaskvel import Flaskvel, BodyFormats, ValidationException

from CustomValidator import CustomValidator # write your own validator in CustomValidator.py

app = Flask(__name__)
Flaskvel(app)

@app.route("/validation/manual", methods=["POST"])
def manualValidation():
	validator = CustomValidator(request=request, body_format=BodyFormats.FORM)
	try:
		validator.validate()
		return "Hello from \"not an automated\" world!"
	except ValidationException as e:
		errors = validator.get_validation_errors()
		processor = validator.get_processor()
		# ...
		# code to handle the errors
		# ...
	return "Sorry, your sent the wrong body."
```

## Processor

This class is responsible for processing the validation of every rule defined by default in FlaskVel, and manage all the other custom rules. When calling a `handler` function, a reference to the processor instance is passed as a keyword parameter. You can use it to gather details about other fields using the following methods:

```python
def get_errors(self)
```

- Returns a list of all the errors so far.

```python
def get_failed_validations(self)
```

- Returns a list of all the failed validations in detail so far.

```python
def get_field_type(self, field_name)
```

- Returns one of the following values: `flaskvel.FieldTypes.STRING`, `flaskvel.FieldTypes.NUMERIC`, `flaskvel.FieldTypes.ARRAY`, `flaskvel.FieldTypes.JSON`, `flaskvel.FieldTypes.FILE`, `flaskvel.FieldTypes.UNKOWN`. We recommend you to specify the type of every field ([string](rules#string), [numeric](rules#numeric), [array](rules#array), [json](rules#json), [file](rules#file)) otherwise the processor will try to guess it.

!> Even if you specify the type of a field, it will still be validated, if this fails then `flaskvel.FieldTypes.UNKOWN` is returned.

```python
def get_field_value(self, field_name)
```

- Returns the value of the field. If the field is not present then returns `None`.

```python
def get_field_rules(self, field_name)
```

- Returns a list of all the rules of the field.

```python
def is_field_present(self, field_name)
```

- Returns either `True` or `False` depending on whether or not the field is present. A field is considered present even if is sent with `None` as it's value.

```python
def is_field_nullable(self, field_name)
```

- Returns either `True` or `False` depending on whether or not the field is [nullable](rules#nullable).

```python
def should_bail(self, field_name)
```

- Returns either `True` or `False` depending on whether or not the field contains the [bail](rules#bail) rule.

---

# Contributions
Any form of contribution is welcome!











