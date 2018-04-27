from utilities import read_file, write_file
from polyglot.detect import Detector

'''
Filters Cebuano sentences from news-raw.txt
Each sentence will be fed in a language detector.
It will return the languages and corresponding confidence for each sentences.
Sentence with 'Cebuano' language and with at least 75% confidence will be included.
Cebuano sentences will be stored in news-set-unchecked.txt
'''
def filter_cebuano_sentences():
    checkpoint = read_file('../data/scraped/cp/news-raw-cp.txt')
    start = int(checkpoint[0])
    if start >= 5060:
        print("Status: Finished!")
        return

    sentences = read_file("data/scraped/news-raw-nc.txt", start=start)
    write_file("data/scraped/news-raw-nc.txt", contents=[''], mode="w", add_newline=False, no_encode=True)

    for sentence in sentences:
        start += 1
        is_cebuano = False
        languages = Detector(sentence.decode('utf-8'), quiet=True).languages
        for language in languages:
            if language.name == "Cebuano":
                print(language.confidence)
                if float(language.confidence) >= 75.0:
                    is_cebuano = True
                    break

        if is_cebuano:
            write_file("data/scraped/news-raw-nc.txt", contents=[sentence], mode="a", add_newline=False, no_encode=True)

        write_file("data/scraped/cp/news-raw-cp.txt", contents=[str(start + 1)], mode="w")
        print("Sentence [" + str(start) + "]: OK")


if __name__ == '__main__':
    # filter_cebuano_sentences()
    pass
