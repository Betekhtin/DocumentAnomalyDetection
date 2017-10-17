import os
from nltk import FreqDist
import nltk.probability as prob

from ContractStructure import Sentence

class TrigramModel:

    def __init__(self, freq_unigrams, freq_bigrams, freq_trigrams, lambdas = (1,0,0)):
        self.unigram_dist = prob.MLEProbDist(freq_unigrams)
        self.bigram_dist = prob.MLEProbDist(freq_bigrams)
        self.trigram_dist = prob.MLEProbDist(freq_trigrams)
        self.unigram_freq = freq_unigrams
        self.bigram_freq = freq_bigrams
        self.trigram_freq = freq_trigrams
        self.lambdas = lambdas

    def _simple_backoff(self, ngram, alpha=0.4):
        if len(ngram) != 3: raise Exception('Maximal length of ngram in trigram model is 3')

        if len(ngram) == 3:
            if self.trigram_freq[ngram] == 0:
                return alpha * self._simple_backoff(tuple([ngram[1], ngram[2]]))
            else: return self.trigram_dist.prob(ngram)
        if len(ngram) == 2:
            if self.bigram_freq[ngram] == 0:
                return alpha * self.unigram_dist.prob(ngram[2])
            else: return self.bigram_dist.prob(ngram)
        return self.unigram_dist.prob(ngram)

    def _linear_interpolation(self, trigram):
        if (self.lambdas[0] + self.lambdas[1] + self.lambdas[2] != 1): raise Exception('Sum of coefficients in interpolation should be equal to 1')
        if len(trigram) != 3: raise Exception('Length of ngram in trigram model is 3')
        return self.lambdas[0] * self.trigram_dist.prob(trigram) + \
               self.lambdas[1] * self.bigram_dist.prob(tuple([trigram[1], trigram[2]])) + \
               self.lambdas[2] * self.unigram_dist.prob(tuple([trigram[2]]))

    def get_probabilities(self, sentence, method=_simple_backoff):
        tokens = Sentence(sentence).normalize().tokenize()
        probs = []
        if len(tokens) > 0:
            probs.append(method(tuple([tokens[0]])))
            if len(tokens) > 1:
                probs.append(method(tuple([tokens[0], tokens[1]])))
        for i in range(2, len(tokens)):
            probs.append(method(tuple([tokens[i - 2], tokens[i - 1], tokens[i]])))
        print(tokens)
        return probs

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

model = TrigramModel(unigrams, bigrams, trigrams, (0.5, 0.3, 0.1))
str = "Настоящим Договором предусмотрено получение Товара Получателем на складе Поставщика, если иное не оговорено Сторонами в дополнительном соглашении"
print(Sentence(str).normalize().tokenize())
print(model.get_probabilities(str))
print(model.get_probabilities(str, TrigramModel._linear_interpolation))
print(prob.MLEProbDist(trigrams).prob(('настоящее', 'договор', 'предусмотреть')))
print(model._simple_backoff(('настоящее', 'договор', 'предусмотреть')))