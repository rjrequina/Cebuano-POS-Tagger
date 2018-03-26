from utilities import read_file, write_file
from wrappers import LexicalRule, ContextualRule, ContextCondition


'''
Fetch dictionary
'''
def dictionary():
	return read_file('../data/dict/cebposdict.txt', dict_format=True)

'''
Fetch prefixes
'''
def prefixes():
	return read_file('../data/affixes/PREF.txt', strip=True)

'''
Fetch suffixes
'''
def suffixes():
	return read_file('../data/affixes/SUFF.txt', strip=True)

'''
Fetch function words
'''
def function_words():
	tags = ['CONJ', 'DET', 'PART', 'PRON']
	function_words = []

	for tag in tags:
		words = read_file('../data/function_words/' + tag + '.txt', strip=True)
		function_words += words

	return list(set(function_words))

'''
Fetch lexical rules
'''
def lexical_rules():
	raw = read_file('../data/rules/LEXICAL.txt', strip=True)
	rules = []

	for r in raw:
		rule = LexicalRule()

		string = r.split(' ')

		rule.target = string[0]
		rule.prefix = string[1] if string[1] != '-' else None
		rule.infix  = string[2] if string[2] != '-' else None
		rule.suffix = string[3] if string[3] != '-' else None
		rule.base = list(string[4:])

		rules.append(rule)

	return rules


'''
Fetch contextual rules
'''
def contextual_rules():
	raw = read_file('../data/rules/CONTEXTUAL.txt', strip=True)
	rules = []

	for r in raw:
		rule = ContextualRule()

		string = r.split(' ')

		rule.operator = string[0]
		rule.target = string[1]


		i = 2
		while i < len(string):
			condition = ContextCondition()

			position = string[i]

			if 'C' in position:
				condition.careful_mode = True
				position = position.replace('C', '')

			condition.position = int(position)
			condition.pos_tag = string[i + 1]

			rule.context_conditions.append(condition)

			i += 2

		rules.append(rule)

	return rules