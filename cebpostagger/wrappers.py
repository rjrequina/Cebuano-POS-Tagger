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
