# Read unigrams, bigrams and trigrams from their files
from nltk import FreqDist
from paths import *

unigrams = FreqDist()
bigrams = FreqDist()
trigrams = FreqDist()

with open(unigrams_path, 'r', encoding='utf-8') as file:
    for line in file.readlines():
        entry = line.strip().split(' ')
        unigrams[(entry[0],)] = int(entry[1])

with open(bigrams_path, 'r', encoding='utf-8') as file:
    for line in file.readlines():
        entry = line.strip().split(' ')
        bigrams[tuple(entry[0:2])] = int(entry[2])

with open(trigrams_path, 'r', encoding='utf-8') as file:
    for line in file.readlines():
        entry = line.strip().split(' ')
        trigrams[tuple(entry[0:3])] = int(entry[3])