# Read unigrams, bigrams and trigrams from their files
from nltk import FreqDist
import os

ngrams_folder = os.path.join(os.getcwd(), 'ngrams')

unigrams = FreqDist()
bigrams = FreqDist()
trigrams = FreqDist()

with open(os.path.join(ngrams_folder, 'unigrams.txt'), 'r', encoding='utf-8') as file:
    for line in file.readlines():
        entry = line.strip().split(' ')
        unigrams[(entry[0],)] = int(entry[1])

with open(os.path.join(ngrams_folder, 'bigrams.txt'), 'r', encoding='utf-8') as file:
    for line in file.readlines():
        entry = line.strip().split(' ')
        bigrams[tuple(entry[0:2])] = int(entry[2])

with open(os.path.join(ngrams_folder, 'trigrams.txt'), 'r', encoding='utf-8') as file:
    for line in file.readlines():
        entry = line.strip().split(' ')
        trigrams[tuple(entry[0:3])] = int(entry[3])