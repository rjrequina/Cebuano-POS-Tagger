from copy import deepcopy
import string
import time

from wrappers import Word
from search import search_term
from repos import suffixes, prefixes, function_words


'''
Given a word, stems the word and returns the root and affixes of the word
'''
def stem_word(word=None):
    if word:
        processes = [
            [],
            ['inf'],
            ['pref'],
            ['inf', 'pref'],
            ['redup'],
            ['inf', 'redup'],
            ['pref', 'redup'],
            ['inf', 'pref', 'redup'],
            ['suff'],
            ['inf', 'suff'],
            ['pref', 'suff'],
            ['inf', 'pref', 'suff'],
            ['redup', 'suff'],
            ['inf', 'redup', 'suff'],
            ['pref', 'redup', 'suff'],
            ['inf', 'pref', 'suff', 'redup']

        ]

        stem = Word(text=word)
        temp_stem = deepcopy(stem)
        for process in processes:
            temp_stem = remove_affixes(process=process, stem=temp_stem)
            temp_stem = remove_inflections(process=process, stem=temp_stem)
            temp_stem = lookup(stem=temp_stem)
            temp_stem = affix_lookup(stem=temp_stem)

            if temp_stem.is_entry or len(process) == 4:
                stem = temp_stem
                break

            temp_stem = deepcopy(stem)
        return stem
    return None

'''
Remove affixes
'''
def remove_affixes(process=[], stem=None):
    if not stem:
        return stem

    if 'pref' in process:
        stem = strip_prefix(stem=stem)

    if 'suff' in process:
        stem = strip_suffix(stem=stem)

    if 'inf' in process:
        stem = strip_infix(stem=stem)

    return stem

'''
Remove inflections
'''
def remove_inflections(process=[], stem=None):
    if 'redup' in process:
        stem = remove_duplication(stem=stem)

    return stem

'''
Helper function that will strip prefixes from the word
'''
def strip_prefix(stem=None):
    if not stem:
        return stem

    longest_prefix = None
    word = stem.root
    word = ''.join([i for i in word if i.isalpha()])

    for prefix in prefixes():
        if word.startswith(prefix):
            if not longest_prefix:
                longest_prefix = prefix
            else:
                temp_stem = deepcopy(stem)
                temp_stem.root = string.replace(word, prefix, '')
                temp_stem = lookup(stem=temp_stem)
                if temp_stem.is_entry:
                    longest_prefix = prefix
                    break

    if longest_prefix:
        stem.root = string.replace(word, longest_prefix, '')
        stem.prefix = longest_prefix
    return stem

'''
Helper function that will strip suffixes from the word
'''
def strip_suffix(stem=None):
    if not stem:
        return stem

    word = stem.root
    word = ''.join([i for i in word if i.isalpha()])
    longest_suffix = None

    for suffix in suffixes():
        if word.endswith(suffix):
            if not longest_suffix:
                longest_suffix = suffix
            else:

                temp_stem = deepcopy(stem)
                temp_stem.root = word[0:word.rfind(suffix)]
                temp_stem = lookup(stem=temp_stem)
                if temp_stem.is_entry:
                    longest_suffix = suffix
                    break

    if longest_suffix:
        stem.root = word[0:word.rfind(longest_suffix)]
        stem.suffix = longest_suffix
    return stem

'''
Strip infixes -um- and -in-
'''
def strip_infix(stem=None):
    if not stem:
        return stem

    word = stem.root
    if word.find('um') > 0 or word.find('in') > 0:
        if word.find('in'):
            stem.root = word.replace('in', '')
            stem.infix = 'in'
        elif word.find('um'):
            stem.root = word.replace('um', '')
            stem.infix = 'um'

    return stem

'''
Removes duplication of a word
'''
def remove_duplication(stem=None):
    if not stem:
        return stem

    longest_string = None
    size = 1
    stem.root = ''.join([i for i in stem.root if i.isalpha()])
    for i in range(1, len(stem.root)):
        str_a = stem.root[0:i]
        str_b = stem.root[i: i + size]

        if str_a == str_b:
            longest_string = str_a
        size += 1

    if longest_string:
        if len(longest_string) > 2:
            stem.root = longest_string

    return stem

'''
Checks if the root exists in dictionary
If does not exists, sets root, prefix and suffix to None
as an indicator
'''
def lookup(stem=None):
    entry = stem.root.lower().replace('o', 'u')
    entry = entry.replace('e', 'i')

    if entry in function_words() or search_term(term=stem.root):
        stem.is_entry = True
        return stem
    else:
        stem.is_entry = False
        return stem

'''
Checks if the root is an affix
'''
def affix_lookup(stem=None):
    if stem.root in prefixes() or stem.root in suffixes():
        stem.is_entry = True
        return stem

    return stem


if __name__ == "__main__":
    # start = int(round(time.time() * 1000))
    # stem = stem_word(word='pagkabuang-buang')
    # print(stem.root)
    # print(stem.prefix)
    # end = int(round(time.time() * 1000))
    # print(end - start)
    pass
