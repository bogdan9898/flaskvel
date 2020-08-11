from flaskvel import Validator, Rules

class SizeValidator(Validator):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.rules = {
			'other_string': [ Rules.STRING, 'required' ],
			'other_numeric': [ Rules.NUMERIC, 'required' ],
			'other_array': [ Rules.ARRAY, 'required' ],
			'other_json': [ Rules.JSON, 'required' ],
			# 'other_file': [ 'required' ],

			'gt_string': [ 'gt:other_string' ],
			'gt_numeric': ['gt:other_numeric'],
			'gt_array': [ 'gt:other_array' ],
			'gt_json': [ 'gt:other_json' ],
			# 'gt_file': [ 'gt:other_file' ],

			'gte_string': [ 'gte:other_string' ],
			'gte_numeric': ['gte:other_numeric'],
			'gte_array': [ 'gte:other_array' ],
			'gte_json': [ 'gte:other_json' ],
			# 'gte_file': [ 'gte:other_file' ],

			'lt_string': [ 'lt:other_string' ],
			'lt_numeric': ['lt:other_numeric'],
			'lt_array': [ 'lt:other_array' ],
			'lt_json': [ 'lt:other_json' ],
			# 'lt_file': [ 'lt:other_file' ],

			'lte_string': [ 'lte:other_string' ],
			'lte_numeric': ['lte:other_numeric'],
			'lte_array': [ 'lte:other_array' ],
			'lte_json': [ 'lte:other_json' ],
			# 'lte_file': [ 'lte:other_file' ],

			'size_string': [ 'size:2' ],
			'size_numeric': ['size:2'],
			'size_array': [ 'size:2' ],
			'size_json': [ 'size:2' ],
			# 'size_file': [ 'size:2' ],

			'max_string': [ 'max:2' ],
			'max_numeric': ['max:2'],
			'max_array': [ 'max:2' ],
			'max_json': [ 'max:2' ],
			# 'max_file': [ 'max:2' ],

			'min_string': [ 'min:2' ],
			'min_numeric': ['min:2'],
			'min_array': [ 'min:2' ],
			'min_json': [ 'min:2' ],
			# 'min_file': [ 'min:2' ],

			'between_string': [ 'between:1,3' ],
			'between_numeric': ['between:1,3'],
			'between_array': [ 'between:1,3' ],
			'between_json': [ 'between:1,3' ],
			# 'between_file': [ 'between:1,3' ],

			# 'dimensions_image': ["dimensions:ratio=3/2"],

			'registered_rule': ['nullable', 'my_new_custom_rule:a,b,c'],
		}

		self.messages = {
			'registered_rule.my_new_custom_rule': 'What a failure...'
		}
