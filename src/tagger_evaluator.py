from polyglot.text import Text
from utilities import read_file, write_file
from wrappers import Word
from tagger import tag_sentence

'''
Fetches the unlabeled sentences
'''
def fetch_unlabeled_sentences():
    # files = ['example-sentences.txt','news-sentences.txt', 'blog-sentences.txt']
    # files =  ['news-sentences.txt', 'blog-sentences.txt']
    # files = ['blog-sentences.txt']
    # files = ['news-sentences.txt'] 
    files = ['example-sentences.txt']

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
        sentence = tag_sentence(text=sentence)
        for word in sentence:
            words.append(word)
    # print("Number of tokens: " + str(num_tokens) + '\n')
    # print("Disambiguated: " + str((disambiguated_count / float(num_tokens)) * 100) + '% (' + str(disambiguated_count) + ') \n')
    return words


'''
Extract actual POS tags
'''
def extract_actual_pos_tags():
    actual_pos_tags = []

    # files = ['example-sentences.txt', 'news-sentences.txt', 'blog-sentences.txt']
    # files =  ['news-sentences.txt', 'blog-sentences.txt']
    # files = ['blog-sentences.txt']
    # files = ['news-sentences.txt'] 
    files = ['example-sentences.txt']

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
        predicted_pos_tags.append(word[1])
        
    return predicted_pos_tags


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


# TP FP FN TN
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


def performance(values=[]):
    perf = [[0 for i in range(4)] for j in range(11)]


    
    for i in range(11):
        tp = values[i][0]
        fp = values[i][1]
        fn = values[i][2]
        tn = values[i][3]

        # Get Accuracy
        # TP + TN / TP + TN + FP + FN
        # if tp > 0 and tn > 0 and fp > 0 and fn > 0:
        if (tp + tn + fp + fn) != 0:
            perf[i][0] = float(tp + tn) / (tp + tn + fp + fn)

        # Get Precision
        #  TP / TP + FP
        # if tp > 0 and fp > 0:
        if (tp + fp) != 0:
            perf[i][1] = float(tp) / (tp + fp)

        # Get Recall
        # TP / TP + FN
        
        # if tp > 0 and fn > 0:
        if (tp + fn) != 0:
            perf[i][2] = float(tp) / (tp + fn)

        # Get Fscore
        # 2 * ((precision * recall) / (precision + recall))
        precision = perf[i][1]
        recall = perf[i][2] 

        # if precision > 0 and recall > 0:
        if (precision + recall) != 0:
            perf[i][3] = 2 * (float(precision * recall) / (precision + recall))
    
    return perf
     
