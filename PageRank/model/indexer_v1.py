from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import json
import math

from model.bag_of_words import MyEncoder, BagOfWords


class Indexer(object):

    def __init__(self, document_list=None, enable_stemming=True, filter_stopwords=True):
        self.words_index = {}
        self.num_docs = 0
        if document_list is not None:
            for doc in document_list:
                self.index(BagOfWords(doc, enable_stemming=enable_stemming, filter_stopwords=filter_stopwords))

    def index(self, bag):
        """Indexa un Bag of Words en el indice

        :param bag: Bag of words a insertar
        """
        for term, tf in bag:
            if term in self.words_index:
                self.words_index[term]["documents"].extend([{"tf": tf / bag.document_len(), "document": bag}])
            else:
                self.words_index[term] = {"idf": -1., "documents": [{"tf": tf / bag.document_len(), "document": bag}]}

        self.num_docs = self.num_docs + 1
        for term, values in self.words_index.items():
            values["idf"] = self.__calc_idf(term)

    def get_term(self, term):
        try:
            return self.words_index[term]
        except:
            print("Error en la busqueda del termino %s".format(term))

    def __calc_idf(self, term):
        idf = 1 + math.log10(self.num_docs / self.words_index[term]["documents"].__len__())
        return idf

    def dump(self, fd):
        fd.write(json.dumps(self.words_index, cls=MyEncoder))
        return fd.getvalue()
