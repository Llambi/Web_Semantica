from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import json
import math

from bag_of_words import BagOfWords


class Indexer(object):

    def __init__(self):
        self.docs_index = []
        self.words_index = {}
        self.num_docs = 0

    def index(self, bag):
        """Indexa un Bag of Words en el indice

        :param bag: Bag of words a insertar
        """
        self.docs_index.append(bag.values)
        for key, value in bag:
            if key in self.words_index:
                self.words_index[key].append([[value, bag.document_len()], self.num_docs])
            else:
                self.words_index[key] = [[[value, bag.document_len()], self.num_docs]]
        self.num_docs = self.num_docs + 1

    def score(self, text, enable_stemming=True, filter_stopwords=True):
        """Calcula los scores de cada documento para un texto

        Devuelve una lista con formato [[score1,docId], [score2, docId], ...]

        :param text: Texto del que obtener el score
        :param enable_stemming: True para habilitar la lematizacion
        :param filter_stopwords: True para habilitar la eliminacion de stop words
        :return: Devuelve una lista con los scores del texto para cada documento
        """
        bag = BagOfWords(values=text, enable_stemming=enable_stemming, filter_stopwords=filter_stopwords)
        text = next(iter(bag.string_to_bag_of_words(text, {})))
        t = self.words_index[text]
        idf = math.log10(self.num_docs / len(t))
        tf = list(reversed(list(map(lambda x: [x[0][0] / x[0][1], x[1]], t))))  # ordenados de mayor a menor
        tfidf = map(lambda x: [x[0] * idf, x[1]], tf)
        return tfidf

    def dump(self, fd):
        """Genera un json con words_index y docs_index"""
        fd.write(json.dumps({"words_index": self.words_index, "docs_index": self.docs_index}))
