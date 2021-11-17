# Introduction

A small package that provides a convenient method to validate incoming HTTP requests with a variety of powerful validation rules, highly customizable and heavily influenced by Laravel.

---

# Instalation

To install FlaskVel run:

```bash
pip install flaskvel
```

FlaskVel is now installed. Check out the [Quickstart](#quickstart) or use the search bar on the left to quickly find what you need.

!> This package is only compatible with Python 3+.

---

# Quickstart

Lets suppose we want an endpoint that is used to register a user. First of all, we have to instantiate Flask and to also [initialize FlaskVel](#initialization) by calling the constructor with its appropriate parameters.

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
            "password": ["required", "string", "min:8", "max:32", "confirmed"],
            "email": [Rules.REQUIRED, Rules.EMAIL] # we can also use predefined constants instead of strings
        }
```

> For more info about writing rules see [Rules syntax](#rules-syntax).

Now we can add our validator to the endpoint using one of [the decorators](#the-decorators) provided by FlaskVel.

```python
@app.route("/register", methods=["POST"])
@validate(MyValidator, BodyFormats.ANY)
def register():
    return jsonify({"status": "ok"}), 200
```

!> The decorator used, `@validate(...)` or `@validate_no_validator(...)`, must be positioned after `@app.route(...)`.

> You can find a list of all the rules [here](rules).

---

# Initialization

```python
faskvel.Flaskvel(app, exception_class=flaskvel.ValidationException, error_code=400)
```

-   _app_ - object returned by Flask()
-   _exception_class_ - this parameter can be used to customize the format of the response sent when validation fails; see [Custom error response](#custom-error-response)
-   _error_code_ - HTTP status code returned when validation fails

---

# Exploring further

## The decorators

FlaskVel provides two decorators for you to easily trigger the validations without any extra code in the logic of your functions.

!> The decorator used, `@validate(...)` or `@validate_no_validator(...)`, must be positioned after `@app.route(...)`.

### 1. `validate`

This is the one we recommend and will be used in the entirety of the documentation. Down bellow you can find a short descripton of the parameters and a few examples.

```python
def validate(validator_class, expected_body_format=BodyFormats.ANY, run_on_methods="*")
```

- ***validator_class*** - your implementation of the abstract class `flaskvel.Validator` that should contain your desired rules and messages:

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

- ***expected_body_format*** - the type of body the validator should consider valid: `flaskvel.BodyFormat.JSON`, `flaskvel.BodyFormat.FORM` or `flaskvel.BodyFormat.ANY` to validate every type. By default is equal to `BodyFormats.ANY`.

!> If the body received has a different type, the validation will **FAIL** with an error similar to this:

```json
{
	"errors": "Request body is not a valid json",
	"status": "Validation failure"
}
```

- ***run_on_methods*** - an array of: `"GET"`, `"POST"`, `"PUT"` etc. Used to specify the methods for which the validator should run. By default is equal to `"*"`.

!> If the HTTP request is sent with another method than the one specified, the validation will just be ignored, **NOT** fail.

```python
# some examples on how should this decorator be used

@app.route("/register", methods=["GET", "POST"])
@validate(MyValidator, expected_body_format=BodyFormats.JSON, run_on_methods=["POST"])
def handler_register():
	# at this point FlaskVel will handle all the validations for you
	# in case of a failure an automatic response will be sent which of course can be customized (see [Custom error response](#custom-error-response))

	# your usual code for handling the route here
	pass

-----------------------------------------------------------------------------

@app.route("/home", methods=["GET"])
@validate(MyValidator, run_on_methods=["GET"])
def handler_home():
	# at this point FlaskVel will handle all the validations for you
	# in case of a failure an automatic response will be sent which of course can be customized (see [Custom error response](#custom-error-response))

	# your usual code for handling the route here
	pass

-----------------------------------------------------------------------------

@app.route("/login", methods=["POST"])
@validate(MyValidator, BodyFormats.FORM)
def handler_login():
	# at this point FlaskVel will handle all the validations for you
	# in case of a failure an automatic response will be sent which of course can be customized (see [Custom error response](#custom-error-response))

	# your usual code for handling the route here
	pass
```

### 2. `validate_no_validator`

This one can be used in case you don't want to create a whole entire class just to validate a single route.

```python
def validate_no_validator(rules, messages={}, expected_body_format=BodyFormats.ANY, run_on_methods="*")
```

- ***rules*** - An object containing the rules for the validation of each field. See [Rules syntax](#rules-syntax).

- ***messages*** - An object containing all the custom validation messages. See [Custom validation messages](#custom-validation-messages). By default is equal to `{}` which means that the messages provided by FlaskVel will be used instead.

- ***expected_body_format*** - the type of body the validator should consider valid: `flaskvel.BodyFormat.JSON`, `flaskvel.BodyFormat.FORM` or `flaskvel.BodyFormat.ANY` to validate every type. By default is equal to `BodyFormats.ANY`.

!> If the body received has a different type, the validation will **FAIL** with an error similar to this:

```json
{
	"errors": "Request body is not a valid json",
	"status": "Validation failure"
}
```

- ***run_on_methods*** - an array of: `"GET"`, `"POST"`, `"PUT"` etc. Used to specify the methods for which the validator should run. By default is equal to `"*"`.

!> If the HTTP request is sent with another method than the one specified, the validation will just be ignored, **NOT** fail.

```python
# some examples on how should this decorator be used

@app.route("/register", methods=["GET", "POST"])
@validate_no_validator(
	rules={
		"username": "string",
		"password": "string|confirmed|min:8|max:16"
	},
	messages={
		"username.string": "Username must be a string",
		"password.string": "Password must be a string",
		"password.cofirmed": "The confirmed password does not match",
		"password.min": "The password must be between 8-16 characters long",
		"password.max": "The password must be between 8-16 characters long",
	},
	expected_body_format=BodyFormats.JSON, 
	run_on_methods=["POST"])
def handler_register():
	# at this point FlaskVel will handle all the validations for you
	# in case of a failure an automatic response will be sent which of course can be customized (see [Custom error response](#custom-error-response))

	# your usual code for handling the route here
	pass
```

---

## Rules syntax

!> The rules are case sensitive.

There are 3 ways in which validation rules can be asigned to fields:

### 1. Single rule

```python
self.rules = {
	'username': "required",
	'title': Rules.NULLABLE, # we can also use predefined constants instead of strings, don't forget to import flaskvel.Rules
	'description': "required_with:title",
	'genre': "nullable"
}
```

### 2. Arrays with multiple rules

```python
self.rules = {
	'username': ["required", "string"],
	'title': [Rules.NULLABLE, Rules.STRING],
	'description': ["required_with:title', 'string', 'max:256"],
	'genre': ["nullable", "in:thriller,fantasy,romance"]
}
```

### 3. Piped strings

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

---

## Custom validation messages

By default, FlaskVel offers a set of default validation failure messages that you can find [here](https://github.com/bogdan9898/flaskvel/blob/master/flaskvel/Constants/DefaultMessages.py), but the validator prioritizes your own messages if you provide them. To do so, override the `messages` attribute inside your own validator class. This attribute should be a `dict` of _field_name.rule_ and their corresponding error messages.

### 1. Static messages

-   Simple to use, hardcoded strings

```python
from flaskvel import Validator, Rules

class CustomValidator(Validator):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.rules = {
			"username": ["required", "string"],
			"password": ["required", "string", "min:8", "max:32", "confirmed"],
			"email": [Rules.REQUIRED, Rules.EMAIL]
		}

		self.messages = {
			"username.string": "Username must be a string",
			"password.min": "Password must be between 8 and 32",
			"password.max": "Password must be between 8 and 32",
			"password.confirmed": "Please confirm your password",
			"email.required": "Email address is required"
		}
```

### 2. Dynamic messages

-   These messages are parameterized strings that are formated after all rules are validated by the [processor](#processor). In the next example we'll [register a new rule](#_2-registered-rules) named `my_custom_rule` just for demonstration purposes:

```python
# main.py

def my_handler(err_msg_params, **kwargs): # go to [1. Unregstered rules] to read about all the arguments that a handler functions can have
	# we can use err_msg_params to pass information to the final error message
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
			"test_field": ['required', 'my_custom_rule:param1,param2,param3'],
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

---

## Custom error response

By default, if the validation fails, the response will have HTTP error status code 400 and will be similar to this:

```json
{
	"errors": {
		"password": [
			"The password field does not match it's confirmation.",
			"The password field must have more than 6 characters."
		],
		"username": ["The username field is required.", "The username field must be a string."]
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

Don't forget to tell FlaskVel to use the exception just created and change the HTTP error status code to another value if you want to. As of now you can only do it for all routes at once as shown in the code snippet bellow:

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
		"username": ["The username field is required.", "The username field must be a string."]
	},
	"validation": "failed"
}
```

---

## Stopping on first validation failure

Sometimes you may wish to stop running the validation after the first failure. To do so, assign [bail](rules#bail) to the field:

```python
self.rules = {
	"post": "bail|required|string",
	"comments": "nullable|array"
}
```

---

## Nested Attributes

If your HTTP request contains nested parameters, you may specify them in your validation rules using “dot” syntax:

```python
self.rules = {
    "user.id": "required",
    "user.email": "required",
}
```

---

## Custom rules

Besides [the rules offered by default](rules), you can extend the validator with your own custom rules. FlaskVel offers 2 ways to do so:

### 1. Unregistered rules

The easiest way to expand FlaskVel's functionality is to write your own `handlers` and pass them directly as rules to the validator. Every `handler` is a function that must satisfy the following conditions:

-   it must return either `True` or `False`
-   it will receive the folowing keyword parameters:
    -   `value` - the value of the field being validated
    -   `field_name` - the name of the field being validated
    -   `params` - a list of all the parameters of the rule
    -   `nullable` - is `True` if the field has been specified as [nullable](rules#nullable), `False` otherwise
    -   `err_msg_params` - a `dict` object where you can insert data for [dynamic validation messages](#_2-dynamic-messages)
    -   `processor` - an instance of the [Processor](#processor) class that called the `handler`; used to get information about other fields
    -   `rules` - a list of all the rules of the field being validated

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

Although it's possible to pass arguments to the unregistered rules, it's recomended to use [Registered rules](#2-registered-rules) for more complex use cases. In the following example we'll take a look at how to do it for a rule similar to the one above. For that we have to create an object of type `flaskvel.ParsedRule` and pass the parameters in a list as following:

```python
# MyValidator.py

from flaskvel import Validator, Rules, ParsedRule

class MyValidator(Validator):
    def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.rules = {
			"order_number": [Rules.NUMERIC, ParsedRule(self.is_divisible, [2])], # pass a list containing the params for 'is_divisible'
		}

		self.messages = {
			"order_number.is_divisible": "Order number must be divisible by {divisor}"
		}

	def is_divisible(self, value, params, err_msg_params, **kwargs):
		err_msg_params['divisor'] = params[0] # populate err_msg_params to customize the message defined above
		return int(value) % params[0] == 0
```

> For more details on how to get another field's values, to check if another field is nullable etc. see [Processor](#processor).

### 2. Registered rules

Registered rules are rules that can be used with the [default rules syntax](#rules-syntax), just like the ones provided by FlaskVel. The `handlers` for this type of rules must satisfy exactly the same condition as the ones for [Unregistered rules](#1-unregistered-rules)
Although this proccess requires a bit of setup, it is recomended when you want to pass params to an unregistered rule more than one time.

The function `flaskvel.Flaskvel.register_rule` has the following signature:

```python
def register_rule(rule, handler, is_null_tolerant=True)
```

-   ***rule*** - the name of the rule to be registered as a string
-   ***handler*** - the function implementing the rule
-   ***is_null_tolerant*** - whether or not the rule is null tolerant. If the rule is null tolerant, the field is specified as being [nullable](rules#nullable) and its value is `None` then the validation passes by default. If you want your rule to be checked no matter what then this parameter should be `False`. This option has no effect on fields that are not specified as being [nullable](rules#nullable). All of the rules provided by Flaskvel are null tolerant except for: [required](rules#required), [required_if](rules#required_ifanother_fieldvalue1value2), [required_unless](rules#required_unlessanother_fieldvalue1value2), [required_with](rules#required_withfoobar), [required_with_all](rules#required_with_allfoobar), [required_without](rules#required_withoutfoobar), [required_without_all](rules#required_without_allfoobar), [present](rules#present), [filled](rules#filled).

Let's take the example above and register a new rule named `divisible`:

!> Be carefull when choosing a name because you risk overriding the default behavior of a rule already defined by FlaskVel with the same name. You can find a full list of all rules [here](rules).

```python
# main.py

def is_divisible(value, params, err_msg_params, **kwargs):
	err_msg_params['divisor'] = params[0]
	return int(value) % int(params[0]) == 0

Flaskvel.register_rule('divisible', is_divisible)
```

And just like that our new rule is registered. Now let's get some use out of it:

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

> You can override the default `handler` of a rule provided by FlaskVel by registering one with the same name and your own `handler` instead, except for [bail](rules#bail) and [nullable](rules#nullable), their behaviour **CANNOT** be overridden.

---

## Manual validation

If you want to validate the data at a specific point during the HTTP request, you can execute the validation manually. To do so, remove [the decorator](#the-decorators), initialize your own validator class and call `validator.validate()`. Don't forget to wrap this call in a `Try/Except` block and treat the `ValidationException` as following:

!> The `Validator` provided by FlaskVel should be treated as an abstract class and **NOT** be instantiated.

```python
# main.py

from flask import Flask, jsonify, request
from flaskvel import Flaskvel, BodyFormats, ValidationException

from CustomValidator import CustomValidator # write your own validator in CustomValidator.py as seen in [Quickstart](#quickstart)

app = Flask(__name__)
Flaskvel(app)

@app.route("/validation/manual", methods=["POST"])
def manualValidation():
	validator = CustomValidator(request=request, expected_body_format=BodyFormats.FORM)
	try:
		validator.validate()
		return "Hello automated world!"
	except ValidationException as e:
		errors = validator.get_validation_errors()
		processor = validator.get_processor()
		# ...
		# code to handle the errors
		# ...
	return "Sorry, your sent the wrong data."
```

---

## Processor

This class is responsible for processing the validation of every rule. When it calls a `handler` function, a reference to the processor instance is passed as a keyword parameter. You can use it to gather details about other fields using the following methods:

```python
def get_errors(self)
```

-   Returns a list of all the errors so far.

```python
def get_failed_validations(self)
```

-   Returns a list of all the failed validations in detail so far.

```python
def get_field_type(self, field_name)
```

-   Returns one of the following values: `flaskvel.FieldTypes.STRING`, `flaskvel.FieldTypes.NUMERIC`, `flaskvel.FieldTypes.ARRAY`, `flaskvel.FieldTypes.JSON`, `flaskvel.FieldTypes.FILE`, `flaskvel.FieldTypes.UNKOWN`. We recommend you to specify the type of every field ([string](rules#string), [numeric](rules#numeric), [array](rules#array), [json](rules#json), [file](rules#file)) otherwise the processor will try to guess it.

!> Even if you specify the type of a field, it will still be validated, if this fails then `flaskvel.FieldTypes.UNKOWN` is returned.

```python
def get_field_value(self, field_name)
```

-   Returns the value of a field. If the field is not present then returns `None`.

```python
def get_field_rules(self, field_name)
```

-   Returns a list of all the rules of a field.

```python
def is_field_present(self, field_name)
```

-   Returns either `True` or `False` depending on whether or not the specified field is [present](rules#present). A field is considered present even if is sent with `None` as its value.

```python
def is_field_nullable(self, field_name)
```

-   Returns either `True` or `False` depending on whether or not the field is [nullable](rules#nullable).

```python
def should_bail(self, field_name)
```

-   Returns either `True` or `False` depending on whether or not the field contains the [bail](rules#bail) rule.

---

# Contributions

Any form of contribution is welcome!
