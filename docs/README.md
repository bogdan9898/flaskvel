# Introduction
A small package that provides a convenient method to validate incoming HTTP requests with a variety of powerful validation rules, highly customizable and heavily influenced by Laravel.

---

# Instalation
To install FlaskVel run:
```
pip install flaskvel
```
FlaskVel is now installed. Check out the [Quickstart](#quickstart) or use the list on the left to quickly find what you need.

!> This package only works with Python 3

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

!> `@validate` must be positioned after `@app.route`.

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
def validate(validator_class, body_format, methods="*")
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
- ***body_format*** - the type of body that the validator should consider valid: `flaskvel.BodyFormat.JSON`, `flaskvel.BodyFormat.FORM` or `flaskvel.BodyFormat.ANY` to validate every type. If the body received has a different type, the validation will fail:

```json
{
  "errors": "Request body is not a valid json",
  "status": "Validation failure"
}
```

- ***methods*** - an array of: `"GET"`, `"POST"`, `"PUT"` etc. Used to specify the methods for which the validator should do it's job.

!> If the HTTP request is sent with another method than the one specified, the validation will just be ignored, **NOT** fail.

```python
@validate(MyValidator, BodyFormats.JSON, methods=["POST", "PUT"])
```

!> `@validate` must be positioned after `@app.route`.

## Rules syntax

!> The rules are case sensitive.

There are 2 ways in which validation rules can be asigned to fields:

1. Single rule:

  ```python
  self.rules = {
  'username': "required",
  'title': Rules.NULLABLE, # we can also use predefined constants instead of strings
  'description': "required_with:title"
  }
  ```

2. Arrays of multiple rules:

  ```python
  self.rules = {
  'username': ["required", "string"],
  'title': [Rules.NULLABLE, Rules.STRING],
  'description': ["required_with:title', 'string', 'max:256"]
  }
  ```

3. Piped strings:
  
  !> Piped strings are **NOT** allowed inside arrays.

  ```python
  self.rules = {
  'username': "required|string",
  'title': "nullable|string",
  'description': "required_with:title|string|max:256"
  }
  ```

## Custom validation messages

By default, FlaskVel offers a set of default validation failure messages that you can find [here](https://github.com/bogdan9898/flaskvel/blob/master/flaskvel/Constants/DefaultMessages.py), but the validator prioritizes your own messages if you provide them. To do so, override the `messages` attribute inside your own validator. This attribute should be an array of *field_name.rule* pairs and their corresponding error messages.

1. Static messages

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
      "password": "Please confirm your password",
      "email.required": "Email address is required"
    }
```

2. Dynamic messages
These messages can receive parameters from the validator. By default, a few arguments are provided: `field_name` as a keyword param and a list of all the params of that rule. 
```python
message.format(*params, field_name=field_name, **err_msg_params)
```



todo: write a good explaination for this shit...
Daca dorim putem customiza aceste mesaje punandu le la dispozitie niste argumente speciale, le vom numi err_msg_params. Acest obiect va fi de tipul `dict` si va fi populat de catre functia `handler` a fiecare reguli. 


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
Sometimes you may wish to stop running the validation after the first failure. To do so, assign [bail](#bail) to the field:

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
  - `nullable` - is `True` if the field has been specified as [nullable](#nullable), `False` otherwise
  - `err_msg_params` - a `dict` object where you can insert parameters for [custom validation messages](#custom-validation-messages)
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
      "order_number": [Rules.NUMERIC, ParsedRule(self.is_divisible, [2])], # here we pass a list containig our params for is_divisible
    }

    self.messages = {
      "order_number.is_divisible": "Order number must be divisible by {divisor}"
    }

  def is_divisible(self, value, params, err_msg_params, **kwargs):
    err_msg_params['divisor'] = params[0] # we populate err_msg_params to customize the message defined above
    return int(value) % params[0] == 0
```

For more details on how to get another field's values, check if nullable etc. see [Processor](#processor).

### 2. Registered rules
Registered rules are rules that can be used with the [default rules syntax](#rules-syntax), just like the ones provided by FlaskVel. The `handlers` for this type of rules must satisfy exactly the same condition as the ones for [Unregistered rules](#1-unregistered-rules)
Although this proccess requires a bit of setup, it is recomended when you want to pass params to an unregistered rule more than one time.

Let's take the example above and register a new rule named `divisible`.

!> Be carefull when choosing a name because you risk overriding the default handler for a rule already defined by FlaskVel with the same name. You can find a full list of rules [here](#rules).

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

> You can override the `handler` of a rule provided by FlaskVel by registering one with the same name and your own `handler` instead, except for [bail](#bail) and [nullable](#nullable), their behaviour **CANNOT** be overridden.

The function `flaskvel.Flaskvel.register_rule` has the following signature:

```python
def register_rule(rule, handler, is_null_tolerant=True)
```
- ***rule*** - the name of the rule to be registered
- ***handler*** - the function implementing the rule
- ***is_null_tolerant*** - whether or not the rule is null tolerant. If the rule is null tolerant and the field is specified as being [nullable](#nullable) and it's value is `None` then the `handler` for this rule is ignored. If you want your rule to be verified no matter what than this parameter should be `False`

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

- Returns one of the following values: `flaskvel.FieldTypes.STRING`, `flaskvel.FieldTypes.NUMERIC`, `flaskvel.FieldTypes.ARRAY`, `flaskvel.FieldTypes.JSON`, `flaskvel.FieldTypes.FILE`, `flaskvel.FieldTypes.UNKOWN`. We recommend you to specify the type of every field ([string](#string), [numeric](#numeric), [array](#array), [json](#json), [file](#file)) otherwise the processor will try to guess it.

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

- Returns either `True` or `False` depending on whether or not the field is [nullable](#nullable).

```python
def should_bail(self, field_name)
```

- Returns either `True` or `False` depending on whether or not the field contains the [bail](#bail) rule.

---

# Rules

## accepted
- The field under validation must be `yes, on, 1, or true`. This is useful for validating "Terms of Service" acceptance.

## active_url
- The field under validation must be active and responds to a request from `requests` Python package.

## after:*date*
- The field under validation must be a value after a given date. The dates will be passed into the `parse` function from [python-dateutil](https://pypi.org/project/python-dateutil/) Python package.

```python
'start_date': ['required', 'date', 'after:2020-07-15']
```

## after_or_equal:*date*
- The field under validation must be a value after or equal to the given date. For more information, see the [after](#afterdate) rule.

## alpha
- The field under validation must be entirely alphabetic characters.

## alpha_dash
- The field under validation may have alpha-numeric characters, as well as dashes and underscores.

## alpha_num
- The field under validation must be entirely alpha-numeric characters.

## array
- The field under validation must be a valid `array` string or a Python `array` object.

## bail
- Stop running validation rules after the first validation failure.

## before:*date*
- The field under validation must be a value preceding the given date. The dates will be passed into the the `parse` function from [python-dateutil](https://pypi.org/project/python-dateutil/) Python package.

## before_or_equal:*date*
- The field under validation must be a value preceding or equal to the given date. The dates will be passed into the `parse` function from [python-dateutil](https://pypi.org/project/python-dateutil/) Python package.

## between:*min, max*
- The field under validation must have a size between the given *min* and *max*. Strings, numerics, arrays, and files are evaluated in the same fashion as the [size](#sizevalue) rule.

## boolean
- The field under validation must be able to be cast as a boolean. Accepted input are `true, false, 1, 0, "1", and "0"`.

## confirmed
- The field under validation must have a matching field of `foo_confirmation`. For example, if the field under validation is `password`, a matching `password_confirmation` field must be present in the input.

## date
- The field under validation must be a valid, non-relative date according to the `parse` function from [python-dateutil](https://pypi.org/project/python-dateutil/) Python package.

## date_equals:*date*
- The field under validation must be equal to the given date. The date will be passed into the `parse` function from [python-dateutil](https://pypi.org/project/python-dateutil/) Python package.

## date_format:*format*
- The field under validation must match the given *format*. You should use either [date](#date) or [date_format](#date_formatformat) when validating a field, not both. This validation rule supports all formats supported by `strptime` function from `datetime` Python package.

```python
"start_date": ["date", "date_format:%d-%m-%Y"]
```

## different:*foo,bar,...*
- The field under validation must have a different value than the given *fields*.

## digits:*value*
- The field under validation must be *numeric* and must have an exact length of *value*.

## digits_between:*min, max*
- The field under validation must be *numeric* and must have a length between the given *min* and *max*.

## dimensions
- The file under validation must be an image meeting the dimension constraints as specified by the rule's parameters:

```python
'avatar': 'dimensions:min_width=100,min_height=200'
```

- Available constraints are: *min_width, max_width, min_height, max_height, width, height, ratio*.

- A ratio constraint should be represented as width divided by height. This can be specified either by a statement like 3/2:

```python
'avatar': 'dimensions:ratio=3/2'
```

## distinct
- When working with arrays, the field under validation must not have any duplicate values. Returns `True` for everything else.

## email
- The field under validation must be formatted as an e-mail address. The regex used is the same as [Django's EmailValidator](https://github.com/django/django/blob/stable/1.3.x/django/core/validators.py#L151).

## ends_with:*foo, bar,...*
- For strings, files and numbers, the field under validation must end with one of the given values. For arrays, the last element must be one of the given values.

## file
- The field under validation must be a successfully uploaded file.

## filled
- The field under validation must not be empty when it is present.

## gt:*field*
- The field under validation must be greater than the given *field*. The two fields must be of the same type. Strings, numerics, arrays, and files are evaluated using the same conventions as the [size](#sizevalue) rule.

## gte:*field*
- The field under validation must be greater than or equal to the given *field*. The two fields must be of the same type. Strings, numerics, arrays, and files are evaluated using the same conventions as the [size](#sizevalue) rule.

## image
- The file under validation must be an image (jpeg, png, bmp, gif, svg, or webp)

## in:*foo, bar,...*
- The field under validation must be included in the given list of values.

## in_array:*another_field*
- The field under validation must exist in *another_field*'s values.

## integer
- The field under validation must be an integer.

## ip
- The field under validation must be an IP address.

## ipv4
- The field under validation must be an IPv4 address. The regex used is the same as [Django's ipv4 validator](https://github.com/django/django/blob/stable/1.3.x/django/core/validators.py#L161).

## ipv6
- The field under validation must be an IPv6 address.

## json
- The field under validation must be a valid JSON string or a Python `dict` object.

## lt:*field*
- The field under validation must be less than the given *field*. The two fields must be of the same type. Strings, numerics, arrays, and files are evaluated using the same conventions as the [size](#sizevalue) rule.

## lte:*field*
- The field under validation must be less than or equal to the given *field*. The two fields must be of the same type. Strings, numerics, arrays, and files are evaluated using the same conventions as the [size](#sizevalue) rule.

## max:*value*
- The field under validation must be less than or equal to a maximum *value*. Strings, numerics, arrays, and files are evaluated in the same fashion as the [size](#sizevalue) rule.

## mimetypes:*text/plain,...*
- The file under validation must match one of the given MIME types:

```python
'video': 'mimetypes:video/avi,video/mpeg,video/quicktime'
```
- The MIME type used for the given file will be provided by the werkzeug.FileStorage module.

## min:*value*
- The field under validation must have a minimum *value*. Strings, numerics, arrays, and files are evaluated in the same fashion as the [size](#sizevalue) rule.

## not_in:*foo,bar,...*
- The field under validation must *not* be included in the given list of values.

## not_in_array:*another_field*
- The field under validation must *not* exist in *another_field*'s values.

## not_regex:*pattern*
- The field under validation must not match the given regular expression.

- **Note**: When using the `regex` / `not_regex` patterns, it may be necessary to specify rules in an array instead of using pipe delimiters, especially if the regular expression contains a pipe character.
  
## nullable
- The field under validation may be `None`. This is particularly useful when validating primitive such as strings and integers that can contain `None` values.

## numeric
- The field under validation must be numeric.

## present
- The field under validation must be present in the input data but can be empty.

## regex:*pattern*
- The field under validation must match the given regular expression.

- **Note**: When using the `regex` / `not_regex` patterns, it may be necessary to specify rules in an array instead of using pipe delimiters, especially if the regular expression contains a pipe character.

## required
- The field under validation must be present in the input data and not empty. A field is considered "empty" if one of the following conditions are true:

    - The value is `None`.
    - The value is an empty string.
    - The value is an empty array.
    - The value is an empty json.

## required_if:*another_field,value1,value2,...*
- The field under validation must be present and not empty *if* the *another_field* field is equal to any *value*.

## required_unless:*another_field,value1,value2,...*
- The field under validation must be present and not empty *unless* the *another_field* field is equal to any *value*.

## required_with:*foo,bar,...*
- The field under validation must be present and not empty *only if any* of the other specified fields are present.

## required_with_all:*foo,bar,...*
- The field under validation must be present and not empty *only when any* of the other specified fields are not present.

## required_without:*foo,bar,...*
- The field under validation must be present and not empty *only when all* of the other specified fields are not present.

## required_without_all:*foo,bar,...*
- The field under validation must be present and not empty *only when all* of the other specified fields are not present.

## same:*foo,bar,..*
- All of the given *fields* must match the field under validation.

## size:*value*
- The field under validation must have a size matching the given *value*. For string data, *value* corresponds to the number of characters. For numeric data, value corresponds to a given integer/float *value* (the attribute must also have the [numeric](#numeric) or [integer](#integer) rule). For an array, size corresponds to the count of the array. For a json, *value* must be equal to the number of keys. For files, *size* corresponds to the file size in kilobytes.

```python
# Validate that a string is exactly 12 characters long...
'title': 'size:12'

# Validate that a provided integer equals 10...
'seats': 'integer|size:10'

# Validate that an array has exactly 5 elements...
'tags': 'array|size:5'

# Validte that a json has exaclty 2 keys...
'login_credentials': 'json|size:2'

# Validate that an uploaded file is exactly 512 kilobytes...
'image': 'file|size:512'
```

## starts_with:*foo,bar,...*
- For strings, files and numbers, the field under validation must start with one of the given values. For arrays, the first element must be one of the given values.

## string
- The field under validation must be a string. If you would like to allow the field to also be `None`, you should assign the [nullable](#nullable) rule to the field.

## timezone
- The field under validation must be a valid timezone identifier according to the `pytz` Python package.

## url
- The field under validation must be a valid URL. The regex used is the same as [Django's UrlValidator](https://github.com/django/django/blob/stable/1.3.x/django/core/validators.py#L45).

## uuid
- The field under validation must be a valid RFC 4122 (version 1, 3, 4, or 5) universally unique identifier (UUID).

---

# Contributions
Any form of contribution is welcome!











