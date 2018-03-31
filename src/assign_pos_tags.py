from utilities import read_file, write_file
from tagger import tokenize, assign_pos_tags

'''
Assigns POS Tags on test sentences
'''
def assign_pos_tags_on_test_sentences():
    files = ['blog-sentences.txt']
    files = None
    
    if files:
        for f in files:
            sentences = read_file('data/test/tagger/input/' + f, strip=True)
            output = []

            for s in sentences:
                tokens = tokenize(text=s)
                words = assign_pos_tags(tokens=tokens)
                o_sentence = ''
                for w in words:
                    o_sentence += str(w) + ' '
                
                output.append(o_sentence)
            
            write_file(name='data/test/tagger/output/' + f, contents=output, no_encode=True, append_newline=True, add_newline=False)


if __name__ == '__main__':
    assign_pos_tags_on_test_sentences()