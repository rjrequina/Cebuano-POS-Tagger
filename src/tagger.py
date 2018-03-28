import string
from polyglot.text import Text

from utilities import read_file, write_file
from wrappers import Word
from stemmer import stem_word
import stemmer
from search import search_term
from repos import dictionary, prefixes, suffixes, function_words, lexical_rules, contextual_rules


'''
Given a Cebuano sentence, it will tag all words with its corresponding POS tags
'''
def tag_sentence(text=''):
    tokens = tokenize(text=text)
    words = assign_pos_tags(tokens=tokens)
    words = disambiguate_pos_tags(words=words)

    return words

'''
Transform sentence to tokens
'''
def tokenize(text=''):
    tokens = list(Text(text).words)
    result = []
    get_next = False
    for token in tokens:
        if token == '-':
            result[-1] = result[-1] + token
            get_next = True
        elif token != '-' and get_next:
            result[-1] = result[-1] + token
            get_next = False
        else:
            result.append(token)

    return result


'''
POS Tag Assignment
Assigns all possible POS tags per token
'''
def assign_pos_tags(tokens=[]):
    words = []
    for token in tokens:
        stem = stem_word(word=token)
        word = dictionary_search(word=stem)
        word = function_words_search(word=stem)
        word = apply_lexical_rules_assignment(word=stem)
        word = apply_capitalization_assignment(word=stem)

        if len(word.pos_tags) == 0:
            if stem.text.isdigit():
                # Assign num if the word is a numerical value
                word.pos_tags = ['NUM']
            elif stem.text in string.punctuation:
                word.pos_tags = ['SYM']
            else:
                word.pos_tags = ['OTH']

        words.append(word)
    return words


'''
Assign possible tags helper function: Dictionary Search
'''
def dictionary_search(word=None):
    if word.is_entry:
        pos_tags = search_term(entries=stemmer.entries, term=word.root)
        if pos_tags:
            pos_tags = [tag for tag in pos_tags if tag != 'OTH']
            pos_tags = ['PART' if tag == 'PREP' else tag for tag in pos_tags]
            word.pos_tags = pos_tags
            word.root_tags = word.pos_tags

    return word


'''
Assign possible tags helper function: Function Word Search
'''
def function_words_search(word=None):
    entry = word.root.lower().replace('o', 'u')
    entry = entry.replace('e', 'i')

    if entry in function_words():
        word.pos_tags += function_words()[entry]
        word.pos_tags = list(set(word.pos_tags))

    return word


'''
Assign possible tags helper function: Applying Lexical Rules Assignment
'''
def apply_lexical_rules_assignment(word=None):
    # if not word.is_close:

    all_lexical_rules = select_lexical_rules(word=word)
    is_unknown = len(word.pos_tags) == 0

    for rule in all_lexical_rules:
        intersection = list(set(rule.base).intersection(word.pos_tags))

        if rule.target not in word.pos_tags:
            if not is_unknown:
                if len(intersection) == 0:
                    if rule.target not in word.pos_tags:
                        word.pos_tags.append(rule.target)
                        word.derived_tags.append(rule.target)
            else:
                # For unknown words
                if rule.target not in word.pos_tags:
                    word.pos_tags.append(rule.target)
                    word.derived_tags.append(rule.target)

    return word

'''
Assign NOUN if capitalized
'''
def apply_capitalization_assignment(word=None):
    if len(word.pos_tags) == 0:
        if word.orig_text[0].isupper():
            word.pos_tags = ['NOUN']

    return word
'''
POS Tags Disambiguation
Disambiguate multiple POS tags
'''
def disambiguate_pos_tags(words=None):
    words = apply_lexical_disambiguation(words=words)
    # words = apply_contextual_disambiguation(words=words)

    return words


'''
Lexical Disambiguation
'''
def apply_lexical_disambiguation(words=None):
    open_tags = ['NOUN', 'ADJ', 'VERB', 'NUM', 'ADV']

    # all_lexical_rules = lexical_rules()
    for word in words:
        retain_tags = []
        if len(word.pos_tags) > 1:
            # Checks if the word is a function word.
            # If it is, it will remove the open POS tags that belongs to the word
            # If it isn't, it will remove the closed POS tags
            # if word.is_close:
            #     word.pos_tags = [item for item in word.pos_tags if item not in open_tags]
            # else:
            #     word.pos_tags = [item for item in word.pos_tags if item in open_tags]


            # Apply lexical rules for open words only
            # Words with these POS tags have affixes attach to them
            # if not word.is_close:

            approp_lexical_rules = select_lexical_rules(word=word)
            for rule in approp_lexical_rules:
                if rule.target in word.pos_tags:
                    retain_tags.append(rule.target)


            if len(retain_tags) > 0:
                orig_tags = word.pos_tags
                word.pos_tags = []
                for tag in retain_tags:
                    word.pos_tags.append(tag)

    return words


'''
Contextual Disambiguation
'''
def apply_contextual_disambiguation(words=None):
    for idx, word in enumerate(words):
        # print(word.stem.word)
        target = contextual_rules[0].target
        is_valid = False
        for rule in contextual_rules():
            if len(word.pos_tags) > 1:
                if target != rule.target:
                    if not is_valid:
                        # Removes the target pos tag if not valid
                        # Checks if the number of pos tags of the current word
                        # is greater than 1 if less than or equal to 1
                        # will retain the pos tag
                        if len(word.pos_tags) > 1 and target in word.pos_tags:
                            word.pos_tags.remove(target)
                    target = rule.target
                    is_valid = False

                if target in word.pos_tags:
                    for condition in rule.context_conditions:
                        position = 0
                        if condition.position != 0:
                            position = idx + condition.position

                            # Checks if the pos tags in the current position is empty
                            # It means the word is a symbol
                            other_word = get_word(words=words, position=position)
                            if other_word:
                                if len(other_word.pos_tags) == 0:
                                    if condition.position < 0:
                                        # Move one step to the left
                                        position = idx + (condition.position - 1)
                                    else:
                                        # Move one step to the right
                                        position = idx + (condition.position + 1)

                        other_word = get_word(words=words, position=position)
                        if other_word:
                            if not condition.pos_tag in other_word.pos_tags:
                                is_valid = False
                                break
                            else:
                                is_valid = True

    return words

'''
Helper function for contextual Disambiguation
Gets the word in the current position
If None is returned, it means the position is invalid
'''
def get_word(words=[], position=-1):
    if position >= 0 and position < len(words):
        return words[position]

    return None


'''
Return the applicable lexical rules given a word
'''
def select_lexical_rules(word=None):
    applicable_lexical_rules = []
    if word:
        for rule in lexical_rules():
            if word.prefix == rule.prefix and word.suffix == rule.suffix and word.infix == rule.infix:
                applicable_lexical_rules.append(rule)

    return applicable_lexical_rules


'''
Return the applicable contextual rules given a word
'''
def select_contextual_rules(word=None):
    applicable_contextual_rules = []
    if word:
        for rule in contextual_rules():
            if rule.target in word.pos_tags:
                applicable_contextual_rules.append(rule)

    return applicable_contextual_rules

if __name__ == '__main__':
    tokens = tag_sentence('Ang bata naligo sa sapa.')
    sentence = ''
    for token in tokens:
        sentence += str(token) + ' '

    print(sentence)
