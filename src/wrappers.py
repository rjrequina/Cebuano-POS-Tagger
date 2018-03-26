'''
Wrapper for stems of a word
'''
class Stem:
    def __init__(self, word=None, root=None, prefix=None, suffix=None, infix=None):
        self.word = word
        self.root = word
        self.prefix = prefix
        self.infix = infix
        self.suffix = suffix
        self.is_entry = False

    def __str__(self):
        contents = ''
        contents = contents + 'Word: ' + self.word + '\n'
        contents = contents + 'Root: ' + str(self.root) + '\n'
        contents = contents + 'Prefix: ' + str(self.prefix) + '\n'
        contents = contents + 'Infix: ' + str(self.infix) + '\n'
        contents = contents + 'Suffix: ' + str(self.suffix) + '\n'
        contents = contents + 'Dictionary Entry: ' + str(self.is_entry) + '\n'

        return contents


'''
Wrapper for each word with their stems and pos tags
'''
class Word:
    def __init__(self, stem=None, pos_tags=[], word=''):
        self.stem = stem
        self.pos_tags = []
        self.root_tags = []
        self.derived_tags = []
        self.is_close = False
        self.word = word
        self.orig_word = word


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
    def __init__(self, word=None, target=None, base=[], prefix=None, suffix=None, infix=None):
        self.word = word
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
