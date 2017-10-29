import nltk.probability as prob
import os
from nltk.util import ngrams
from paths import doc_obj_folder
from read_ngrams import unigrams, bigrams, trigrams
from TestingDocument import TestingDocument

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
        if len(ngram) > 3:
            raise Exception('Maximal length of ngram in trigram model is 3')
        # print(len(ngram), ngram)
        if len(ngram) == 3:
            if self.trigram_freq[ngram] == 0:
                return alpha * self._simple_backoff(tuple([ngram[1], ngram[2]]))
            else:
                return self.trigram_dist.prob(ngram)
        if len(ngram) == 2:
            if self.bigram_freq[ngram] == 0:
                return alpha * self.unigram_dist.prob((ngram[1],))
            else:
                return self.bigram_dist.prob(ngram)
        return self.unigram_dist.prob(ngram)

    def _linear_interpolation(self, trigram):
        if self.lambdas[0] + self.lambdas[1] + self.lambdas[2] != 1:
            raise Exception('Sum of coefficients in interpolation should be equal to 1')
        if len(trigram) != 3:
            raise Exception('Length of ngram in trigram model is 3')
        return self.lambdas[0] * self.trigram_dist.prob(trigram) + \
               self.lambdas[1] * self.bigram_dist.prob(tuple([trigram[1], trigram[2]])) + \
               self.lambdas[2] * self.unigram_dist.prob(tuple([trigram[2]]))

    def get_probabilities(self, sentence, method=_simple_backoff):
        trigrams = ngrams(['#', '#'] + sentence, 3) # Sentence(sentence).normalize().tokenize() -> sentence
        probs = []
        for trigram in trigrams:
            probs.append(method(self, trigram))
        return probs

    def test_document(self, testDoc, low_bound=5e-6, method=_simple_backoff):
        t_p, f_p, t_n, f_n = 0, 0, 0, 0
        print("+: ", testDoc.positives, " | -: ", testDoc.negatives)
        for sentence in testDoc.modeling_data:
            probs = self.get_probabilities(TestingDocument.get_sentence(sentence), method)
            for i in range(len(probs)):
                if probs[i] < low_bound:
                    #false negative
                    if sentence[i][1] == True:
                        f_n += 1
                    #true negative
                    else:
                        t_n += 1
                else:
                    #true positive
                    if sentence[i][1] == True:
                        t_p += 1
                    #false positive
                    else:
                        f_p += 1
        print('++: ', t_p, " | +-: ", f_n, " | -+: ", f_p, " | --: ", t_n)
        return (t_p + t_n) / sum([len(sentence) for sentence in testDoc.modeling_data])

if __name__ == '__main__':
    model1 = TrigramModel(unigrams, bigrams, trigrams, lambdas=(0.5, 0.3, 0.2)) #, prob_dist=prob.LaplaceProbDist)
    # model2 = TrigramModel(unigrams, bigrams, trigrams, lambdas=(0.5, 0.3, 0.2))
    # str = "Настоящим Договором предусмотрено"
    # print('Laplace Backoff probabilities: ', model1.get_probabilities(str))
    # print('MLE Interpolation probabilities: ', model1.get_probabilities(str, TrigramModel._linear_interpolation))
    # print('MLE Backoff probabilities: ', model2.get_probabilities(str))
    # print('MLE Interpolation probabilities: ', model2.get_probabilities(str, TrigramModel._linear_interpolation))
    test_doc = TestingDocument()
    test_doc.load(os.path.join(doc_obj_folder, '0cb3fa5380193efefeac0c461b'))
    print(str(model1.test_document(test_doc)) + "%")