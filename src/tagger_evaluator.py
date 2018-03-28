from polyglot.text import Text
from utilities import read_file, write_file
from wrappers import Word
from tagger import tag_sentence

'''
Fetches the unlabeled sentences
'''
def fetch_unlabeled_sentences():
    files = ['example-sentences.txt','news-sentences.txt', 'blogs-sentences.txt']
    files =  ['news-sentences.txt']

    sentences = []

    for f in files:
        contents = read_file('data/test/tagger/input/' + f, strip=True, decode=True)
        sentences += contents

    return sentences

'''
Tags all the test sentences
'''
def tag_test_sentences():
    sentences = fetch_unlabeled_sentences()
    words = []

    disambiguated_count = 0
    non_disambiguated_count = 0
    num_tokens = 0
    for idx, sentence in enumerate(sentences):
        sentence_words = tag_sentence(text=sentence)
        tagged_sentence = ""

        for word in sentence_words:
            if len(word.pos_tags):
                num_tokens += 1
                if len(word.pos_tags) == 1:
                    disambiguated_count += 1
                else:
                    non_disambiguated_count += 1

            # if len(word.pos_tags) > 1:
            #      print(word)
            # if len(word.pos_tags):
            #     tagged_sentence +=  word.stem.word + "/" + word.pos_tags[0] + " "
            # else:
            #     tagged_sentence += word.stem.word
        words += sentence_words
    print("Number of tokens: " + str(num_tokens) + '\n')
    print("Disambiguated: " + str((disambiguated_count / float(num_tokens)) * 100) + '% (' + str(disambiguated_count) + ') \n')
    return words


'''
Extract actual POS tags
'''
def extract_actual_pos_tags():
    actual_pos_tags = []

    files = ['example-sentences.txt', 'news-sentences.txt', 'blogs-sentences.txt']
    files = ['news-sentences.txt']

    for f in files:
        sentences = read_file('data/test/tagger/output/' + f, strip=True)

        for sentence in sentences:
            tokens = list(Text(sentence).words)

            get_next = False
            for token in tokens:
                if token == '/':
                    get_next = True

                if token != '/' and get_next:
                    actual_pos_tags.append(token.upper())
                    get_next = False
    return actual_pos_tags


'''
Extract predicted POS tags
'''
def extract_predicted_pos_tags(words=[]):
    predicted_pos_tags = []
    for word in words:
        if len(word.pos_tags) > 0:
            predicted_pos_tags.append(word.pos_tags[0])

    return predicted_pos_tags
    
