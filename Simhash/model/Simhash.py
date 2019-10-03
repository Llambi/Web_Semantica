from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import binascii
from heapq import heapify, heappop

from nltk import ngrams

from model.BagOfWords import BagOfWords


class Simhash:

    def __init__(self, line=None, restrictiveness=None, ngram=0):
        self.__line = line
        self.__restrictiveness = restrictiveness
        self.__ngram = ngram

    def exec(self):
        """Realiza Simhash
        :param line: texto
        :param restrictiveness
        :param ngram: numero de ngramas
        :return:
        """
        if self.__ngram < 0:
            bag = BagOfWords(text=self.__line)
            if len(bag) == 0:
                return None
            hashes = self.__calculate_hashes(bag.values, self.__restrictiveness)
            return hashes
        else:
            bag = ngrams(self.__line.split(), self.__ngram)
            hashes = self.__calculate_hashes([' '.join(x) for x in bag], self.__restrictiveness)
            return hashes

    def __calculate_hashes(self, bag, restrictiveness):
        hashes = [binascii.crc32(x.encode("utf-8")) & 0xffffffff for x in bag]
        heapify(hashes)  # ordenar de pequeño a mayor
        simh = 0
        if len(hashes) <= restrictiveness:
            for i in range(len(hashes)):  # nos quedamos con los restrictiveness mas pequeños
                simh ^= heappop(hashes)  # hacer xor de todos con todos
            return simh
        else:
            for i in range(restrictiveness):  # nos quedamos con los restrictiveness mas pequeños
                simh ^= heappop(hashes)  # hacer xor de todos con todos
            return simh
