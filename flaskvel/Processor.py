import re
import ast
import json
from copy import deepcopy
import pytz
import requests
import os
import operator
from dateutil.parser import parse as parse_date
from datetime import datetime
from flask import request
from werkzeug.datastructures import FileStorage # comes packaged with flask
from PIL import Image

from .Constants.RulesPredicates import RulesPredicates
from .Constants.DefaultMessages import DefaultMessages
from .Constants.FieldTypes import FieldTypes
from .Flaskvel import Flaskvel

class Processor():
	def __init__(self, validator):
		self._validator = validator
		self._errors = {} # error messages already formated
		self._failed_validations = {} # info about failed validations
		self._parsed_rules = None
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
					(nullable and field_value is None and not rule_predicate in Flaskvel._null_intolerant_rules)):
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

		# 	# DELETE ME!
		# 	field_type = self.get_field_type(field_name)
		# 	print("{0} -> {1} / {2}".format(field_name, field_type, type(self.get_field_value(field_name))))
		# print("\n")
		# # DELETE ME!
		return validation_passed

	def get_field_type(self, field_name):
		rules = self._parsed_rules[field_name]
		value = self.get_field_value(field_name)

		for rule in [
			RulesPredicates.DIGITS,
			RulesPredicates.DIGITS_BETWEEN,
			RulesPredicates.INTEGER,
			RulesPredicates.NUMERIC,]:
			if rule in rules:
				if self.handler_integer(value=value) or self.handler_numeric(value=value):
					return FieldTypes.NUMERIC
				else:
					return FieldTypes.UNKOWN

		for rule in [
			RulesPredicates.FILE,
			RulesPredicates.IMAGE,
			RulesPredicates.DIMENSIONS,]:
			if rule in rules:
				if self.handler_file(value=value):
					return FieldTypes.FILE
				else:
					return FieldTypes.UNKOWN

		for rule in [
			RulesPredicates.STRING,
			RulesPredicates.ALPHA,
			RulesPredicates.ALPHA_DASH,]:
			if rule in rules:
				if self.handler_string(value=value):
					return FieldTypes.STRING
				else:
					return FieldTypes.UNKOWN

		for rule in [
			RulesPredicates.ARRAY,
			RulesPredicates.DISTINCT,]:
			if rule in rules:
				if self.handler_array(value=value):
					return FieldTypes.ARRAY
				else:
					return FieldTypes.UNKOWN

		for rule in [RulesPredicates.JSON,]:
			if rule in rules:
				if self.handler_json(value=value):
					return FieldTypes.JSON
				else:
					return FieldTypes.UNKOWN

		if isinstance(value, int) or isinstance(value, float):
			return FieldTypes.NUMERIC

		if isinstance(value, FileStorage):
			return FieldTypes.FILE

		if isinstance(value, list):
			return FieldTypes.ARRAY

		if isinstance(value, dict):
			return FieldTypes.JSON

		if isinstance(value, str):
			if self.handler_integer(value=value) or self.handler_numeric(value=value):
				return FieldTypes.NUMERIC

			if self.handler_array(value=value):
				return FieldTypes.ARRAY

			if self.handler_json(value=value):
				return FieldTypes.JSON

			return FieldTypes.STRING

		return FieldTypes.UNKOWN

	def get_field_value(self, field_name):
		if field_name in request.files:
			return request.files.get(field_name)

		result = request.json if request.is_json else request.form
		keys = field_name.split('.')
		for key in keys:
			if not isinstance(result, dict):
				return None
			result = result.get(key)
			if not result:
				return None
			try:
				if isinstance(result, str): # parse json strings within forms
					json_obj = json.loads(result)
					if isinstance(json_obj, dict):
						result = json_obj
			except:
				continue
		return result

	def is_field_present(self, field_name):
		if field_name in request.files:
			return True

		result = request.json if request.is_json else request.form
		keys = field_name.split('.')
		for key in keys:
			if key not in result:
				return False
			result = result[key]
		return True

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
		for rule_predicate, params in self._failed_validations[field_name].items():
			params, err_msg_params = params
			message = self._messages.get('{0}.{1}'.format(field_name, rule_predicate))

			if not message:
				message = DefaultMessages.get(rule_predicate)
				if isinstance(message, dict):
					message = message.get(self.get_field_type(field_name))

			if not message:
				errors_strings.append('Validation failed for: ' + str(rule_predicate))
			else:
				errors_strings.append(message.format(*params, field_name=field_name, **err_msg_params))

		return errors_strings

	def _assert_params_types(self, params, params_types, rule_predicate):
		if len(params) < len(params_types):
			raise Exception('Rule <{0}> requires at least {1} parameter.'.format(rule_predicate,len(params_types)))
		
		for i in range(len(params_types)):
			try:
				params_types[i](params[i])
			except:
				raise Exception('Rule <{0}> requires parameter number {1} to be of type {2}.'.format(rule_predicate, i+1, params_types[i].__name__))

	def _compare_fields_size(self, field_a_name, field_b_name, operator):
		value_a = self.get_field_value(field_a_name)
		value_b = self.get_field_value(field_b_name)
		field_a_type = self.get_field_type(field_a_name)
		field_b_type = self.get_field_type(field_b_name)
		if value_a is None or value_b is None or not field_a_type == field_b_type:
			return False
		
		if field_a_type == FieldTypes.STRING:
			return operator(len(value_a), len(value_b))
		elif field_a_type == FieldTypes.NUMERIC:
			return operator(float(value_a), float(value_b))
		elif field_a_type == FieldTypes.ARRAY:
			if isinstance(value_a, str):
				try:
					value_a = ast.literal_eval(value_a)
				except:
					return False
			if isinstance(value_b, str):
				try:
					value_b = ast.literal_eval(value_b)
				except:
					return False
			return isinstance(value_b, list) and isinstance(value_b, list) and operator(len(value_a), len(value_b))
		elif field_a_type == FieldTypes.JSON:
			if isinstance(value_a, str):
				try:
					value_a = json.loads(value_a)
				except:
					return False
			if isinstance(value_b, str):
				try:
					value_b = json.loads(value_b)
				except:
					return False
			return isinstance(value_a, dict) and isinstance(value_b, dict) and operator(len(value_a), len(value_b))
		elif field_a_type == FieldTypes.FILE:
			value_a.seek(0, os.SEEK_END)
			value_b.seek(0, os.SEEK_END)
			file_a_size = round(value_a.tell() / 1024)
			file_b_size = round(value_b.tell() / 1024)
			value_a.seek(0, os.SEEK_SET)
			value_b.seek(0, os.SEEK_SET)
			return operator(file_a_size, file_b_size)
		return False

	def _compare_single_field_size(self, field, size, operator):
		field_value = self.get_field_value(field)
		field_type = self.get_field_type(field)
		if field_type == FieldTypes.STRING:
			return operator(len(field_value), int(size))
		elif field_type == FieldTypes.NUMERIC:
			return operator(float(field_value), float(size))
		elif field_type == FieldTypes.ARRAY:
			if isinstance(field_value, list):
				return operator(len(field_value), int(size))
			if isinstance(field_value, str):
				try:
					field_value = ast.literal_eval(field_value)
					return isinstance(field_value, list) and operator(len(field_value), int(size))
				except:
					return False
		elif field_type == FieldTypes.JSON:
			if isinstance(field_value, dict):
				return operator(len(field_value), int(size))
			if isinstance(field_value, str):
				try:
					field_value = json.loads(field_value)
					return isinstance(field_value, dict) and operator(len(field_value), int(size))
				except:
					return False
		elif field_type == FieldTypes.FILE:
			field_value.seek(0, os.SEEK_END)
			file_size = round(field_value.tell() / 1024)
			field_value.seek(0, os.SEEK_SET)
			return operator(file_size, int(size))
		return False

	def get_rule_handler(self, rule_predicate):
		if rule_predicate in Flaskvel._registered_rules:
			return Flaskvel._registered_rules[rule_predicate]
		handler = 'handler_' + rule_predicate
		if not hasattr(self, handler):
			raise Exception('No handler found for rule <{0}>.\nThis may be caused by a misspelled rule or by using a custom rule with an unregistered handler.'.format(rule_predicate))
		return getattr(self, handler)

	def handler_accepted(self, **kwargs):
		return kwargs['value'] in ['yes', 1, '1', 'on', True, 'true']

	def handler_active_url(self, **kwargs):
		try:
			if requests.head(kwargs['value']).status_code < 400:
				return True
		except:
			return False

	def handler_after(self, **kwargs):
		self._assert_params_types(kwargs['params'], [str], RulesPredicates.AFTER)
		try:
			return parse_date(kwargs['value']) > parse_date(kwargs['params'][0])
		except:
			return False 

	def handler_after_or_equal(self, **kwargs):
		self._assert_params_types(kwargs['params'], [str], RulesPredicates.AFTER_OR_EQUAL)
		try:
			return parse_date(kwargs['value']) >= parse_date(kwargs['params'][0])
		except:
			return False

	def handler_alpha(self, **kwargs):
		pattern = re.compile("^[a-z\s]*$", re.IGNORECASE)
		try:
			return pattern.match(kwargs['value']) is not None
		except:
			return False

	def handler_alpha_dash(self, **kwargs):
		pattern = re.compile("^[a-z\-_\s]*$", re.IGNORECASE)
		try:
			return pattern.match(kwargs['value']) is not None
		except:
			return False

	def handler_alpha_num(self, **kwargs):
		pattern = re.compile("^[a-z0-9\s]*$", re.IGNORECASE)
		try:
			return pattern.match(kwargs['value']) is not None
		except:
			return False

	def handler_array(self, **kwargs):
		value = kwargs['value']
		if isinstance(value, list):
			return True
		if isinstance(value, str):
			try:
				return isinstance(ast.literal_eval(value), list)
			except:
				return False
		return False

	def handler_before(self, **kwargs):
		self._assert_params_types(kwargs['params'], [str], RulesPredicates.BEFORE)
		try:
			return parse_date(kwargs['value']) < parse_date(kwargs['params'][0])
		except:
			return False

	def handler_before_or_equal(self, **kwargs):
		self._assert_params_types(kwargs['params'], [str], RulesPredicates.BEFORE_OR_EQUAL)
		try:
			return parse_date(kwargs['value']) <= parse_date(kwargs['params'][0])
		except:
			return False

	def handler_between(self, **kwargs):
		self._assert_params_types(kwargs['params'], [int, int], RulesPredicates.BETWEEN)
		params = kwargs['params']
		return (self._compare_single_field_size(kwargs['field_name'], params[0], operator.gt) and
				self._compare_single_field_size(kwargs['field_name'], params[1], operator.lt))

	def handler_boolean(self, **kwargs):
		value = kwargs['value']
		if isinstance(value, bool):
			return True
		return value in [1, 0, '1', '0', True, False]

	def handler_confirmed(self, **kwargs):
		return kwargs['value'] == self.get_field_value("{0}_confirmation".format(kwargs['field_name']))

	def handler_date(self, **kwargs):
		try:
			return parse_date(kwargs['value'])
		except:
			return False

	def handler_date_equals(self, **kwargs):
		self._assert_params_types(kwargs['params'], [str], RulesPredicates.DATE_EQUALS)
		try:
			return parse_date(kwargs['value']) == parse_date(kwargs['params'][0])
		except:
			return False

	def handler_date_format(self, **kwargs):
		self._assert_params_types(kwargs['params'], [str], RulesPredicates.DATE_FORMAT)
		value = kwargs['value']
		date_format = kwargs['params'][0]
		try:
			datetime.strptime(value, date_format)
			return True
		except:
			return False

	def handler_different(self, **kwargs):
		value = kwargs['value']
		params = kwargs['params']
		kwargs['err_msg_params']['all_params'] = params
		for param in params:
			other_value = self.get_field_value(param)
			if value == other_value:
				return False
		return True

	def handler_digits(self, **kwargs):
		self._assert_params_types(kwargs['params'], [int], RulesPredicates.DIGITS)
		value = kwargs['value']
		if isinstance(value, str):
			if value.isnumeric() and len(value) == int(kwargs['params'][0]):
				return True
		if isinstance(value, int) or isinstance(value, float):
			value = str(value)
			value = value.replace(".", "")
			if  len(value) == int(kwargs['params'][0]):
				return True
		return False

	def handler_digits_between(self, **kwargs):
		self._assert_params_types(kwargs['params'], [int, int], RulesPredicates.DIGITS_BETWEEN)
		value = kwargs['value']
		if isinstance(value, str):
			length = len(value)
			if value.isnumeric() and int(kwargs['params'][0]) < length and length < int(kwargs['params'][1]):
				return True
		if isinstance(value, int) or isinstance(value, float):
			value = str(value)
			value = value.replace(".", "")
			length = len(value)
			if  int(kwargs['params'][0]) < length and length < int(kwargs['params'][1]):
				return True
		return False

	def handler_dimensions(self, **kwargs):
		params = kwargs['params']
		self._assert_params_types(params, [str for _ in range(len(params))], RulesPredicates.DIMENSIONS)
		kwargs['err_msg_params']['all_params'] = params

		valid_params = []
		patterns = [
			"(min_width)=(\d+)",
			"(max_width)=(\d+)",
			"(min_height)=(\d+)",
			"(max_height)=(\d+)",
			"(width)=(\d+)",
			"(height)=(\d+)",
			"(ratio)=(\d+)/(\d+)"]
		dim_rules = {}
		for pattern in patterns:
			for param in params:
				match = re.compile(pattern).match(param)
				if match:
					groups = match.groups()
					dim_rules[groups[0]] = groups[1:]
					valid_params.append(param)
		if not len(params) == len(valid_params):
			raise Exception("Invalid parameters for rule 'dimensions': " + str(set(params) - set(valid_params)))

		try:
			image = Image.open(kwargs['value'])
			width, height = image.size
			for dim_rule, dim_params in dim_rules.items():
				if dim_rule == "min_width":
					if not int(dim_params[0]) <= width:
						return False
				elif dim_rule == "max_width":
					if not int(dim_params[0]) >= width:
						return False
				elif dim_rule == "min_height":
					if not int(dim_params[0]) <= height:
						return False
				elif dim_rule == "max_height":
					if not int(dim_params[0]) >= height:
						return False
				elif dim_rule == "width":
					if not int(dim_params[0]) == width:
						return False
				elif dim_rule == "height":
					if not int(dim_params[0]) == height:
						return False
				elif dim_rule == "ratio":
					if not width / int(dim_params[0]) == height / int(dim_params[1]):
						return False
			return True
		except:
			return False

	def handler_distinct(self, **kwargs):
		value = kwargs['value']
		if isinstance(value, list):
			return len(set(value)) == len(value)
		elif isinstance(value, str):
			try:
				value = ast.literal_eval(value)
				return isinstance(value, list) and len(set(value)) == len(value)
			except:
				return True
		return True

	def handler_email(self, **kwargs):
		pattern = re.compile(
			r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*"  # dot-atom
			# quoted-string, see also http://tools.ietf.org/html/rfc2822#section-3.2.5
			r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-\011\013\014\016-\177])*"'
			r')@(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?$', re.IGNORECASE)  # domain)
		try:
			return pattern.match(kwargs['value']) is not None
		except:
			return False

	def handler_ends_with(self, **kwargs):
		value = kwargs['value']
		params = kwargs['params']
		kwargs['err_msg_params']['all_params'] = params

		field_type = self.get_field_type(kwargs['field_name'])
		if field_type == FieldTypes.NUMERIC or field_type == FieldTypes.STRING:
			value = str(value)
			for param in params:
				if value.endswith(param):
					return True
		elif field_type == FieldTypes.ARRAY:
			if isinstance(value, list) and len(value) > 0:
				return value[-1] in params
			elif isinstance(value, str):
				try:
					value = ast.literal_eval(value)
					return isinstance(value, list) and len(value) > 0 and value[-1] in params
				except:
					return False
		elif field_type == FieldTypes.FILE:
			try:
				CHUNK_SIZE = 16
				bytes_read_cnt = 0
				file_buffer = b''
				value.seek(0, os.SEEK_END)
				for param in params:
					# read last n bytes from file
					while len(param) > bytes_read_cnt:
						backward_offset = min(CHUNK_SIZE, value.tell())
						value.seek(-backward_offset, os.SEEK_CUR)
						data = value.read(backward_offset)
						if data == b'':
							break
						file_buffer = data + file_buffer
						bytes_read_cnt += len(data)
						value.seek(-backward_offset, os.SEEK_CUR)
					if file_buffer.endswith(param.encode()):
						value.seek(0, os.SEEK_SET)
						return True
				value.seek(0, os.SEEK_SET)
			except:
				return False
		return False

	def handler_file(self, **kwargs):
		return isinstance(kwargs['value'], FileStorage)

	def handler_filled(self, **kwargs):
		if self.is_field_present(kwargs['field_name']):
			return not kwargs['value'] == None
		return True

	def handler_gt(self, **kwargs):
		self._assert_params_types(kwargs['params'], [str], RulesPredicates.GT)
		return self._compare_fields_size(kwargs['field_name'], kwargs['params'][0], operator.gt)

	def handler_gte(self, **kwargs):
		self._assert_params_types(kwargs['params'], [str], RulesPredicates.GTE)
		return self._compare_fields_size(kwargs['field_name'], kwargs['params'][0], operator.ge)

	def handler_image(self, **kwargs):
		try:
			return kwargs['value'].filename.split(".")[-1] in ['jpg', 'jpeg', 'png', 'bmp', 'gif', 'svg', 'webp']
		except:
			return False

	def handler_in(self, **kwargs):
		kwargs['err_msg_params']['all_params'] = kwargs['params']
		return kwargs['value'] in kwargs['params']

	def handler_in_array(self, **kwargs):
		self._assert_params_types(kwargs['params'], [str], RulesPredicates.IN_ARRAY)
		other = self.get_field_value(kwargs['params'][0])
		try:
			if not isinstance(other, list):
				other = ast.literal_eval(other)
			return isinstance(other, list) and kwargs['value'] in other
		except:
			return False

	def handler_integer(self, **kwargs):
		value = kwargs['value']
		if isinstance(value, int) or isinstance(value, float):
			return True
		try:
			int(value)
			return True
		except:
			return False

	def handler_ip(self, **kwargs):
		value = kwargs['value']
		return self.handler_ipv4(value=value) or self.handler_ipv6(value=value)

	def handler_ipv4(self, **kwargs):
		pattern = re.compile(r'^(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}$')
		try:
			return pattern.match(kwargs['value']) is not None
		except:
			return False

	def handler_ipv6(self, **kwargs):
		pattern = re.compile(
			r'([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|'				# 1:2:3:4:5:6:7:8
			r'([0-9a-fA-F]{1,4}:){1,7}:|'								# 1::                              1:2:3:4:5:6:7::
			r'([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|'				# 1::8             1:2:3:4:5:6::8  1:2:3:4:5:6::8
			r'([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|'		# 1::7:8           1:2:3:4:5::7:8  1:2:3:4:5::8
			r'([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|'		# 1::6:7:8         1:2:3:4::6:7:8  1:2:3:4::8
			r'([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|'		# 1::5:6:7:8       1:2:3::5:6:7:8  1:2:3::8
			r'([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|'		# 1::4:5:6:7:8     1:2::4:5:6:7:8  1:2::8
			r'[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|'				# 1::3:4:5:6:7:8   1::3:4:5:6:7:8  1::8  
			r':((:[0-9a-fA-F]{1,4}){1,7}|:)|'							# ::2:3:4:5:6:7:8  ::2:3:4:5:6:7:8 ::8       ::     
			r'fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|'			# fe80::7:8%eth0   fe80::7:8%1     (link-local IPv6 addresses with zone index)
			r'::(ffff(:0{1,4}){0,1}:){0,1}'
			r'((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}'
			r'(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|'				# ::255.255.255.255   ::ffff:255.255.255.255  ::ffff:0:255.255.255.255  (IPv4-mapped IPv6 addresses and IPv4-translated addresses)
			r'([0-9a-fA-F]{1,4}:){1,4}:'
			r'((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}'
			r'(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])', re.IGNORECASE	# 2001:db8:3:4::192.0.2.33  64:ff9b::192.0.2.33 (IPv4-Embedded IPv6 Address)
		)
		try:
			return pattern.match(kwargs['value']) is not None
		except:
			return False

	def handler_json(self, **kwargs):
		value = kwargs['value']
		if isinstance(value, dict):
			return True
		if isinstance(value, str):
			try:
				json.loads(value)
				return True
			except:
				return False
		return False

	def handler_lt(self, **kwargs):
		self._assert_params_types(kwargs['params'], [str], RulesPredicates.LT)
		return self._compare_fields_size(kwargs['field_name'], kwargs['params'][0], operator.lt)

	def handler_lte(self, **kwargs):
		self._assert_params_types(kwargs['params'], [str], RulesPredicates.LTE)
		return self._compare_fields_size(kwargs['field_name'], kwargs['params'][0], operator.le)

	def handler_max(self, **kwargs):
		self._assert_params_types(kwargs['params'], [int], RulesPredicates.MAX)
		return self._compare_single_field_size(kwargs['field_name'], kwargs['params'][0], operator.le)

	def handler_mimetypes(self, **kwargs):
		try:
			return kwargs['value'].mimetype in kwargs['params']
		except:
			return False

	def handler_min(self, **kwargs):
		self._assert_params_types(kwargs['params'], [int], RulesPredicates.MIN)
		return self._compare_single_field_size(kwargs['field_name'], kwargs['params'][0], operator.ge)

	def handler_not_in(self, **kwargs):
		kwargs['err_msg_params']['all_params'] = kwargs['params']
		return kwargs['value'] not in kwargs['params']

	def handler_not_in_array(self, **kwargs):
		self._assert_params_types(kwargs['params'], [str], RulesPredicates.NOT_IN_ARRAY)
		other = self.get_field_value(kwargs['params'][0])
		try:
			if not isinstance(other, list):
				other = ast.literal_eval(other)
			return isinstance(other, list) and kwargs['value'] not in other
		except:
			return False

	def handler_not_regex(self, **kwargs):
		self._assert_params_types(kwargs['params'], [str], RulesPredicates.NOT_REGEX)
		try:
			pattern = re.compile(kwargs['params'][0])
			return pattern.match(kwargs['value']) is None
		except:
			return False

	def handler_numeric(self, **kwargs):
		value = kwargs['value']
		if isinstance(value, int) or isinstance(value, float):
			return True
		try:
			float(value)
			return True
		except:
			return False

	def handler_present(self, **kwargs):
		return not kwargs['value'] == None or self.is_field_present(kwargs['field_name'])

	def handler_regex(self, **kwargs):
		self._assert_params_types(kwargs['params'], [str], RulesPredicates.REGEX)
		try:
			pattern = re.compile(kwargs['params'][0])
			return pattern.match(kwargs['value']) is not None
		except:
			return False

	def handler_required(self, **kwargs):
		return kwargs['value'] != None

	def handler_required_if(self, **kwargs):
		self._assert_params_types(kwargs['params'], [str, str], RulesPredicates.REQUIRED_IF)
		params = kwargs['params']
		kwargs['err_msg_params']['the_rest_of_params'] = params[1:]
		other_value = self.get_field_value(params[0])
		# if not other_value in params[1:]:
		# 	return True
		# else:
		# 	return kwargs['value'] is not None
		return not other_value in params[1:] or kwargs['value'] is not None

	def handler_required_unless(self, **kwargs):
		self._assert_params_types(kwargs['params'], [str, str], RulesPredicates.REQUIRED_UNLESS)
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
		self._assert_params_types(kwargs['params'], [int], RulesPredicates.SIZE)
		return self._compare_single_field_size(kwargs['field_name'], kwargs['params'][0], operator.eq)

	def handler_starts_with(self, **kwargs):
		value = kwargs['value']
		params = kwargs['params']
		kwargs['err_msg_params']['all_params'] = params

		field_type = self.get_field_type(kwargs['field_name'])
		if field_type == FieldTypes.NUMERIC or field_type == FieldTypes.STRING:
			value = str(value)
			for param in params:
				if value.startswith(param):
					return True
		elif field_type == FieldTypes.ARRAY:
			if isinstance(value, list) and len(value) > 0:
				return value[0] in params
			elif isinstance(value, str):
				try:
					value = ast.literal_eval(value)
					return isinstance(value, list) and len(value) > 0 and value[0] in params
				except:
					return False
		elif field_type == FieldTypes.FILE:
			try:
				CHUNK_SIZE = 16
				bytes_read_cnt = 0
				file_buffer = b''
				value.seek(0, os.SEEK_SET)
				for param in params:
					while len(param) > bytes_read_cnt:
						# read first n bytes from file
						data = value.read(CHUNK_SIZE)
						if data == b'':
							break
						file_buffer += data
						bytes_read_cnt += len(data)
					if file_buffer.startswith(param.encode()):
						value.seek(0, os.SEEK_SET)
						return True
				value.seek(0, os.SEEK_SET)
			except:
				return False
		return False

	def handler_string(self, **kwargs):
		return isinstance(kwargs['value'], str)

	def handler_timezone(self, **kwargs):
		return kwargs['value'] in pytz.all_timezones

	def handler_url(self, **kwargs):
		pattern = re.compile(
			r'^(?:http|ftp)s?://' # optional http:// or https://
			r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
			r'localhost|' #localhost...
			r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
			r'(?::\d+)?' # optional port
			r'(?:/?|[/?]\S+)$', re.IGNORECASE)
		try:
			return pattern.match(kwargs['value']) is not None
		except:
			return False

	def handler_uuid(self, **kwargs):
		pattern = re.compile("^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", re.IGNORECASE)
		try:
			return pattern.match(kwargs['value']) is not None
		except:
			return False