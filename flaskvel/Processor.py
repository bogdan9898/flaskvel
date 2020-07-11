from flask import request

from .Constants.RulesPredicates import RulesPredicates
from .Constants.DefaultMessages import DefaultMessages

class Processor():
	def __init__(self, validator):
		self._parsed_rules = validator.get_parsed_rules()
		self._errors = {} # error messages already formated
		self._failed_validations = {} # info about failed validations
		self._registered_handlers = validator.get_registered_handlers()

	def get_errors(self):
		return self._errors

	def get_failed_validations(self):
		return self._failed_validations

	def run(self):
		ignored_predicates = [RulesPredicates.NULLABLE, RulesPredicates.BAIL]

		validation_passed = True
		for field_name, rules in self._parsed_rules.items():
			failed_validations = {}

			field_value = self.get_field_value(field_name)
			nullable = self.is_field_nullable(field_name, rules)
			bail = self.should_bail(field_name, rules)

			for parsed_rule in rules:
				rule_predicate = parsed_rule.get_predicate()
				params = parsed_rule.get_params()
				if rule_predicate in ignored_predicates:
					continue
				
				handler = None
				if parsed_rule.has_unregistered_handler():
					handler = rule_predicate
				else:
					handler = self.get_rule_handler(rule_predicate)

				if not handler(value=field_value, params=params, nullable=nullable):
					validation_passed = False
					failed_validations[rule_predicate] = params
					if bail:
						self._failed_validations[field_name] = failed_validations
						return validation_passed
			if len(failed_validations) > 0:
				self._failed_validations[field_name] = failed_validations
				# todo: generate errors
				self._errors[field_name] = [ 'error1', 'error2', 'error3...' ]
		return validation_passed

	def get_field_value(self, field_name):
		if request.is_json:
			return request.json.get(field_name)
		else:
			return request.form.get(field_name)

	def is_field_nullable(self, field_name, rules):
		return RulesPredicates.NULLABLE in rules

	def should_bail(self, field_name, rules):
		return RulesPredicates.BAIL in rules

	def get_rule_handler(self, rule_predicate):
		# todo: !!first!! check if handler is in custom_handlers, so an user can override default handlers for default RulesPredicates
		# if rule_predicate in self._registered_handlers:
			# return self._registered_handlers.find(rule_predicate)
		handler = 'handler_' + rule_predicate
		if not hasattr(self, handler):
			raise Exception('No handler found for: {0}'.format(rule_predicate))
		return getattr(self, handler)

	def handler_required(self, **kwargs):
		return kwargs['value'] != None

	def handler_email(self, **kwargs):
		return True

	def handler_eq(self, **kwargs):
		return False

	# todo: finish all handle_fct