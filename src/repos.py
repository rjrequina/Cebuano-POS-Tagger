from utilities import read_file, write_file
from wrappers import LexicalRule


'''
Fetch dictionary
'''
def dictionary():
	return read_file('data/dict/cebposdict.txt', dict_format=True)

'''
Fetch prefixes
'''
def prefixes():
	return read_file('data/affixes/PREF.txt', strip=True)

'''
Fetch suffixes
'''
def suffixes():
	return read_file('data/affixes/SUFF.txt', strip=True)

'''
Fetch function words
'''
def function_words():
	tags = ['CONJ', 'DET', 'PART', 'PRON']
	function_words = []

	for tag in tags:
		words = read_file('data/function_words/' + tag + '.txt', strip=True)
		function_words += words

	return list(set(function_words))

'''
Fetch Lexical
'''