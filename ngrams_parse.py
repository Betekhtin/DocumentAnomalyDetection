from nltk.util import ngrams
import time
from ContractStructure import *
from paths import *

unigrams = {}
bigrams = {}
trigrams = {}

#Elapsed time 1:  11764.10448050499
#Elapsed time 2 (doc objects): 139.37553548812866
start = time.time()

for file in (list(map(abspath_doc, os.listdir(doc_obj_folder))) + list(map(abspath_docx, os.listdir(docx_obj_folder)))):
    d = Document()
    d.load(file)
    print(file, ":")
    for sentence in d.modeling_data:
        # get unigrams
        for unigram in sentence:
            unigrams[unigram] = (unigrams[unigram] + 1) if (unigram in unigrams) else 1
        # get bigrams
        for bigram in ngrams(['#'] + sentence, 2):
            bigrams[bigram] = (bigrams[bigram] + 1) if (bigram in bigrams) else 1
        # get trigrams
        for trigram in ngrams(['#', '#'] + sentence, 3):
            trigrams[trigram] = (trigrams[trigram] + 1) if (trigram in trigrams) else 1

finish = time.time()

print("Elapsed time: ", finish - start)

with open(unigrams_path, 'w+', encoding='utf-8') as file:
    for key, value in unigrams.items():
        file.write(key + ' ' + str(value) + '\n')

with open(bigrams_path, 'w+', encoding='utf-8') as file:
    for key, value in bigrams.items():
        file.write(' '.join(key) + ' ' + str(value) + '\n')

with open(trigrams_path, 'w+', encoding='utf-8') as file:
    for key, value in trigrams.items():
        file.write(' '.join(key) + ' ' + str(value) + '\n')