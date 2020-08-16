

class ParsedRule():
	def __init__(self, predicate, params=[]):
		self._predicate = predicate
		self._params = params

	def __str__(self):
		self.__repr__()

	def __repr__(self):
		return str({
			'predicate': self._predicate,
			'params': self._params
		})

	def __eq__(self, other):
		if isinstance(other, str) or callable(other): # when using: 'rule' in [...]
			return self._predicate == other
		if isinstance(other, ParsedRule):
			return self._predicate == other._predicate and self._params == other._params
		return False

	def get_predicate(self):
		return self._predicate

	def get_params(self):
		return self._params

	def has_unregistered_handler(self):
		return callable(self._predicate)