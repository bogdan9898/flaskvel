import re
from dateutil.parser import parse as parse_date
from flask import request
from werkzeug.datastructures import FileStorage # comes packaged with flask

from .Constants.RulesPredicates import RulesPredicates
from .Constants.DefaultMessages import DefaultMessages
from .Constants.FieldTypes import FieldTypes

class Processor():
	null_intolerant_rules = [ # todo: move this into Flaskvel class with regitered_handlers 
		RulesPredicates.REQUIRED,
		RulesPredicates.REQUIRED_IF,
		RulesPredicates.REQUIRED_UNLESS,
		RulesPredicates.REQUIRED_WITH,
		RulesPredicates.REQUIRED_WITH_ALL,
		RulesPredicates.REQUIRED_WITHOUT,
		RulesPredicates.REQUIRED_WITHOUT_ALL,
		RulesPredicates.PRESENT
	]

	def __init__(self, validator):
		self._validator = validator
		self._errors = {} # error messages already formated
		self._failed_validations = {} # info about failed validations
		self._parsed_rules = None
		self._registered_handlers = None
		self._messages = None

	def get_errors(self):
		return self._errors

	def get_failed_validations(self):
		return self._failed_validations

	def run(self):
		# update critical data
		if self._messages is None:
			self._messages = self._validator.get_messages()
		if self._parsed_rules is None:
			self._parsed_rules = self._validator.get_parsed_rules()
		if self._registered_handlers is None:
			self._registered_handlers = self._validator.get_registered_handlers()

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
				if ((rule_predicate in ignored_predicates) or
					(nullable and field_value is None and not rule_predicate in Processor.null_intolerant_rules)):
					continue
				
				handler = None
				if parsed_rule.has_unregistered_handler():
					handler = rule_predicate
					rule_predicate = rule_predicate.__name__
				else:
					handler = self.get_rule_handler(rule_predicate)

				err_msg_params = {}
				if not handler(field_name=field_name, value=field_value, params=params, nullable=nullable, bail=bail, err_msg_params=err_msg_params, processor=self):
					validation_passed = False
					failed_validations[rule_predicate] = [params, err_msg_params]
					if bail:
						self._failed_validations[field_name] = failed_validations
						self._errors[field_name] = self.generate_errors(field_name)
						return validation_passed

			if len(failed_validations) > 0:
				self._failed_validations[field_name] = failed_validations
				self._errors[field_name] = self.generate_errors(field_name)

			# DELETE ME!
			field_type = self.get_field_type(field_name)
			print("{0} -> {1} / {2}".format(field_name, field_type, type(self.get_field_value(field_name))))
			# DELETE ME!
		return validation_passed

	def get_field_type(self, field_name):
		rules = self._parsed_rules[field_name]
		types_requirements = {
			FieldTypes.NUMERIC: ['integer', 'numeric'],
			FieldTypes.FILE: ['file', 'image', 'dimensions'],
			FieldTypes.STRING: ['string', 'alpha', 'alpha_dash'],
			FieldTypes.ARRAY: ['array'],
		}
		for field_type, requirements in types_requirements.items():
			for requirement in requirements:
				if requirement in rules:
					return field_type

		field_value = self.get_field_value(field_name)
		if isinstance(field_value, int) or isinstance(field_value, float):
			return FieldTypes.NUMERIC

		if isinstance(field_value, str):
			return FieldTypes.STRING

		if isinstance(field_value, list):
			return FieldTypes.ARRAY

		if isinstance(field_value, FileStorage):
			return FieldTypes.FILE

		return FieldTypes.UNKOWN

	def get_field_value(self, field_name):
		if field_name in request.files:
			return request.files.get(field_name)

		result = request.json if request.is_json else request.form
		keys = field_name.split('.')
		for key in keys:
			result = result.get(key)
			if not result:
				return None
		return result

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
		comparison_messages = ['between', 'gt', 'gte', 'lt', 'lte', 'max', 'min', 'size']
		errors_strings = []
		field_type = self.get_field_type(field_name)
		for rule_predicate, params in self._failed_validations[field_name].items():
			params, err_msg_params = params
			message = self._messages.get('{0}.{1}'.format(field_name, rule_predicate))

			if not message:
				message = DefaultMessages.get(rule_predicate)
				if message and (rule_predicate in comparison_messages):
					message = message.get(field_type)

			if not message:
				errors_strings.append('Validation failed for: ' + str(rule_predicate))
			else:
				errors_strings.append(message.format(*params, field_name=field_name, **err_msg_params))

		return errors_strings

	def assert_params_count(self, params, required_size, rule_predicate):
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
		self.assert_params_count(kwargs['params'], 1, RulesPredicates.AFTER)
		try:
			return parse_date(kwargs['value']) > parse_date(kwargs['params'][0])
		except:
			return False 

	def handler_after_or_equal(self, **kwargs):
		self.assert_params_count(kwargs['params'], 1, RulesPredicates.AFTER_OR_EQUAL)
		try:
			return parse_date(kwargs['value']) >= parse_date(kwargs['params'][0])
		except:
			return False

	def handler_alpha(self, **kwargs):
		patern = re.compile("^[a-z\s]*$", re.IGNORECASE)
		try:
			return patern.match(kwargs['value'])
		except:
			return False

	def handler_alpha_dash(self, **kwargs):
		patern = re.compile("^[a-z\-_\s]*$", re.IGNORECASE)
		try:
			return patern.match(kwargs['value'])
		except:
			return False

	def handler_alpha_num(self, **kwargs):
		patern = re.compile("^[a-z0-9\s]*$", re.IGNORECASE)
		try:
			return patern.match(kwargs['value'])
		except:
			return False

	def handler_array(self, **kwargs):
		# todo: validate strings that match [.+(,\w+)*]
		return isinstance(kwargs['value'], list)

	def handler_before(self, **kwargs):
		self.assert_params_count(kwargs['params'], 1, RulesPredicates.BEFORE)
		try:
			return parse_date(kwargs['value']) < parse_date(kwargs['params'][0])
		except:
			return False

	def handler_before_or_equal(self, **kwargs):
		self.assert_params_count(kwargs['params'], 1, RulesPredicates.BEFORE_OR_EQUAL)
		try:
			return parse_date(kwargs['value']) <= parse_date(kwargs['params'][0])
		except:
			return False

	def handler_between(self, **kwargs):
		pass

	def handler_boolean(self, **kwargs):
		return kwargs['value'] in [1, 0, '1', '0', True, False]

	def handler_confirmed(self, **kwargs):
		return kwargs['value'] == self.get_field_value("{0}_confirmed".format(kwargs['field_name']))

	def handler_date(self, **kwargs):
		try:
			return parse_date(kwargs['value'])
		except:
			return False

	def handler_date_equals(self, **kwargs):
		pass

	def handler_date_format(self, **kwargs):
		pass

	def handler_different(self, **kwargs):
		# todo: support more than one field (like same rule)
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
		try:
			return pattern.match(kwargs['value']) is not None
		except:
			return False

	def handler_ends_with(self, **kwargs):
		params = kwargs['params']
		kwargs['err_msg_params']['all_params'] = params
		pass

	def handler_file(self, **kwargs):
		return isinstance(kwargs['value'], FileStorage)

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
		try:
			int(kwargs['value'])
			return True
		except:
			return False

	def handler_ip(self, **kwargs):
		pass

	def handler_ipv4(self, **kwargs):
		pass

	def handler_ipv6(self, **kwargs):
		pass

	def handler_json(self, **kwargs):
		return isinstance(kwargs['value'], dict)

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
		try:
			float(kwargs['value'])
			return True
		except:
			return False

	def handler_present(self, **kwargs):
		field_name = kwargs['field_name']
		if field_name in request.files:
			return True

		result = request.json if request.is_json else request.form
		keys = field_name.split('.')
		for key in keys:
			if key not in result:
				return False
			result = result[key]
		return True

	def handler_regex(self, **kwargs):
		pass

	def handler_required(self, **kwargs):
		return kwargs['value'] != None

	def handler_required_if(self, **kwargs):
		params = kwargs['params']
		kwargs['err_msg_params']['the_rest_of_params'] = params[1:]
		other_value = self.get_field_value(params[0])
		# if not other_value in params[1:]:
		# 	return True
		# else:
		# 	return kwargs['value'] is not None
		return not other_value in params[1:] or kwargs['value'] is not None

	def handler_required_unless(self, **kwargs):
		params = kwargs['params']
		kwargs['err_msg_params']['the_rest_of_params'] = params[1:]
		other_value = self.get_field_value(params[0])
		# if other_value in params[1:]:
		# 	return True
		# else:
		# 	return kwargs['value'] is not None
		return other_value in params[1:] or kwargs['value'] is not None

	def handler_required_with(self, **kwargs):
		params = kwargs['params']
		kwargs['err_msg_params']['all_params'] = params
		for field in params:
			if self.get_field_value(field) is not None:
				return kwargs['value'] is not None
		return True

	def handler_required_with_all(self, **kwargs):
		params = kwargs['params']
		kwargs['err_msg_params']['all_params'] = params
		for field in params:
			if self.get_field_value(field) is None:
				return True
		return kwargs['value'] is not None

	def handler_required_without(self, **kwargs):
		params = kwargs['params']
		kwargs['err_msg_params']['all_params'] = params
		for field in params:
			if self.get_field_value(field) is None:
				return kwargs['value'] is not None
		return True

	def handler_required_without_all(self, **kwargs):
		params = kwargs['params']
		kwargs['err_msg_params']['all_params'] = params
		for field in params:
			if self.get_field_value(field) is not None:
				return True
		return kwargs['value'] is not None

	def handler_same(self, **kwargs):
		value = kwargs['value']
		params = kwargs['params']
		kwargs['err_msg_params']['all_params'] = params
		for param in params:
			other_value = self.get_field_value(param)
			if not value == other_value:
				return False
		return True

	def handler_size(self, **kwargs):
		pass

	def handler_starts_with(self, **kwargs):
		params = kwargs['params']
		kwargs['err_msg_params']['all_params'] = params
		pass

	def handler_string(self, **kwargs):
		return isinstance(kwargs['value'], str)

	def handler_timezone(self, **kwargs):
		pass

	def handler_url(self, **kwargs):
		pass

	def handler_uuid(self, **kwargs):
		pass
