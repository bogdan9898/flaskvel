from ..ParsedRule import ParsedRule

class ArrayParser():
	@staticmethod
	def parse(rules):
		parsed_rules = []
		for rule in rules:
			if callable(rule):
				parsed_rules.append(ParsedRule(rule))
				continue
			elif isinstance(rule, ParsedRule):
				parsed_rules.append(rule)
				continue
			tmp = rule.split(":")
			predicate = tmp[0]
			params = []
			if len(tmp) > 1:
				params = tmp[1].split(',')
			parsed_rules.append(ParsedRule(predicate, params))
		return parsed_rules
