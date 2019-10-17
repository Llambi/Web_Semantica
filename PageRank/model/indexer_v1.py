from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import json
import math

from model.bag_of_words import MyEncoder


class Indexer(object):

    def __init__(self):
        self.words_index = {}
        self.num_docs = 0

    def index(self, bag):
        """Indexa un Bag of Words en el indice

        :param bag: Bag of words a insertar
        """
        for term, tf in bag:
            if term in self.words_index:
                self.words_index[term]["documents"].extend([{"tf": tf, "documents": [bag]}])
            else:
                self.words_index[term] = {"idf": -1, "documents": [{"tf": tf, "documents": [bag]}]}

        self.num_docs = self.num_docs + 1
        for term, values in self.words_index.items():
            values["idf"] = self.__calc_idf(term)

    def __calc_idf(self, term):
        idf = -1 if len(self.words_index[term]["documents"]) == 0 else math.log10(
            self.num_docs / len(self.words_index[term]["documents"]))
        return idf

    def dump(self, fd):
        """Genera un json con words_index y docs_index"""
        fd.write(json.dumps(self.words_index, cls=MyEncoder))
        return fd.getvalue()
