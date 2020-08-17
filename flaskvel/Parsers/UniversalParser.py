from .ArrayParser import ArrayParser
from .PipedStringParser import PipedStringParser
from ..ParsedRule import ParsedRule

class UniversalParser():
	@staticmethod
	def parse(rules):
		parsed_rules = {}
		for field_name, field_rules in rules.items():
			if isinstance(field_rules, list):
				parsed_rules[field_name] = ArrayParser.parse(field_rules)
			elif isinstance(field_rules, str):
				parsed_rules[field_name] = PipedStringParser.parse(field_rules)
			elif isinstance(field_rules, ParsedRule):
				parsed_rules[field_name] = [field_rules]
			elif callable(field_rules):
				parsed_rules[field_name] = [ParsedRule(field_rules)]
			else:
				raise Exception("Invalid rules; Expected list/str/callable but got {2} for: <{0}: {1}>".format(field_name, field_rules, type(field_rules)))
		return parsed_rules
