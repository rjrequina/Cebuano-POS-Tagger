import string
# from polyglot.text import Text
from nltk.tokenize import word_tokenize
from cebdict import dictionary
from cebstemmer import stemmer

from utilities import read_file, write_file
from wrappers import Word
from repos import  lexical_rules, contextual_rules


'''
Given a Cebuano sentence, it will tag all words with its corresponding POS tags
'''
def tag_sentence(text=''):
    tokens = tokenize(text=text)
    words = assign_pos_tags(tokens=tokens)
    words = disambiguate_pos_tags(words=words)

    sentence = []
    for word in words:
        sentence.append((word.orig_text.encode('utf-8'), word.pos_tags[0]))

    return sentence

'''
Transform sentence to tokens
'''
def tokenize(text=''):
    # tokens = list(Text(text).words)
    return word_tokenize(text.strip())
    # result = []
    # get_next = False
    # for token in tokens:
    #     if token == '-':
    #         result[-1] = result[-1] + token
    #         get_next = True
    #     elif token != '-' and get_next:
    #         result[-1] = result[-1] + token
    #         get_next = False
    #     else:
    #         result.append(token)

    # return result


'''
POS Tag Assignment
Assigns all possible POS tags per token
'''
def assign_pos_tags(tokens=[]):
    words = []
    for idx, token in enumerate(tokens):
        stem = stemmer.stem_word(word=token, as_object=True)
        word = dictionary_search(word=stem)
        #word = function_words_search(word=stem)
        word = apply_lexical_rules_assignment(word=stem)
        word = apply_capitalization_assignment(word=stem, pos=idx)

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
        # pos_tags = search_term(entries=stemmer.entries, term=word.root)
        pos_tags = dictionary.search(word.root)
        if pos_tags:
            word.pos_tags = pos_tags
            word.root_tags = word.pos_tags

    return word


'''
Assign possible tags helper function: Function Word Search
'''
# def function_words_search(word=None):
#     entry = word.root.lower().replace('o', 'u')
#     entry = entry.replace('e', 'i')

#     if entry in function_words():
#         word.pos_tags += function_words()[entry]
#         word.pos_tags = list(set(word.pos_tags))

#     return word


'''
Assign possible tags helper function: Applying Lexical Rules Assignment
'''
def apply_lexical_rules_assignment(word=None):

    all_lexical_rules = select_lexical_rules(word=word)
    is_unknown = len(word.pos_tags) == 0

    for rule in all_lexical_rules:
        intersection = list(set(word.pos_tags).intersection(rule.base))

        if len(rule.base) == 0:
            intersection = [1]

        if is_unknown:
            if rule.target not in word.pos_tags:
                word.pos_tags.append(rule.target)
                word.pos_tags = list(set(word.pos_tags))
                word.derived_tags.append(rule.target)
                word.derived_tags = list(set(word.derived_tags))
        else:
            if len(intersection) > 0:
                if rule.target not in word.pos_tags:
                    word.pos_tags.append(rule.target)
                    word.pos_tags = list(set(word.pos_tags))
                    word.derived_tags.append(rule.target)
                    word.derived_tags = list(set(word.derived_tags))
    return word

'''
Assign NOUN if capitalized
'''
def apply_capitalization_assignment(word=None, pos=-1):
    if len(word.pos_tags) == 0:
        if word.orig_text[0].isupper():
            word.pos_tags = ['NOUN']

    if pos > 0:
        if word.orig_text[0].isupper():
            word.pos_tags = ['NOUN']

    return word
'''
POS Tags Disambiguation
Disambiguate multiple POS tags
'''
def disambiguate_pos_tags(words=None):
    words = apply_lexical_disambiguation(words=words)
    words = apply_contextual_disambiguation(words=words)

    return words


'''
Lexical Disambiguation
'''
def apply_lexical_disambiguation(words=None):
    for word in words:
        retain_tags = []

        if len(word.pos_tags) > 1:

            skip = word.prefix and word.infix and word.suffix

            if not skip:
                approp_lexical_rules = select_lexical_rules(word=word)
                for rule in approp_lexical_rules:
                    if rule.target in word.pos_tags:
                        retain_tags.append(rule.target)


                if len(retain_tags) > 0:
                    word.pos_tags = []
                    for tag in retain_tags:
                        word.pos_tags.append(tag)

    return words


'''
Contextual Disambiguation
'''
def apply_contextual_disambiguation(words=None):
    for idx, word in enumerate(words):
        if len(word.pos_tags) > 1:
            approp_rules = select_contextual_rules(word=word)

            for rule in approp_rules:
                if rule.operator == '=!!':
                    if satisfies_condition(rule=rule, word=word, words=words, curr_pos=idx):
                        word.pos_tags = [rule.target]
                    else:
                        if rule.target in word.pos_tags:
                            word.pos_tags.remove(rule.target)
                elif rule.operator == '=!':
                    if satisfies_condition(rule=rule, word=word, words=words, curr_pos=idx):
                        word.pos_tags = [rule.target]
                elif rule.operator == '=0':
                    if satisfies_condition(rule=rule, word=word, words=words, curr_pos=idx):
                        if rule.target in word.pos_tags:
                            word.pos_tags.remove(rule.target)

                if len(word.pos_tags) == 1:
                    break

    return words

'''
Helper function for Contextual Disambiguation
Gets the word in the current position
If None is returned, it means the position is invalid
'''
def get_word(words=[], position=-1):
    if position >= 0 and position < len(words):
        return words[position]

    return None

'''
Helper function
Gets a valid position
A valid position means that the pos tag on that word is not SYM
'''
def get_valid_position(words=None, position=-1, curr_pos=-1):

    curr_pos += position

    if curr_pos >= len(words) or curr_pos < 0:
        return curr_pos


    while 'SYM' in words[curr_pos].pos_tags:
        if position < 0:
            # Move one step to the left
            curr_pos = curr_pos + (position - 1)
        else:
            # Move one step to the right
            curr_pos = curr_pos + (position + 1)

        if curr_pos >= len(words) or curr_pos < 0:
            return curr_pos

    return curr_pos

'''
Helper function for Contextual Disambiguation
Checks if the current word meets the contextual conditions of the rule
'''
def satisfies_condition(rule=None, word=None, words=None, curr_pos=-1):
    for condition in rule.context_conditions:
        position = get_valid_position(words=words, position=condition.position, curr_pos=curr_pos)
        context_word = get_word(words=words, position=position)

        if context_word:
            if condition.careful_mode:
                if len(context_word.pos_tags) > 1:
                    return False
                else:
                    if condition.pos_tag not in context_word.pos_tags or condition.pos_tag != context_word.text:
                        return False
            else:
                if condition.pos_tag not in context_word.pos_tags or condition.pos_tag != context_word.text:
                    return False

        else:
            return False

    return True


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
    pass
