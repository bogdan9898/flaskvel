from .ArrayParser import ArrayParser

class PipedStringParser():
	@staticmethod
	def parse(rules):
		return ArrayParser.parse(rules.split('|'))