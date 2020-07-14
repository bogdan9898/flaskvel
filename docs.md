
# Flaskvel

## Rules
---
### accepted
- The field under validation must be `yes, on, 1, or true`. This is useful for validating "Terms of Service" acceptance.

### active_url
- The field under validation must be active and responds to a request from `requests` Python package.

### after:*date*
- The field under validation must be a value after a given date. The dates will be passed into the `parse` function from [python-dateutil](https://pypi.org/project/python-dateutil/) Python package.
```python
'start_date': ['required', 'date', 'after:2020-07-15']
```

### after_or_equal:*date*
- The field under validation must be a value after or equal to the given date. For more information, see the [after](#afterdate) rule.

### alpha
- The field under validation must be entirely alphabetic characters.

### alpha_dash
- The field under validation may have alpha-numeric characters, as well as dashes and underscores.

### alpha_num
- The field under validation must be entirely alpha-numeric characters.

### array
- The field under validation must be an `array` string or a Python `array` object.

### bail
- Stop running validation rules after the first validation failure.

### before:*date*
- The field under validation must be a value preceding the given date. The dates will be passed into the the `parse` function from [python-dateutil](https://pypi.org/project/python-dateutil/) Python package.

### before_or_equal:*date*
- The field under validation must be a value preceding or equal to the given date. The dates will be passed into the `parse` function from [python-dateutil](https://pypi.org/project/python-dateutil/) Python package.

### between:*min, max*
- The field under validation must have a size between the given *min* and *max*. Strings, numerics, arrays, and files are evaluated in the same fashion as the [size](#size) rule.

### boolean
- The field under validation must be able to be cast as a boolean. Accepted input are `true, false, 1, 0, "1", and "0"`.

### confirmed
- The field under validation must have a matching field of `foo_confirmation`. For example, if the field under validation is `password`, a matching `password_confirmation` field must be present in the input.

### date
- The field under validation must be a valid, non-relative date according to the `parse` function from [python-dateutil](https://pypi.org/project/python-dateutil/) Python package.

### date_equals:*date*
- The field under validation must be equal to the given date. The date will be passed into the `parse` function from [python-dateutil](https://pypi.org/project/python-dateutil/) Python package.

### date_format:*format*
- The field under validation must match the given *format*. You should use either date or date_format when validating a field, not both. This validation rule supports all formats supported by ______.

### different:*field*
- The field under validation must have a different value than *field*.

### digits:*value*
- The field under validation must be *numeric* and must have an exact length of *value*.

### digits_between:*min, max*
- The field under validation must have a length between the given *min* and *max*.

### dimensions:*WidthxHeight*
The file under validation must be an image meeting the dimension constraints specified as `WidthxHeight`
```python
'avatar': ['dimensions:200x200']
```

### distinct
- When working with arrays, the field under validation must not have any duplicate values.

### email
- The field under validation must be formatted as an e-mail address.

### ends_with:*foo, bar,...*
- The field under validation must end with one of the given values.

### file
- The field under validation must be a successfully uploaded file.

### filled
- The field under validation must not be empty when it is present.

### gt:*field*
- The field under validation must be greater than the given *field*. The two fields must be of the same type. Strings, numerics, arrays, and files are evaluated using the same conventions as the [size](#size) rule.

### gte
- The field under validation must be greater than or equal to the given *field*. The two fields must be of the same type. Strings, numerics, arrays, and files are evaluated using the same conventions as the [size](#size) rule.

### image
- The file under validation must be an image (jpeg, png, bmp, gif, svg, or webp)

### in

### in_array

### integer

### ip

### ipv4

### ipv6

### json

### lt

### lte

### max

### mimetypes

### min

### not_in

### not_regex

### nullable

### numeric

### present

### regex

### required

### required_if

### required_unless

### required_with

### required_with_all

### required_without

### required_without_all

### same

### size

### starts_with

### string

### timezone

### url

### uuid