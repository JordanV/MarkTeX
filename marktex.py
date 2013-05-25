# *-* coding:Utf8
# To Do
# Ensure that emph/bold/etc. can end with a punctuation sign and not necessarily a whitespace
# Possibility to write things like _*test*_ ?
# Ignore math mode in text
# only-rules to not print begin and end (for existing documents)

import pdb
import sys
import re
from TemplateParser import TemplateParser

def determine_type(chunk):
	chunk = chunk.strip()

	if chunk[:2] == "$$" or chunk[:2] == "\\[" or chunk[:17] == "\\begin{equation}" :
		return "MATH"
	elif chunk[0] == '-':
		return "LIST"
	elif chunk[0] == "=":
		return "TITLE"
	elif chunk[0] is not "\\":
		return "TEXT"
	else:
		return "ASIS"

def parse_list(chunk):
	output = "\\begin{itemize}\n"
	for line in chunk.split("\n"):
		if line is not '':
			line = line.strip()[1:]
			output += "\\item " + line.strip() + "\n"
	output += "\\end{itemize}\n"
	output.strip()
	return parse_text(output)

def parse_text(chunk):
	# punctuation = .,;:!?

	chunk = chunk.replace(' ' + EMPH_DELIMITER, EMPH_BEGIN)
	chunk = chunk.replace( EMPH_DELIMITER + ' ', EMPH_END)
	chunk = chunk.replace(' ' + BOLD_DELIMITER, BOLD_BEGIN)
	chunk = chunk.replace(BOLD_DELIMITER + ' ', BOLD_END)
	return chunk

def parse_title(chunk):
	title_level = -1
	chunk = chunk.strip()

	if chunk[:3] == SUBSUBSECTION_DELIMITER:
		title_level = 3
	elif chunk[:2] == SUBSECTION_DELIMITER:
		title_level = 2
	elif chunk[0] == SECTION_DELIMITER:
		title_level = 1

	title = chunk.strip(SECTION_DELIMITER).strip()
	if title_level == 1:
		title = SECTION_BEGIN + title + SECTION_END
	elif title_level == 2:
		title = SUBSECTION_BEGIN + title + SUBSECTION_END
	elif title_level == 3:
		title = SUBSUBSECTION_BEGIN + title + SUBSUBSECTION_END

	return title

# ===== Main ====
if sys.argv[1] == "help" :
	print 'Usage : marktex <input_file> <output_file> (template)'
	print 'To see available templates, run "marktex show-tpl" '
	print 'To show this help, run "marktex help"'
	sys.exit()
elif sys.argv[1] == "show-tpl":
	print 'List of available templates'
	sys.exit()
elif len(sys.argv) < 3:
	print 'Bad usage. Run "marktex help" for more information.'
	sys.exit()

fic = open(sys.argv[1], 'r')
out_fic = open(sys.argv[2], 'w')
if len(sys.argv) == 4:
	tpl_name = sys.argv[3]
else:
	tpl_name = "default"

tpl = TemplateParser(tpl_name)
tpl.parse_template()

EMPH_BEGIN = ' ' + tpl._rules["emph"]["begin"].encode()
EMPH_END = tpl._rules["emph"]["end"].encode() + ' '
EMPH_DELIMITER = tpl._rules["emph"]["delim"].encode()
BOLD_BEGIN = ' ' + tpl._rules["bold"]["begin"].encode()
BOLD_END = tpl._rules["bold"]["end"].encode() + ' '
BOLD_DELIMITER = tpl._rules["bold"]["delim"].encode()
SECTION_BEGIN = ' ' + tpl._rules["section"]["begin"].encode()
SECTION_END = tpl._rules["section"]["end"].encode() + ' '
SECTION_DELIMITER = tpl._rules["section"]["delim"].encode()
SUBSECTION_BEGIN = ' ' + tpl._rules["subsection"]["begin"].encode()
SUBSECTION_END = tpl._rules["subsection"]["end"].encode() + ' '
SUBSECTION_DELIMITER = tpl._rules["subsection"]["delim"].encode()
SUBSUBSECTION_BEGIN = ' ' + tpl._rules["subsubsection"]["begin"].encode()
SUBSUBSECTION_END = tpl._rules["subsubsection"]["end"].encode() + ' '
SUBSUBSECTION_DELIMITER = tpl._rules["subsubsection"]["delim"].encode()

DOC_BEGIN = tpl._begin
DOC_END = tpl._end

text = fic.read()
# Work on file to eliminate tabs -- Messes up with de block delimiter otherwise
text = text.replace("\t", "")

paragraphs = text.split("\n\n")

# DEBUG : print detected block type
# for chunk in paragraphs:
	# print(determine_type(chunk))
	# pdb.set_trace()

out_fic.write(DOC_BEGIN)

for chunk in paragraphs:
	if determine_type(chunk) == 'TEXT':
		chunk = parse_text(chunk)
	elif determine_type(chunk) == "LIST":
		chunk = parse_list(chunk)
	elif determine_type(chunk) == "MATH":
		pass
	elif determine_type(chunk) == "TITLE":
		chunk = parse_title(chunk)
	elif determine_type(chunk) == "ASIS":
		# Leave chunk as it is
		pass
	chunk += "\n\n"
	out_fic.write(chunk)

out_fic.write(DOC_END)
# print(paragraphs)
