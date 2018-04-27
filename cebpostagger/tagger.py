import string
# from polyglot.text import Text
from nltk.tokenize import word_tokenize
from cebdict import dictionary
from cebstemmer import stemmer

'''
Wrapper for each word with its properties

Properties:
    root_tags = tags of the word from the dictionary
    derived_tags = tags of the word from lexical rules
    is_close = boolean to check if the current word is a function word
    pos_tags = tag/s of the word
    text = the word itself (string)
    prefix = prefix of the word
    infix = infix of the word
    suffix = suffix of the word
    root = root of the word
    is_entry = boolean to check if the current is a dictionary entry
'''
class Word:
    def __init__(self, text=None):
        self.pos_tags = []
        self.root_tags = []
        self.derived_tags = []
        self.is_close = False
        self.orig_text = text
        self.text = text.lower() if text is not None else text
        self.prefix = None
        self.infix = None
        self.suffix = None
        self.root = text.lower() if text is not None else text
        self.is_entry = False


    def to_lower():
        if self.text:
            return self.text.lower()

        return self.text

    def __str__(self):
        return self.orig_text.encode('utf-8') + '/' + str(','.join(self.pos_tags))

    def print_stem_results(self):
        pref = self.prefix if self.prefix else '-'
        inf = self.infix if self.infix else '-'
        suff = self.suffix if self.suffix else '-'

        text = self.text + ':[(' + str(self.root) +  '), {' + pref + ',' + inf + ',' + suff + '}]'
        return text
'''
Wrapper for each contextual rule

Operator:

'=!!' indicates that the target reading is the correct one if and only if all context conditions are satisfied; all other readings should be discarded. If the context conditions are not satisfied, the target reading itself is discarded.

'=!' indicates that the target reading is the correct one if and only if all context conditions are satisfied, all other readings are discarded.

'=0' indicates that the target reading will be discarded if and only of the context conditions are satisfied, it leaves all other readings.
'''
class ContextualRule:
    def __init__(self):
        self.operator = '=!!'
        self.target = None
        self.context_conditions = []

    def __str__(self):
        rule = ''
        rule = rule + '( Target: ' + self.target + ', '
        rule = rule + 'Operator: ' + self.operator + ' )'
        return rule
'''
Wrapper for each lexical rule
'''
class LexicalRule:
    def __init__(self):
        self.target = None
        self.base = []
        self.prefix = None
        self.suffix = None
        self.infix = None

'''
Wrapper for each context condition
'''
class ContextCondition:
    def __init__(self):
        self.polarity = None
        self.position = 0
        self.pos_tag = None
        self.careful_mode = False

    def __str__(self):
        condition = ''
        condition = condition + '( Polarity: ' + str(self.polarity) + ', '
        condition = condition + 'Position: ' + str(self.position) + ', '
        condition = condition + 'Careful: ' + str(self.careful_mode) + ', '
        condition = condition + 'Tag: ' + str(self.pos_tag) + ' )'

        return condition

'''
Fetch lexical rules
'''
def lexical_rules():
    raw = [ 'VERB gi - -', 
            'NOUN hi - -',
            'VERB i - -',
            'NOUN ika - -',
            'ADV inigka - - NOUN',
            'NOUN isigka - -',
            'ADV ka - - NOUN',
            'ADV ka - - NUM',
            'NOUN ka - - VERB',
            'ADV kada - -',
            'VERB mag - -',
            'VERB maka - -',
            'VERB magka - -',
            'VERB man - -',
            'VERB manga - - VERB',
            'VERB mang - -',
            'VERB mo - -',
            'VERB na - -',
            'VERB nag - -',
            'VERB naka - -',
            'VERB nang - -',
            'VERB nanga - -',
            'PRON ni - - VERB',
            'VERB ni - - VERB',
            'NOUN pag - -',
            'NOUN pagka - -',
            'ADJ pala - -',
            'ADJ pinaka - -',
            'NOUN tag - -',
            'NOUN taga - -',
            'NOUN tig - -',
            'NOUN ting - -',
            'ADJ - in - NOUN',
            'NOUN - in - NOUN',
            'NOUN - um -',
            'VERB - - a',
            'ADJ - - an ADJ',
            'NOUN - - an NOUN VERB',
            'VERB - - an VERB',
            'VERB gi - an',
            'VERB gihi - an VERB',
            'ADJ ka - an',
            'NOUN ka - an NOUN',
            'NOUN - in an',
            'NOUN - - anan',
            'ADJ - - dor',
            'NOUN - - era',
            'NOUN - - ero',
            'ADJ - - g ADJ',
            'VERB gi - g VERB',
            'NOUN - - han',
            'VERB - - han',
            'VERB - - hon',
            'VERB - - i',
            'VERB ka - i',
            'ADJ  - - ng',
            'ADJ ni - ng VERB',
            'ADJ  - - on VERB NOUN ADJ',
            'NOUN - - on VERB',
            'VERB - - on VERB',
            'ADJ gi - on ADJ',
            'NOUN gi - on NOUN',
            'NOUN ka - on',
            'ADJ ma - on ADJ VERB',
            'ADJ - - or VERB',
            'NOUN - - or VERB',
            'NOUN - - syon',
            'VERB nahi - -',
            'VERB gihi - -']
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
    raw = [ '=!! NOUN 1 PART',
            '=!! NOUN 2 PRON',
            '=!! NOUN 3 PART',
            '=!! NOUN 4 PART',
            '=!! NOUN 5 DET',
            '=!! NOUN 6 NOUN',
            '=!! PART -1 NOUN',
            '=!! PART 1 PRON',
            '=!! PART 2 PART',
            '=!! PART 3 PART',
            '=!! PART 4 DET',
            '=!! PART 5 NOUN',
            '=!! PRON -1 PART',
            '=!! PRON 1 PART',
            '=!! PRON 2 PART',
            '=!! PRON 3 DET',
            '=!! PRON 4 NOUN',
            '=!! PART -1 PRON',
            '=!! PART 1 NOUN',
            '=!! PART 1 PART',
            '=!! PART 2 DET',
            '=!! PART 3 NOUN',
            '=!! PART -1 PART',
            '=!! PART 2 NOUN',
            '=!! PART 1 DET',
            '=!! DET -1 PART',
            '=!! DET 1 PRON',
            '=!! DET 2 PART',
            '=!! DET 3 NOUN',
            '=!! DET 1 NOUN',
            '=!! NOUN -1 DET',
            '=!! NOUN 4 NOUN',
            '=!! NOUN 2 NOUN',
            '=!! NOUN -1 PART',
            '=!! NOUN 3 PRON',
            '=!! NOUN 4 VERB',
            '=!! NOUN 5 PART',
            '=!! NOUN 6 PRON',
            '=!! NOUN 7 PRON',
            '=!! NOUN 8 PART',
            '=!! NOUN 9 NOUN',
            '=!! PART 2 PRON',
            '=!! PART 3 VERB',
            '=!! PART 4 PART',
            '=!! PART 5 PRON',
            '=!! PART 6 PRON',
            '=!! PART 7 PART',
            '=!! PART 8 NOUN',
            '=!! PRON 1 PRON',
            '=!! PRON 2 VERB',
            '=!! PRON 3 PART',
            '=!! PRON 4 PRON',
            '=!! PRON 5 PRON',
            '=!! PRON 6 PART',
            '=!! PRON 7 NOUN',
            '=!! PRON -1 PRON',
            '=!! PRON 1 NOUN',
            '=!! PRON 1 VERB',
            '=!! PRON 3 PRON',
            '=!! PRON 5 PART',
            '=!! PRON 6 NOUN', 
            '=!! VERB -1 PRON',
            '=!! VERB 1 PART',
            '=!! VERB 2 NOUN',
            '=!! VERB 2 PRON',
            '=!! VERB 3 PRON', 
            '=!! VERB 4 PART',
            '=!! VERB 5 NOUN',
            '=!! PART -1 VERB', 
            '=!! PART 4 NOUN', 
            '=!! PRON 2 PRON',
            '=!! PRON 3 NOUN',
            '=!! PRON 4 PART',
            '=!! PRON 5 NOUN',
            '=!! PRON 2 NOUN',
            '=!! PART 2 VERB',
            '=!! PART 3 PRON',
            '=!! PART 4 PRON',
            '=!! PART 5 PART',
            '=!! PART 6 NOUN',
            '=!! NOUN 1 PRON',
            '=!! NOUN 2 PART', 
            '=!! NOUN 3 VERB',
            '=!! NOUN 4 PRON',
            '=!! NOUN 5 PRON',
            '=!! NOUN 6 PART',
            '=!! NOUN 7 NOUN',
            '=!! PRON 2 DET',
            '=!! PRON 3 ADJ',
            '=!! PRON 5 ADV',
            '=!! PRON 6 VERB',
            '=!! PART 2 ADJ',
            '=!! PART 4 ADV',
            '=!! PART 5 VERB',
            '=!! DET 1 ADJ',
            '=!! DET 3 ADV',
            '=!! DET 4 VERB',
            '=!! ADJ -1 DET',
            '=!! ADJ 1 PRON',
            '=!! ADJ 1 PART',
            '=!! ADJ 2 ADV',
            '=!! ADJ 3 VERB',
            '=!! PART -1 ADJ',
            '=!! PART 1 ADV',
            '=!! ADV -1 PART',
            '=!! ADV 1 DET',
            '=!! ADV 2 PART',
            '=!! ADV 3 PRON',
            '=!! ADV 1 VERB', 
            '=!! VERB -1 ADV',
            '=!! VERB 1 ADJ',
            '=!! VERB 2 DET',
            '=!! VERB 3 PART',
            '=!! VERB 4 PRON',
            '=!! NUM 1 PART',
            '=!! NUM 2 NOUN',
            '=!! NUM 3 NOUN',
            '=!! NUM 4 VERB', 
            '=!! NUM 5 PRON',
            '=!! PART -1 NUM',
            '=!! NOUN 1 NOUN',
            '=!! NOUN 2 VERB',
            '=!! NOUN -1 NOUN', 
            '=!! NOUN 1 NUM',
            '=!! NOUN 1 VERB',
            '=!! VERB -1 NOUN',
            '=!! VERB 2 NUM',
            '=!! VERB 1 PRON',
            '=!! PRON -1 VERB',
            '=!! PRON 3 NUM',
            '=!! PRON 2 ADV',
            '=!! PRON 4 ADJ', 
            '=!! PART 3 ADJ',
            '=!! ADV 1 ADJ',
            '=!! ADV 2 ADJ',
            '=!! ADJ -1 ADV',
            '=!! ADJ 1 ADJ',
            '=!! ADJ -1 ADJ', 
            '=!! ADJ 2 PRON',
            '=!! VERB 1 DET',
            '=!! DET -1 VERB',
            '=!! ADJ 2 NOUN',
            '=!! ADJ 2 DET',
            '=!! ADJ 3 NOUN',
            '=!! NOUN 1 ADJ',
            '=!! NOUN 2 ADJ',
            '=!! PART 1 ADJ',
            '=!! ADJ -1 PART',
            '=!! DET 3 ADJ',
            '=!! ADJ 1 DET',
            '=!! ADJ 1 CONJ',
            '=!! ADJ 2 ADJ', 
            '=!! ADJ 3 PART',
            '=!! ADJ 4 NOUN',
            '=!! CONJ -1 ADJ',
            '=!! CONJ 1 ADJ',
            '=!! CONJ 2 PART',
            '=!! CONJ 3 NOUN',
            '=!! ADJ -1 CONJ',
            '=!! NOUN 1 CONJ',
            '=!! ADJ 4 DET',
            '=!! ADJ 5 NOUN',
            '=!! CONJ 3 DET',
            '=!! CONJ 4 NOUN',
            '=!! DET 1 CONJ',
            '=!! DET 2 ADJ',
            '=!! NOUN 2 CONJ',
            '=!! NOUN 3 ADJ',
            '=!! NOUN 3 CONJ',
            '=!! NOUN 4 ADJ',
            '=!! PART 2 CONJ',
            '=!! CONJ 1 NOUN',
            '=!! PART 4 CONJ',
            '=!! PART 5 ADJ',
            '=!! ADJ 1 ADV',
            '=!! ADV -1 ADJ',
            '=!! DET 1 NUM',
            '=!! NUM -1 DET',
            '=!! PART 2 NUM',
            '=!! NUM -1 NOUN',
            '=!! ADV 1 PART',
            '=!! ADV 2 ADV',
            '=!! PART -1 ADV',
            '=!! ADV 1 ADV',
            '=!! ADV -1 ADV',
            '=!! ADV 1 NOUN',
            '=!! NOUN -1 ADV',
            '=!! CONJ 1 CONJ',
            '=!! CONJ -1 CONJ',
            '=!! CONJ 1 PART',
            '=!! PART -1 CONJ',
            '=!! DET 1 DET',
            '=!! DET 2 NOUN',
            '=!! DET -1 DET',
            '=!! NOUN 1 DET',
            '=!! DET 3 PART',
            '=!! DET 4 ADJ',
            '=!! PART 3 DET',
            '=!! DET 1 PART',
            '=!! DET 2 PRON',
            '=!! PRON -1 NOUN',
            '=!! DET 3 PRON',
            '=!! PRON 1 DET',
            '=!! PRON 3 CONJ', 
            '=!! DET -1 PRON',
            '=!! DET 2 CONJ',
            '=!! CONJ -1 NOUN',
            '=!! CONJ 1 PRON',
            '=!! NOUN -1 CONJ',
            '=!! PART 4 ADJ',
            '=!! ADJ 2 PART',
            '=!! DET -1 ADJ',
            '=!! PRON -1 DET',
            '=!! VERB 2 ADJ',
            '=!! PRON 1 ADJ',
            '=!! ADJ -1 PRON',
            '=!! PRON -1 ADJ', 
            '=!! VERB 3 DET',
            '=!! DET 1 VERB']
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
    ltokens = text.strip().split()
    tokens = []
    for lk in ltokens:
        if lk[-1] in string.punctuation:
            tokens.append(lk[:-1])
            tokens.append(lk[-1])
        else:
            tokens.append(lk)

    return tokens


'''
POS Tag Assignment
Assigns all possible POS tags per token
'''
def assign_pos_tags(tokens=[]):
    words = []
    for idx, token in enumerate(tokens):
        stem = stemmer.stem_word(word=token, as_object=True)
        word = dictionary_search(word=stem)
        word = apply_lexical_rules_assignment(word=stem)
        word = apply_capitalization_assignment(word=stem, pos=idx)

        if len(word.pos_tags) == 0:

            if any(i.isdigit() for i in stem.text):
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
