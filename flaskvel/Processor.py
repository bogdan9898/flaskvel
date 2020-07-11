import re
from dateutil.parser import parse as parse_date
from flask import request

from .Constants.RulesPredicates import RulesPredicates
from .Constants.DefaultMessages import DefaultMessages

class Processor():
	def __init__(self, validator):
		self._parsed_rules = validator.get_parsed_rules()
		self._errors = {} # error messages already formated
		self._failed_validations = {} # info about failed validations
		self._registered_handlers = validator.get_registered_handlers()
		self._messages = validator.get_messages()

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
			nullable = self.is_field_nullable(rules)
			bail = self.should_bail(rules)

			for parsed_rule in rules:
				rule_predicate = parsed_rule.get_predicate()
				params = parsed_rule.get_params()
				if rule_predicate in ignored_predicates:
					continue
				
				handler = None
				if parsed_rule.has_unregistered_handler():
					handler = rule_predicate
					rule_predicate = rule_predicate.__name__
				else:
					handler = self.get_rule_handler(rule_predicate)

				if not handler(field_name=field_name, value=field_value, params=params, nullable=nullable):
					validation_passed = False

					failed_validations[rule_predicate] = params
					if bail:
						self._failed_validations[field_name] = failed_validations
						return validation_passed
			if len(failed_validations) > 0:
				self._failed_validations[field_name] = failed_validations
				self._errors[field_name] = self.generate_errors(field_name)
		return validation_passed

	def get_field_value(self, field_name):
		if request.is_json:
			return request.json.get(field_name)
		else:
			return request.form.get(field_name)

	def is_field_nullable(self, rules):
		imply_nullable = [
			RulesPredicates.NULLABLE,
			RulesPredicates.REQUIRED_IF,
			RulesPredicates.REQUIRED_UNLESS,
			RulesPredicates.REQUIRED_WITH,
			RulesPredicates.REQUIRED_WITH_ALL,
			RulesPredicates.REQUIRED_WITHOUT,
			RulesPredicates.REQUIRED_WITHOUT_ALL
		]
		for rule in imply_nullable:
			if rule in rules:
				return True
		return False

	def should_bail(self, rules):
		return RulesPredicates.BAIL in rules

	def generate_errors(self, field_name):
		errors_strings = []
		for rule_predicates, params in self._failed_validations[field_name].items():
			message = (self._messages.get('{0}:{1}'.format(field_name, rule_predicates)) or
					DefaultMessages.get(rule_predicates))

			if not message:
				errors_strings.append('Validation failed for: ' + str(rule_predicates))
			else:
				errors_strings.append(message.format(*params, field_name=field_name, all_params=params))

		return errors_strings

	def assert_params_len(self, params, required_size, rule_predicate):
		if len(params) < required_size:
			raise Exception('Rule <{0}> requires at least {1} parameter'.format(rule_predicate, required_size))

	def get_rule_handler(self, rule_predicate):
		# todo: !!first!! check if handler is in custom_handlers, so an user can override default handlers for default RulesPredicates
		# if rule_predicate in self._registered_handlers:
			# return self._registered_handlers.find(rule_predicate)
		handler = 'handler_' + rule_predicate
		if not hasattr(self, handler):
			raise Exception('No handler found for rule <{0}>'.format(rule_predicate))
		return getattr(self, handler)

	def handler_accepted(self, **kwargs):
		return kwargs['value'] in ['yes', 1, '1', 'on', True, 'true']

	def handler_active_url(self, **kwargs):
		pass

	def handler_after(self, **kwargs):
		self.assert_params_len(kwargs['params'], 1, 'after')
		try:
			return parse_date(kwargs['value']) > parse_date(kwargs['params'][0])
		except Exception:
			return False

	def handler_after_or_equal(self, **kwargs):
		self.assert_params_len(kwargs['params'], 1, 'after_or_equal')
		try:
			return parse_date(kwargs['value']) >= parse_date(kwargs['params'][0])
		except Exception:
			return False

	def handler_alpha(self, **kwargs):
		pass

	def handler_alpha_dash(self, **kwargs):
		pass

	def handler_alpha_num(self, **kwargs):
		pass

	def handler_array(self, **kwargs):
		pass

	def handler_before(self, **kwargs):
		self.assert_params_len(kwargs['params'], 1, 'before')
		try:
			return parse_date(kwargs['value']) < parse_date(kwargs['params'][0])
		except Exception:
			return False

	def handler_before_or_equal(self, **kwargs):
		self.assert_params_len(kwargs['params'], 1, 'before_or_equal')
		try:
			return parse_date(kwargs['value']) <= parse_date(kwargs['params'][0])
		except Exception:
			return False

	def handler_between(self, **kwargs):
		pass

	def handler_boolean(self, **kwargs):
		pass

	def handler_confirmed(self, **kwargs):
		pass

	def handler_date(self, **kwargs):
		pass

	def handler_date_equals(self, **kwargs):
		pass

	def handler_date_format(self, **kwargs):
		pass

	def handler_diferent(self, **kwargs):
		pass

	def handler_digits(self, **kwargs):
		pass

	def handler_digits_between(self, **kwargs):
		pass

	def handler_dimensions(self, **kwargs):
		pass

	def handler_distinct(self, **kwargs):
		pass

	def handler_email(self, **kwargs):
		pattern = re.compile("^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$", re.IGNORECASE)
		return pattern.match(str(kwargs['value'])) is not None

	def handler_ends_with(self, **kwargs):
		pass

	def handler_file(self, **kwargs):
		pass

	def handler_filled(self, **kwargs):
		pass

	def handler_gt(self, **kwargs):
		pass

	def handler_gte(self, **kwargs):
		pass

	def handler_image(self, **kwargs):
		pass

	def handler_in(self, **kwargs):
		pass

	def handler_in_array(self, **kwargs):
		pass

	def handler_integer(self, **kwargs):
		pass

	def handler_ip(self, **kwargs):
		pass

	def handler_ipv4(self, **kwargs):
		pass

	def handler_ipv6(self, **kwargs):
		pass

	def handler_json(self, **kwargs):
		pass

	def handler_lt(self, **kwargs):
		pass

	def handler_lte(self, **kwargs):
		pass

	def handler_max(self, **kwargs):
		pass

	def handler_mimetypes(self, **kwargs):
		pass

	def handler_min(self, **kwargs):
		pass

	def handler_not_int(self, **kwargs):
		pass

	def handler_not_regex(self, **kwargs):
		pass

	def handler_numeric(self, **kwargs):
		pass

	def handler_password(self, **kwargs):
		pass

	def handler_present(self, **kwargs):
		pass

	def handler_regex(self, **kwargs):
		pass

	def handler_required(self, **kwargs):
		return kwargs['value'] != None

	def handler_required_if(self, **kwargs):
		pass

	def handler_required_unless(self, **kwargs):
		pass

	def handler_required_with(self, **kwargs):
		pass

	def handler_required_with(self, **kwargs):
		pass

	def handler_required_with_all(self, **kwargs):
		pass

	def handler_required_without(self, **kwargs):
		pass

	def handler_required_without_all(self, **kwargs):
		pass

	def handler_same(self, **kwargs):
		pass

	def handler_size(self, **kwargs):
		pass

	def handler_starts_with(self, **kwargs):
		pass

	def handler_string(self, **kwargs):
		return isinstance(kwargs['value'], str)

	def handler_timezone(self, **kwargs):
		pass

	def handler_url(self, **kwargs):
		pass

	def handler_uuid(self, **kwargs):
		pass
