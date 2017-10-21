from nltk.util import ngrams
import ContractStructure as cs
import os
import time

doc_folder = os.path.join(os.getcwd(), 'documents', 'txt', 'doc')
docx_folder = os.path.join(os.getcwd(),'documents', 'txt', 'docx')
ngrams_folder = os.path.join(os.getcwd(), 'ngrams')


unigrams = {}
bigrams = {}
trigrams = {}

abspath_doc = lambda x: os.path.join(doc_folder, x)
abspath_docx = lambda x: os.path.join(docx_folder, x)


#Elapsed time 1:  11764.10448050499
start = time.time()

for file in (list(map(abspath_doc, os.listdir(doc_folder))) + list(map(abspath_docx, os.listdir(docx_folder)))):
    d = cs.Document(file)
    print(file, ":", "none" if (d.main_text == []) else '')

    for paragraph in d.main_text: # + d.preamble.get_sentences(normalize=True, tokenize=True, remove_stop_words=True)
        for sentence in paragraph.get_sentences(normalize=True, tokenize=True, remove_stop_words=True):
            # get unigrams
            for unigram in sentence:
                unigrams[unigram] = (unigrams[unigram] + 1) if (unigram in unigrams) else 1
            # get bugrams
            for bigram in ngrams(['#'] + sentence, 2):
                bigrams[bigram] = (bigrams[bigram] + 1) if (bigram in bigrams) else 1
            # get trigrams
            for trigram in ngrams(['#', '#'] + sentence, 3):
                trigrams[trigram] = (trigrams[trigram] + 1) if (trigram in trigrams) else 1

    for sentence in d.preamble.get_sentences(normalize=True, tokenize=True, remove_stop_words=True):
        # get unigrams
        for unigram in sentence:
            unigrams[unigram] = (unigrams[unigram] + 1) if (unigram in unigrams) else 1
        # get bugrams
        for bigram in ngrams(['#'] + sentence, 2):
            bigrams[bigram] = (bigrams[bigram] + 1) if (bigram in bigrams) else 1
        # get trigrams
        for trigram in ngrams(['#', '#'] + sentence, 3):
            trigrams[trigram] = (trigrams[trigram] + 1) if (trigram in trigrams) else 1

finish = time.time()

print("Elapsed time: ", finish - start)

with open(os.path.join(ngrams_folder,'unigrams.txt'), 'w+', encoding='utf-8') as file:
    for key, value in unigrams.items():
        file.write(key + ' ' + str(value) + '\n')

with open(os.path.join(ngrams_folder,'bigrams.txt'), 'w+', encoding='utf-8') as file:
    for key, value in bigrams.items():
        file.write(' '.join(key) + ' ' + str(value) + '\n')

with open(os.path.join(ngrams_folder,'trigrams.txt'), 'w+', encoding='utf-8') as file:
    for key, value in trigrams.items():
        file.write(' '.join(key) + ' ' + str(value) + '\n')