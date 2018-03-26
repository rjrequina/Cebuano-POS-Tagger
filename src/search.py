import string
from utilities import read_file
from repos import dictionary


'''
Search term in dictionary
'''
def search_term(term=''):
	entries = dictionary()
	
	term = term.lower()
    if term not in entries:
        term = string.replace(term, 'o', 'u')
        term = string.replace(term, 'e', 'i')

    if term not in entries:
        return None

    return entries[term]
