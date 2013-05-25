# Rule Parser class
# Parses custom rules from a file

class TemplateParser():
	def __init__(self, tpl_name = "default"):
		self._template_name = tpl_name
		self._rules = {}
		self._begin = ""
		self._packages = ""
		self._end = ""
	
	def parse_beginning(self):
		with open('templates/' + self._template_name + '/begin.txt') as beginning_file:
			self._begin = beginning_file.read()
		beginning_file.close()

	def parse_end(self):
		with open('templates/' + self._template_name + '/end.txt') as ending_file:
			self._end = ending_file.read()
		ending_file.close()

	def parse_packages(self):
		with open('templates/' + self._template_name + '/packages.txt') as pack_file:
			self._packages = pack_file.read()
		pack_file.close()

	def parse_rules(self):
		return 0

	def parse_template(self):
		parse_beginning()
		parse_packages()
		parse_end()
		parse_rules()

	def get_begin(self):
		return self._begin