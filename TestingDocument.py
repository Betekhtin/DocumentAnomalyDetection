import random
import string
import nltk.probability as prob
from read_ngrams import unigrams
from ContractStructure import *
from paths import *

class TestingDocument(Document):

    prob_dist = prob.MLEProbDist(unigrams)

    def __init__(self):
        super().__init__()
        self.modeling_data = [list(map(lambda x: (x, True), sentence)) for sentence in self.modeling_data]
        self.positives = sum([len(sentence) for sentence in self.modeling_data])
        self.negatives = 0

    def load(self, path):
        with open(path, 'rb') as f:
            try:
                doc = pickle.load(f)
            except Exception as e:
                print(path)
                raise e
            self.title = doc.title
            self.preamble = doc.preamble
            self.main_text = doc.main_text
            self.attachment = doc.attachment
            if type(doc) is Document:
                self.modeling_data = [list(map(lambda x: (x, True), sentence)) for sentence in doc.modeling_data]
                self.positives = sum([len(sentence) for sentence in self.modeling_data])
                self.negatives = 0
                self._add_noise()
                self._add_words()
            elif type(doc) is TestingDocument:
                self.modeling_data = doc.modeling_data
                self.positives = doc.positives
                self.negatives = doc.negatives

    def _add_noise(self, low_bound = 0.0001, upper_bound = 0.01):
        def random_word():
            return ''.join(random.choices(string.ascii_letters, k=random.randint(1, 15)))
        negatives = 100 #random.randint(int(self.positives * low_bound), int(self.positives * upper_bound))
        for i in range(negatives):
            line = random.randint(0, len(self.modeling_data) - 1)
            word = random_word()
            self.modeling_data[line].insert(random.randint(0, len(self.modeling_data[line]) - 1), (word, False))
            # print(line, word)
        self.negatives += negatives

    def _add_words(self, low_bound = 0.0001, upper_bound = 0.01):
        negatives = 100 #random.randint(int(self.positives * low_bound), int(self.positives * upper_bound))
        for i in range(negatives):
            line = random.randint(0, len(self.modeling_data) - 1)
            word = TestingDocument.prob_dist.generate()[0]
            self.modeling_data[line].insert(random.randint(0, len(self.modeling_data[line]) - 1), (word, False))
            # print(line, word)
        self.negatives += negatives

    @staticmethod
    def get_sentence(word_list):
        return list(map(lambda x: x[0], word_list))

if __name__ == "__main__":
    parsed_doc = TestingDocument()
    parsed_doc.load(os.path.join(doc_obj_folder, '0cb3fa5380193efefeac0c461b'))
    # parsed_doc.save(test_obj_folder, '0cb3fa5380193efefeac0c461b')
    # parsed_doc.load(os.path.join(test_obj_folder, '0cb3fa5380193efefeac0c461b'))
    print(parsed_doc.modeling_data)
    print(parsed_doc.positives)
    print(parsed_doc.negatives)