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

!> When using the `regex` / `not_regex` patterns, it may be necessary to specify rules in an array instead of using pipe delimiters, especially if the regular expression contains a pipe character.

## nullable
- The field under validation may be `None`. This is particularly useful when validating primitive such as strings and integers that can contain `None` values.

## numeric
- The field under validation must be numeric.

## present
- The field under validation must be present in the input data but can be empty.

## regex:*pattern*
- The field under validation must match the given regular expression.

!> When using the `regex` / `not_regex` patterns, it may be necessary to specify rules in an array instead of using pipe delimiters, especially if the regular expression contains a pipe character.

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
- The field under validation must be present and not empty *only if any* of the other specified fields is present.

## required_with_all:*foo,bar,...*
- The field under validation must be present and not empty *only when all* of the other specified fields are present.

## required_without:*foo,bar,...*
- The field under validation must be present and not empty *only when any* of the other specified fields is not present.

## required_without_all:*foo,bar,...*
- The field under validation must be present and not empty *only when all* of the other specified fields are not present.

## same:*foo,bar,..*
- All of the given *fields* must match the field under validation.

## size:*value*
- The field under validation must have a size matching the given *value*. For string data, *value* corresponds to the number of characters. For numeric data, value corresponds to a given integer/float *value* (the attribute must also have the [numeric](#numeric) or [integer](#integer) rule). For an array, size corresponds to the count of the array. For a json, *value* must be equal to the number of keys. For files, *size* corresponds to the file size in kilobytes.

```python
# Validate that a string is exactly 12 characters long...
'title': 'string|size:12'

# Validate that an integer equals 10...
'seats': 'integer|size:10'

# Validate that an array has exactly 5 elements...
'tags': 'array|size:5'

# Validate that a json has exaclty 2 keys...
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
