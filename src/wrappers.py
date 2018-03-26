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
        self.text = text
        self.prefix = None
        self.infix = None
        self.suffix = None
        self.root = None
        self.is_entry = False


    def to_lower():
        if self.text:
            return self.text.lower()
        
        return self.text

    def __str__(self):
        return self.text + '/' + str(self.pos_tags)

'''
Wrapper for each contextual rule
'''
class ContextualRule:
    def __init__(self, operator='=0', target=None, context_conditions=[]):
        self.operator = operator
        self.target = target
        self.context_conditions = []

    def __str__(self):
        rule = ''
        rule = rule + '( Target: ' + self.target + ', '
        rule = rule + 'Operator: ' + self.operator
        rule = rule + ', '.join(self.context_conditions) + ' )'
        return rule
'''
Wrapper for each lexical rule
'''
class LexicalRule:
    def __init__(self, target=None, base=[], prefix=None, suffix=None, infix=None):
        self.target = target
        self.base = base
        self.prefix = prefix
        self.suffix = suffix
        self.infix = infix

'''
Wrapper for each context condition
'''
class ContextCondition:
    def __init__(self, polarity=None, position=0, pos_tag=None, careful_mode=False):
        self.polarity = polarity
        self.position = position
        self.pos_tag = pos_tag
        self.careful_mode = careful_mode

    def __str__(self):
        condition = ''
        condition = condition + '( Polarity: ' + str(self.polarity) + ', '
        condition = condition + 'Position: ' + str(self.position) + ', '
        condition = condition + 'Careful: ' + str(self.careful_mode) + ', '
        condition = condition + 'Tag: ' + str(self.pos_tag) + ' )'

        return condition
