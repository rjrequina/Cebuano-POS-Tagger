from nltk.tokenize import word_tokenize
from utilities import read_file, write_file
from cebpostagger.tagger import tag_sentence
import string

'''
Fetches the unlabeled sentences
'''
def fetch_unlabeled_sentences(test_all=True, specific=''):
    files = ['example-sentences.txt','news-sentences.txt', 'blog-sentences.txt']
    if not test_all:
        files = [specific]

    sentences = []

    for f in files:
        contents = read_file('data/test/input/' + f, strip=True, decode=True)
        sentences += contents

    return sentences

'''
Tags all the test sentences
'''
def tag_test_sentences(test_all=True, specific=''):
    sentences = fetch_unlabeled_sentences(test_all=test_all, specific=specific)
    words = []

    for sentence in sentences:
        sentence = tag_sentence(text=sentence)
        for word in sentence:
            words.append(word)
    return words


'''
Extract actual POS tags
'''
def extract_actual_pos_tags(test_all=True, specific=''):
    actual_pos_tags = []

    files = ['example-sentences.txt', 'news-sentences.txt', 'blog-sentences.txt']
    if not test_all:
        files = [specific]

    for f in files:
        sentences = read_file('data/test/output/' + f, strip=True)

        for sentence in sentences:
            tokens = sentence.split(' ')
            for token in tokens:
                l = token.split('/')
                actual_pos_tags.append(l[1].upper())

    return actual_pos_tags


'''
Extract predicted POS tags
'''
def extract_predicted_pos_tags(words=[]):
    predicted_pos_tags = []
    for word in words:
        predicted_pos_tags.append(word[1])
        
    return predicted_pos_tags


'''
Generates confusion matrix
'''
def confusion_matrix(actual=[], pred=[]):
    idx = {
        'ADJ' : 0,
        'ADV' : 1,
        'CONJ': 2,
        'DET' : 3,
        'NOUN': 4,
        'NUM' : 5,
        'OTH' : 6,
        'PART': 7,
        'PRON': 8,
        'SYM' : 9,
        'VERB': 10
    }

    matrix = [[0 for i in range(11)] for j in range(11)]

    for i in range(0, len(actual)):
       matrix[idx[actual[i]]][idx[pred[i]]] += 1
    
    return matrix

'''
Gives the TP, FP, FN, TN given a confusion matrix
'''
def cm_values(matrix=[]):
    values = [[0 for i in range(4)] for j in range(11)]

    # Extract True Positives
    for i in range(11):
        values[i][0] = matrix[i][i]
    
    # Extract False Positives
    for i in range(11):
        for j in range(11):
            if i != j:
                values[i][1] += matrix[j][i]

    # Extract False Negatives
    for i in range(11):
        for j in range(11):
            if i != j:
                values[i][2] += matrix[i][j]
    
    # Extract True Negatives
    total = 0
    for i in range(11):
        for j in range(11):
            total += matrix[i][j]
    
    for i in range(11):
            values[i][3] = total - (values[i][0] + values[i][1] + values[i][2])

    return values