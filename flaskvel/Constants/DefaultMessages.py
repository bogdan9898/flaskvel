from .FieldTypes import FieldTypes

DefaultMessages = {
	'accepted': 'The {field_name} field must be accepted.',
    'active_url': 'The {field_name} field is not a valid URL.',
    'after': 'The {field_name} field must be a date after {0}.',
    'after_or_equal': 'The {field_name} field must be a date after or equal to {0}.',
    'alpha': 'The {field_name} field may only contain letters.',
    'alpha_dash': 'The {field_name} field may only contain letters, numbers, dashes and underscores.',
    'alpha_num': 'The {field_name} field may only contain letters and numbers.',
    'array': 'The {field_name} field must be an array.',
    'before': 'The {field_name} field must be a date before {0}.',
    'before_or_equal': 'The {field_name} field must be a date before or equal to {0}.',
    'between': {
        FieldTypes.NUMERIC: 'The {field_name} field must have values between {0} and {1}.',
        FieldTypes.FILE: 'The {field_name} field must be between {0} and {1} kilobytes.',
        FieldTypes.STRING: 'The {field_name} field must have between {0} and {1} characters.',
        FieldTypes.ARRAY: 'The {field_name} field must have between {0} and {1} items.',
        FieldTypes.JSON: 'The {field_name} field must have between {0} and {1} keys.',
    },
    'boolean': 'The {field_name} field must be true or false.',
    'confirmed': 'The {field_name} field confirmation does not match.',
    'date': 'The {field_name} field is not a valid date.',
    'date_equals': 'The {field_name} field must be a date equal to {0}.',
    'date_format': 'The {field_name} field does not match the format {0}.',
    'different': 'The {field_name} field and {all_fields} fields must be different.',
    'digits': 'The {field_name} field must be {0} digits.',
    'digits_between': 'The {field_name} field must be between {0} and {1} digits.',
    'dimensions': 'The {field_name} field must have the following dimensions restrictinos: {all_params}',
    'distinct': 'The {field_name} field has a duplicate value.',
    'email': 'The {field_name} field must be a valid email address.',
    'ends_with': 'The {field_name} field must end with one of the following: {all_params}',
    'file': 'The {field_name} field must be a file.',
    'filled': 'The {field_name} field must have a value.',
    'gt': {
        FieldTypes.NUMERIC: 'The {field_name} field must be greater than {0} field.',
        FieldTypes.FILE: 'The {field_name} file must have more kBs than {0} file.',
        FieldTypes.STRING: 'The {field_name} field must have more characters than {0} field.',
        FieldTypes.ARRAY: 'The {field_name} field must have more items than {0} field.',
        FieldTypes.JSON: 'The {field_name} field must have more keys than {0} field.',
    },
    'gte': {
        FieldTypes.NUMERIC: 'The {field_name} field must be greater than or equal to {0} field.',
        FieldTypes.FILE: 'The {field_name} file must have at least the same number of kBs as {0} file.',
        FieldTypes.STRING: 'The {field_name} field must have at least the same number of characters as {0} field.',
        FieldTypes.ARRAY: 'The {field_name} field must have at least the same number of items as {0} field.',
        FieldTypes.JSON: 'The {field_name} field must have at least the same number of keys as {0} field.',
    },
    'image': 'The {field_name} field must be an image.',
    'in': 'The {field_name} field does not exist in {all_params}.',
    'in_array': 'The {field_name} field does not exist in {0}\'s values.',
    'integer': 'The {field_name} field must be an integer.',
    'ip': 'The {field_name} field must be a valid IP address.',
    'ipv4': 'The {field_name} field must be a valid IPv4 address.',
    'ipv6': 'The {field_name} field must be a valid IPv6 address.',
    'json': 'The {field_name} field must be a valid JSON.',
    'lt': {
        FieldTypes.NUMERIC: 'The {field_name} field must be lower than {0} field.',
        FieldTypes.FILE: 'The {field_name} file must have fewer kBs than {0} file.',
        FieldTypes.STRING: 'The {field_name} field must have less characters than {0} field.',
        FieldTypes.ARRAY: 'The {field_name} field must have less items than {0} field.',
        FieldTypes.JSON: 'The {field_name} field must have less keys than {0} field.',
    },
    'lte': {
        FieldTypes.NUMERIC: 'The {field_name} field must lower than or equal to {0} field.',
        FieldTypes.FILE: 'The {field_name} file must have at most the same number of kBs as {0} file.',
        FieldTypes.STRING: 'The {field_name} field must have at most the same number of characters as {0} field.',
        FieldTypes.ARRAY: 'The {field_name} field must have at most the same number of items as {0} field.',
        FieldTypes.JSON: 'The {field_name} field must have at most the same number of keys as {0} field.',
    },
    'max': {
        FieldTypes.NUMERIC: 'The {field_name} field must be lower than {0}.',
        FieldTypes.FILE: 'The {field_name} file must be smaller than {0} kBs.',
        FieldTypes.STRING: 'The {field_name} field must have less than {0} characters.',
        FieldTypes.ARRAY: 'The {field_name} field must have less than {0} items.',
        FieldTypes.JSON: 'The {field_name} field must have less than {0} keys.',
    },
    'mimetypes': 'The {field_name} field must be a file of type: {0}.',
    'min': {
        FieldTypes.NUMERIC: 'The {field_name} field must be greater than {0}.',
        FieldTypes.FILE: 'The {field_name} file must be bigger than {0} kBs.',
        FieldTypes.STRING: 'The {field_name} field must have more than {0} characters.',
        FieldTypes.ARRAY: 'The {field_name} field must have more than {0} items.',
        FieldTypes.JSON: 'The {field_name} field must have more than {0} keys.',
    },
    'not_in': 'The {field_name} field must not exist in {all_params}.',
    'not_in_array': 'The {field_name} field must not exist in {0}\'s values.',
    'not_regex': 'The {field_name} field is invalid.',
    'numeric': 'The {field_name} field must be a number.',
    'present': 'The {field_name} field must be present.',
    'regex': 'The {field_name} field is invalid.',
    'required': 'The {field_name} field is required.',
    'required_if': 'The {field_name} field is required when {0} field is one of {the_rest_of_params}.',
    'required_unless': 'The {field_name} field is required unless {0} field is one of the values {the_rest_of_params}.',
    'required_with': 'The {field_name} field is required when any of the fields {all_params} is present.',
    'required_with_all': 'The {field_name} field is required when all of the fields {all_params} are present.',
    'required_without': 'The {field_name} field is required when any of the fields {all_params} is not present.',
    'required_without_all': 'The {field_name} field is required when none of the fields {all_params} are present.',
    'same': 'The {field_name} field and {all_params} fields must match.',
    'size': {
        FieldTypes.NUMERIC: 'The {field_name} field must be equal to {0}.',
        FieldTypes.FILE: 'The {field_name} file must be {0} kBs.',
        FieldTypes.STRING: 'The {field_name} field must have {0} characters.',
        FieldTypes.ARRAY: 'The {field_name} field must have {0} items.',
        FieldTypes.JSON: 'The {field_name} field must have {0} keys.',
    },
    'starts_with': 'The {field_name} field must start with one of the following: {all_params}',
    'string': 'The {field_name} field must be a string.',
    'timezone': 'The {field_name} field must be a valid zone.',
    'url': 'The {field_name} field must be a valid URL.',
    'uuid': 'The {field_name} field must be a valid UUID.',

}

