# Rule Parser class
# *-* coding:Utf8
# Parses custom rules from a file
import json

class TemplateParser():
	def __init__(self, tpl_name = "default"):
		self._template_name = tpl_name
		self._rules = {}
		self._begin = ""
		self._end = ""
	
	def parse_beginning(self):
		with open('templates/' + self._template_name + '/begin.txt') as beginning_file:
			self._begin = beginning_file.read()
		beginning_file.close()

	def parse_end(self):
		with open('templates/' + self._template_name + '/end.txt') as ending_file:
			self._end = ending_file.read()
		ending_file.close()

	def parse_rules(self):
		raw_rules = open("templates/" + self._template_name + "/rules.json").read()

		self._rules = json.loads(raw_rules)

	def parse_template(self):
		self.parse_beginning()
		self.parse_end()
		self.parse_rules()