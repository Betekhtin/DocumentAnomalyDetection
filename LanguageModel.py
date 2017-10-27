import nltk.probability as prob
from read_ngrams import unigrams, bigrams, trigrams
from nltk.util import ngrams
from ContractStructure import Sentence


class TrigramModel:

    def __init__(self, freq_unigrams, freq_bigrams, freq_trigrams, lambdas=(1, 0, 0), prob_dist=prob.MLEProbDist):
        self.unigram_dist = prob_dist(freq_unigrams)
        self.bigram_dist = prob_dist(freq_bigrams)
        self.trigram_dist = prob_dist(freq_trigrams)
        self.unigram_freq = freq_unigrams
        self.bigram_freq = freq_bigrams
        self.trigram_freq = freq_trigrams
        self.lambdas = lambdas

    def _simple_backoff(self, ngram, alpha=0.4):
        if len(ngram) > 3: raise Exception('Maximal length of ngram in trigram model is 3')

        if len(ngram) == 3:
            if self.trigram_freq[ngram] == 0:
                return alpha * self._simple_backoff(tuple([ngram[1], ngram[2]]))
            else: return self.trigram_dist.prob(ngram)
        if len(ngram) == 2:
            if self.bigram_freq[ngram] == 0:
                return alpha * self.unigram_dist.prob(ngram[1])
            else: return self.bigram_dist.prob(ngram)
        return self.unigram_dist.prob(ngram)

    def _linear_interpolation(self, trigram):
        if (self.lambdas[0] + self.lambdas[1] + self.lambdas[2] != 1): raise Exception('Sum of coefficients in interpolation should be equal to 1')
        if len(trigram) != 3: raise Exception('Length of ngram in trigram model is 3')
        return self.lambdas[0] * self.trigram_dist.prob(trigram) + \
               self.lambdas[1] * self.bigram_dist.prob(tuple([trigram[1], trigram[2]])) + \
               self.lambdas[2] * self.unigram_dist.prob(tuple([trigram[2]]))

    def get_probabilities(self, sentence, method=_simple_backoff):
        trigrams = ngrams(['#', '#'] + Sentence(sentence).normalize().tokenize(), 3)
        probs = []
        for trigram in trigrams:
            probs.append(method(self, trigram))
        return probs

if __name__ == '__main__':
    model1 = TrigramModel(unigrams, bigrams, trigrams, lambdas=(0.5, 0.3, 0.2), prob_dist=prob.LaplaceProbDist)
    model2 = TrigramModel(unigrams, bigrams, trigrams, lambdas=(0.5, 0.3, 0.2))
    str = "Настоящим Договором предусмотрено"
    print(Sentence(str).normalize().tokenize())
    print('Laplace Backoff probabilities: ', model1.get_probabilities(str))
    print('MLE Interpolation probabilities: ',model1.get_probabilities(str, TrigramModel._linear_interpolation))
    print('MLE Backoff probabilities: ', model2.get_probabilities(str))
    print('MLE Interpolation probabilities: ',model2.get_probabilities(str, TrigramModel._linear_interpolation))